import os
import sys
<<<<<<< HEAD
import tempfile
import time
=======
>>>>>>> origin/main
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

<<<<<<< HEAD
from source.agents.agent_a import AgentA
from source.agents.agent_b import AgentB
from source.competitive.conflict import ConflictResolver
from source.competitive.engine import CompetitiveEngine, TimeoutGuard
from source.competitive.state import CompetitiveState

# Hàng 1: A ở (1,1), B ở (1,5). Hộp ở (3,3); goal ở (3,5), (3,1).
MAP = """%%%%%%%
%A   A%
%     %
%D B D%
%%%%%%%
"""
REAL_MAP = os.path.join(os.path.dirname(__file__), "..", "maps", "competitive_map.txt")


def make_state(text=MAP, steps=50):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(text)
    try:
        return CompetitiveState.from_map_file(f.name, steps)
    finally:
        os.remove(f.name)


def resolver(state):
    return ConflictResolver(state.static_data.walls)


class TestCompetitiveMode(unittest.TestCase):
    """Bộ kiểm thử chế độ đối kháng (Requirement 6, 7 & 8, docs/04 mục 5.5). Phụ trách: Member 3."""

    def test_loader_reads_two_agents(self):
        s = make_state()
        self.assertEqual((s.agent_a_pos, s.agent_b_pos), ((1, 1), (1, 5)))
        self.assertEqual(s.box_positions, frozenset({(3, 3)}))
        with self.assertRaises(ValueError):
            make_state("%%%\n%A%\n%B%\n%%%\n")

    def test_vertex_collision(self):
        """Hai Agent cùng đi vào 1 ô -> cả hai đứng yên."""
        s = make_state()
        s.agent_a_pos, s.agent_b_pos = (2, 2), (2, 4)
        n = resolver(s).resolve(s, "East", "West")
        self.assertEqual((n.agent_a_pos, n.agent_b_pos), ((2, 2), (2, 4)))

    def test_swap_collision(self):
        """Hai Agent cố đi xuyên qua nhau -> cả hai đứng yên."""
        s = make_state()
        s.agent_a_pos, s.agent_b_pos = (2, 2), (2, 3)
        n = resolver(s).resolve(s, "East", "West")
        self.assertEqual((n.agent_a_pos, n.agent_b_pos), ((2, 2), (2, 3)))

    def test_cannot_walk_into_standing_opponent(self):
        s = make_state()
        s.agent_a_pos, s.agent_b_pos = (2, 2), (2, 3)
        n = resolver(s).resolve(s, "East", "Wait")
        self.assertEqual((n.agent_a_pos, n.agent_b_pos), ((2, 2), (2, 3)))

    def test_same_box_contention(self):
        """Hai Agent cùng đẩy 1 hộp từ hai phía -> hộp đứng yên."""
        s = make_state()
        s.agent_a_pos, s.agent_b_pos = (3, 2), (3, 4)
        n = resolver(s).resolve(s, "East", "West")
        self.assertEqual(n.box_positions, frozenset({(3, 3)}))
        self.assertEqual((n.agent_a_pos, n.agent_b_pos), ((3, 2), (3, 4)))

    def test_push_box_into_standing_opponent_blocked(self):
        s = make_state()
        s.agent_a_pos, s.agent_b_pos = (3, 2), (3, 4)
        n = resolver(s).resolve(s, "East", "Wait")
        self.assertEqual(n.box_positions, frozenset({(3, 3)}))
        self.assertEqual(n.agent_a_pos, (3, 2))

    def test_push_box_into_cell_opponent_leaves(self):
        s = make_state()
        s.agent_a_pos, s.agent_b_pos = (3, 2), (3, 4)
        n = resolver(s).resolve(s, "East", "North")
        self.assertEqual(n.box_positions, frozenset({(3, 4)}))
        self.assertEqual((n.agent_a_pos, n.agent_b_pos), ((3, 3), (2, 4)))

    def test_scoring_and_box_stealing(self):
        """A đẩy hộp vào goal -> A +1; B đẩy hộp ra khỏi goal -> A -1."""
        s = make_state("%%%%%%%\n%A   A%\n%  D  %\n% B   %\n%     %\n%%%%%%%\n")
        s.box_positions, s.box_owners = frozenset({(2, 2)}), {(2, 2): None}
        s.agent_a_pos, s.agent_b_pos = (2, 1), (1, 3)
        r = resolver(s)
        s1 = r.resolve(s, "East", "Wait")                 # A đẩy hộp vào goal (2,3)
        self.assertEqual((s1.score_a, s1.score_b), (1, 0))
        self.assertEqual(s1.box_owners[(2, 3)], "A")
        self.assertEqual((s.score_a, s.current_step), (0, 0))   # state cũ không bị sửa
        s2 = r.resolve(s1, "Wait", "South")               # B đẩy hộp ra khỏi goal
        self.assertEqual((s2.score_a, s2.score_b), (0, 0))
        self.assertEqual(s2.box_positions, frozenset({(3, 3)}))
        self.assertIsNone(s2.box_owners[(3, 3)])

    def test_steal_into_other_goal_changes_owner(self):
        s = make_state("%%%%%%\n%A  A%\n%DBD %\n%%%%%%\n")
        s.box_positions, s.box_owners = frozenset({(2, 2)}), {(2, 2): "A"}
        s.agent_a_pos, s.agent_b_pos = (1, 1), (2, 1)
        s.score_a = 1
        n = ConflictResolver(s.static_data.walls).resolve(s, "Wait", "East")
        self.assertEqual((n.box_owners[(2, 3)], n.score_a, n.score_b), ("B", 0, 1))

    def test_approach_is_executable_when_push_direction_changes(self):
        """Kế hoạch đẩy có đổi hướng (East rồi South) phải chèn đoạn đi vòng và chạy được thật."""
        from source.agents.pathing import Navigator
        s = make_state("%%%%%%%%\n%A     %\n%      %\n% B    %\n%      %\n%     D%\n%     A%\n%%%%%%%%\n")
        assert s.agent_b_pos == (6, 6)   # B đứng xa, không cản đường
        nav = Navigator(s)
        box, goal = (3, 2), (5, 6)
        pushes = nav.push_plans(box, [goal])[goal]
        self.assertIn("South", pushes)
        self.assertIn("East", pushes)
        actions = nav.approach(s.agent_a_pos, box, pushes, s.agent_b_pos)
        self.assertGreater(len(actions), len(pushes))            # có đoạn đi vòng chèn thêm
        r, cur = resolver(s), s
        for act in actions:                                       # mô phỏng bằng luật thật
            cur = r.resolve(cur, act, "Wait")
        self.assertEqual(cur.box_positions, frozenset({goal}))
        self.assertEqual(cur.score_a, 1)

    def test_old_stub_api_is_still_available(self):
        s = make_state()
        self.assertEqual(s.get_scores(), (0, 0))
        self.assertFalse(s.is_game_over())
        self.assertEqual(s.goals, s.static_data.goals)
        self.assertEqual((s.boxes_a, s.boxes_b), (frozenset(), frozenset()))

    def test_timeout_guard(self):
        """Agent chạy quá 1000 ms -> bị thay bằng 'Wait'."""
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
        s = CompetitiveState.from_map_file(REAL_MAP, 100)
        for agent, in ((AgentA(),), (AgentB(),)):
            t = time.perf_counter()
            action = agent.get_next_action(s, 900)
            self.assertIn(action, ("North", "South", "East", "West", "Wait"))
            self.assertLess((time.perf_counter() - t) * 1000, 1000)

    def test_full_match_scores_and_is_deterministic(self):
        def play():
            s = CompetitiveState.from_map_file(REAL_MAP, 120)
            e = CompetitiveEngine(s, resolver(s), AgentA(), AgentB())
            e.run()
            return e
        e1, e2 = play(), play()
        self.assertEqual(e1.state.current_step, 120)
        self.assertGreater(e1.state.score_a + e1.state.score_b, 0)
        self.assertEqual(e1.actions, e2.actions)
        self.assertEqual(len(e1.history), 121)
        self.assertIn(e1.get_winner(), ("Agent A", "Agent B", "Tie"))
=======

class TestCompetitiveMode(unittest.TestCase):
    """
    Bộ kiểm thử cho Chế độ Đối kháng 2 Agent & Phân xử Xung đột (Requirement 6, 7 & 8, docs/04 Mục 5.5).
    Phụ trách: Member 3.
    Lộ trình thực hiện: Ngày 8-10 (Tuần 2).
    """

    def test_vertex_collision(self):
        """Hai Agent cùng đi vào 1 ô -> Cả hai đứng yên tại chỗ."""
        self.assertTrue(True)

    def test_swap_collision(self):
        """Hai Agent cố đi xuyên qua nhau -> Cả hai đứng yên."""
        self.assertTrue(True)

    def test_box_stealing(self):
        """Agent B đẩy hộp của Agent A ra khỏi đích -> Điểm của A bị trừ 1."""
        self.assertTrue(True)

    def test_timeout_guard(self):
        """Agent chạy quá 1,000 ms bị ngắt an toàn và trả về 'Wait'."""
        self.assertTrue(True)
>>>>>>> origin/main


if __name__ == "__main__":
    unittest.main()
