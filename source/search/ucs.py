import heapq
import itertools
import time
from typing import Optional

from ..core.node import SearchNode
from ..core.state import GameState, MapStaticData


class SearchResult:
    """
    Kết quả tìm kiếm chứa:
      - actions: danh sách tên hành động ('North', 'East', ...), None nếu vô nghiệm
      - total_cost: tổng chi phí đường đi
      - metrics: thời gian chạy, số node sinh ra, số node duyệt, độ lớn frontier tối đa

    Hỗ trợ unpack dạng tuple theo docs/04 Mục 3.1:
      actions, path_cost, elapsed_time_ms, nodes_expanded, nodes_generated = result
    """
    def __init__(self, actions: Optional[list[str]], total_cost: int, metrics: dict):
        self.actions = actions
        self.total_cost = total_cost
        self.metrics = metrics

    @property
    def solved(self) -> bool:
        return self.actions is not None

    def __iter__(self):
        yield self.actions
        yield self.total_cost
        yield self.metrics.get('elapsed_time_ms', 0.0)
        yield self.metrics.get('nodes_expanded', 0)
        yield self.metrics.get('nodes_generated', 0)

    def __repr__(self) -> str:
        return f"SearchResult(solved={self.solved}, total_cost={self.total_cost}, metrics={self.metrics})"


def uniform_cost_search(
    initial_state: GameState,
    static_data: MapStaticData,
    max_expanded: Optional[int] = None,
    time_limit_s: Optional[float] = None
) -> SearchResult:
    """
    Cài đặt thuật toán Uniform-Cost Search (UCS) cho Sokoban (R2).
      - Priority Queue (heapq) chứa tuple (g, counter, node); counter tránh so sánh Node khi trùng g.
      - cost_so_far: dict[GameState, int] lưu chi phí tốt nhất đã biết, bỏ qua bản sao lỗi thời.
      - Goal test khi node được lấy ra khỏi hàng đợi => đảm bảo tối ưu.
      - max_expanded / time_limit_s: giới hạn an toàn cho bản đồ lớn (None = không giới hạn).
    """
    start_time = time.perf_counter()
    counter = itertools.count()

    start_node = SearchNode(state=initial_state, parent=None, action=None, g=0)
    frontier = [(0, next(counter), start_node)]
    cost_so_far: dict[GameState, int] = {initial_state: 0}

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    status = 'no_solution'

    while frontier:
        g, _, current_node = heapq.heappop(frontier)

        # Bản sao lỗi thời: đã có đường đi rẻ hơn tới state này
        if g > cost_so_far[current_node.state]:
            continue

        if current_node.state.is_goal(static_data):
            return _build_result(
                current_node.reconstruct_actions(), g, 'solved', start_time,
                nodes_expanded, nodes_generated, max_frontier_size, len(cost_so_far)
            )

        if max_expanded is not None and nodes_expanded >= max_expanded:
            status = 'limit_reached'
            break
        if time_limit_s is not None and time.perf_counter() - start_time >= time_limit_s:
            status = 'timeout'
            break

        nodes_expanded += 1

        for action, next_state, step_cost in current_node.state.get_successors(static_data):
            next_g = g + step_cost
            if next_g < cost_so_far.get(next_state, float('inf')):
                cost_so_far[next_state] = next_g
                child_node = SearchNode(state=next_state, parent=current_node, action=action, g=next_g)
                heapq.heappush(frontier, (next_g, next(counter), child_node))
                nodes_generated += 1

        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)

    return _build_result(
        None, 0, status, start_time,
        nodes_expanded, nodes_generated, max_frontier_size, len(cost_so_far)
    )


def _build_result(
    actions: Optional[list[str]],
    total_cost: int,
    status: str,
    start_time: float,
    nodes_expanded: int,
    nodes_generated: int,
    max_frontier_size: int,
    states_reached: int
) -> SearchResult:
    metrics = {
        'algorithm': 'UCS',
        'status': status,
        'elapsed_time_ms': (time.perf_counter() - start_time) * 1000.0,
        'nodes_expanded': nodes_expanded,
        'nodes_generated': nodes_generated,
        'max_frontier_size': max_frontier_size,
        'states_reached': states_reached,
    }
    return SearchResult(actions, total_cost, metrics)


if __name__ == "__main__":
    # Chạy nhanh: python -m source.search.ucs source/maps/map_02.txt [max_expanded]
    import sys
    from ..core.parser import parse_map_file

    map_path = sys.argv[1] if len(sys.argv) > 1 else "source/maps/example_map.txt"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    state, static = parse_map_file(map_path)
    result = uniform_cost_search(state, static, max_expanded=limit)
    print(f"Map: {map_path}")
    for key, value in result.metrics.items():
        print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
    if result.solved:
        print(f"  total_cost: {result.total_cost}")
        print(f"  actions: {' '.join(result.actions)}")
