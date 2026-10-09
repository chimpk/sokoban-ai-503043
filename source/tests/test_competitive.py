
import os
import sys
import tempfile
import time
import unittest

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from source.agents.agent_a import AgentA
from source.agents.agent_b import AgentB
from source.competitive.conflict import ConflictResolver
from source.competitive.engine import CompetitiveEngine, TimeoutGuard
from source.competitive.state import CompetitiveState


# Bản đồ kiểm thử:
# Hai agent, một hộp và hai đích.
MAP = """%%%%%%%
%A   A%
%     %
%D B D%
%%%%%%%
"""

REAL_MAP = os.path.join(
    os.path.dirname(__file__),
    "..",
    "maps",
    "competitive_map.txt"
)


def make_state(text=MAP, steps=50):
    """Tạo trạng thái từ bản đồ tạm dùng cho kiểm thử."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False
    ) as f:
        f.write(text)
        filename = f.name

    try:
        return CompetitiveState.from_map_file(filename, steps)
    finally:
        os.remove(filename)


def resolver(state):
    """Tạo bộ phân xử va chạm theo tường của bản đồ."""
    return ConflictResolver(state.static_data.walls)


class TestCompetitiveMode(unittest.TestCase):
    """
    Kiểm thử chế độ đối kháng hai agent.
    Requirement 6, 7, 8 — docs/04, mục 5.5.
    Phụ trách: Member 3.
    """

    def test_loader_reads_two_agents(self):
        """Đọc đúng vị trí hai agent, hộp và đích."""
        s = make_state()

        self.assertEqual(
            (s.agent_a_pos, s.agent_b_pos),
            ((1, 1), (1, 5))
        )
        self.assertEqual(
            s.box_positions,
            frozenset({(3, 3)})
        )

        with self.assertRaises(ValueError):
            make_state("%%%\n%A%\n%B%\n%%%\n")

    def test_vertex_collision(self):
        """Hai agent cùng đi vào một ô: cả hai đứng yên."""
        s = make_state()
        s.agent_a_pos = (2, 2)
        s.agent_b_pos = (2, 4)

        n = resolver(s).resolve(s, "East", "West")

        self.assertEqual(
            (n.agent_a_pos, n.agent_b_pos),
            ((2, 2), (2, 4))
        )

    def test_swap_collision(self):
        """Hai agent cố đi xuyên qua nhau: cả hai đứng yên."""
        s = make_state()
        s.agent_a_pos = (2, 2)
        s.agent_b_pos = (2, 3)

        n = resolver(s).resolve(s, "East", "West")

        self.assertEqual(
            (n.agent_a_pos, n.agent_b_pos),
            ((2, 2), (2, 3))
        )

    def test_cannot_walk_into_standing_opponent(self):
        """Không được đi vào ô của agent đang đứng yên."""
        s = make_state()
        s.agent_a_pos = (2, 2)
        s.agent_b_pos = (2, 3)

        n = resolver(s).resolve(s, "East", "Wait")

        self.assertEqual(
            (n.agent_a_pos, n.agent_b_pos),
            ((2, 2), (2, 3))
        )

    def test_same_box_contention(self):
        """Hai agent cùng tranh đẩy một hộp: hộp không di chuyển."""
        s = make_state()
        s.agent_a_pos = (3, 2)
        s.agent_b_pos = (3, 4)

        n = resolver(s).resolve(s, "East", "West")

        self.assertEqual(
            n.box_positions,
            frozenset({(3, 3)})
        )
        self.assertEqual(
            (n.agent_a_pos, n.agent_b_pos),
            ((3, 2), (3, 4))
        )

    def test_push_box_into_standing_opponent_blocked(self):
        """Không thể đẩy hộp vào agent đang đứng yên."""
        s = make_state()
        s.agent_a_pos = (3, 2)
        s.agent_b_pos = (3, 4)

        n = resolver(s).resolve(s, "East", "Wait")

        self.assertEqual(
            n.box_positions,
            frozenset({(3, 3)})
        )
        self.assertEqual(n.agent_a_pos, (3, 2))

    def test_push_box_into_cell_opponent_leaves(self):
        """Có thể đẩy hộp vào ô cũ của đối thủ nếu đối thủ rời đi."""
        s = make_state()
        s.agent_a_pos = (3, 2)
        s.agent_b_pos = (3, 4)

        n = resolver(s).resolve(s, "East", "North")

        self.assertEqual(
            n.box_positions,
            frozenset({(3, 4)})
        )
        self.assertEqual(
            (n.agent_a_pos, n.agent_b_pos),
            ((3, 3), (2, 4))
        )

    def test_scoring_and_box_stealing(self):
        """Đẩy hộp vào đích được điểm; đẩy hộp khỏi đích làm mất điểm."""
        s = make_state(
            "%%%%%%%\n"
            "%A   A%\n"
            "%  D  %\n"
            "% B   %\n"
            "%     %\n"
            "%%%%%%%\n"
        )

        s.box_positions = frozenset({(2, 2)})
        s.box_owners = {(2, 2): None}
        s.agent_a_pos = (2, 1)
        s.agent_b_pos = (1, 3)

        r = resolver(s)

        # Agent A đẩy hộp vào đích (2, 3).
        s1 = r.resolve(s, "East", "Wait")

        self.assertEqual((s1.score_a, s1.score_b), (1, 0))
        self.assertEqual(s1.box_owners[(2, 3)], "A")

        # Trạng thái cũ không bị thay đổi.
        self.assertEqual((s.score_a, s.current_step), (0, 0))

        # Agent B đẩy hộp ra khỏi đích.
        s2 = r.resolve(s1, "Wait", "South")

        self.assertEqual((s2.score_a, s2.score_b), (0, 0))
        self.assertEqual(
            s2.box_positions,
            frozenset({(3, 3)})
        )
        self.assertIsNone(s2.box_owners[(3, 3)])

    def test_steal_into_other_goal_changes_owner(self):
        """Agent B chiếm đích của hộp do A sở hữu."""
        s = make_state(
            "%%%%%%\n"
            "%A  A%\n"
            "%DBD %\n"
            "%%%%%%\n"
        )

        s.box_positions = frozenset({(2, 2)})
        s.box_owners = {(2, 2): "A"}
        s.agent_a_pos = (1, 1)
        s.agent_b_pos = (2, 1)
        s.score_a = 1

        n = resolver(s).resolve(s, "Wait", "East")

        self.assertEqual(
            (n.box_owners[(2, 3)], n.score_a, n.score_b),
            ("B", 0, 1)
        )

    def test_approach_is_executable_when_push_direction_changes(self):
        """
        Kế hoạch đẩy đổi hướng phải có đường tiếp cận
        và thực thi được theo luật của trò chơi.
        """
        from source.agents.pathing import Navigator

        s = make_state(
            "%%%%%%%%\n"
            "%A     %\n"
            "%      %\n"
            "% B    %\n"
            "%      %\n"
            "%     D%\n"
            "%     A%\n"
            "%%%%%%%%\n"
        )

        self.assertEqual(s.agent_b_pos, (6, 6))

        nav = Navigator(s)
        box, goal = (3, 2), (5, 6)
        pushes = nav.push_plans(box, [goal])[goal]

        self.assertIn("South", pushes)
        self.assertIn("East", pushes)

        actions = nav.approach(
            s.agent_a_pos,
            box,
            pushes,
            s.agent_b_pos
        )

        self.assertGreater(len(actions), len(pushes))

        r = resolver(s)
        cur = s

        for act in actions:
            cur = r.resolve(cur, act, "Wait")

        self.assertEqual(cur.box_positions, frozenset({goal}))
        self.assertEqual(cur.score_a, 1)

    def test_old_stub_api_is_still_available(self):
        """Các phương thức tương thích của CompetitiveState vẫn hoạt động."""
        s = make_state()

        self.assertEqual(s.get_scores(), (0, 0))
        self.assertFalse(s.is_game_over())
        self.assertEqual(s.goals, s.static_data.goals)
        self.assertEqual(
            (s.boxes_a, s.boxes_b),
            (frozenset(), frozenset())
        )

    def test_timeout_guard(self):
        """Agent vượt quá giới hạn thời gian hoặc trả action sai phải Wait."""

        class Slow:
            def get_next_action(self, state, remaining_ms):
                time.sleep(1.05)
                return "North"

        class Fast:
            def get_next_action(self, state, remaining_ms):
                return "North"

        class Broken:
            def get_next_action(self, state, remaining_ms):
                return "Fly"

        s = make_state()

        self.assertEqual(TimeoutGuard.ask(Slow(), s), "Wait")
        self.assertEqual(TimeoutGuard.ask(Fast(), s), "North")
        self.assertEqual(TimeoutGuard.ask(Broken(), s), "Wait")

    def test_agents_return_valid_actions_within_time(self):
        """Hai agent phải trả action hợp lệ trong giới hạn thời gian."""
        s = CompetitiveState.from_map_file(REAL_MAP, 100)

        for agent in (AgentA(), AgentB()):
            start = time.perf_counter()
            action = agent.get_next_action(s, 900)
            elapsed_ms = (time.perf_counter() - start) * 1000

            self.assertIn(
                action,
                ("North", "South", "East", "West", "Wait")
            )
            self.assertLess(elapsed_ms, 1000)

    def test_full_match_scores_and_is_deterministic(self):
        """Trận đấu chạy đủ lượt, có lịch sử và kết quả xác định."""

        def play():
            s = CompetitiveState.from_map_file(REAL_MAP, 120)
            engine = CompetitiveEngine(
                s,
                resolver(s),
                AgentA(),
                AgentB()
            )
            engine.run()
            return engine

        e1 = play()
        e2 = play()

        self.assertEqual(e1.state.current_step, 120)
        self.assertGreater(
            e1.state.score_a + e1.state.score_b,
            0
        )
        self.assertEqual(e1.actions, e2.actions)
        self.assertEqual(len(e1.history), 121)
        self.assertIn(
            e1.get_winner(),
            ("Agent A", "Agent B", "Tie")
        )


if __name__ == "__main__":
    unittest.main()