# Member 2: Heuristic and A* Search

This note answers the assigned research questions and provides draft content for Slides 4–6. Replace every bracketed result with measurements from the final benchmark; do not present placeholder values as experimental results.

## Research Notes

### Admissibility and Optimality

A heuristic is admissible when it never overestimates the true cheapest remaining cost: $0 \le h(n) \le h^*(n)$. With nonnegative step costs, A* orders the frontier by $f(n)=g(n)+h(n)$. Before a more expensive goal could be selected, some frontier node on an optimal route has an $f$-value no greater than the optimal solution cost. Thus, when A* removes a goal from the priority queue, that goal has optimal path cost. This relies on an admissible heuristic and correct handling of improved paths; this implementation permits improved paths through its `g_score` table and stale-entry check.

If $h(n)>h^*(n)$, that lower-bound argument fails. A* may prioritize a suboptimal route and is no longer guaranteed to return an optimal solution.

### Consistency

A heuristic is consistent when every legal transition from $n$ to $n'$ satisfies $h(n) \le c(n,a,n')+h(n')$, with $h(goal)=0$. This is a triangle-inequality condition: estimated remaining cost cannot drop by more than the cost of the action. It makes $f$ nondecreasing along a path. Consequently, graph-search A* can permanently close an expanded node without reopening it. This implementation instead tracks the best known `g_score` and supports improved paths directly.

For the implemented heuristic, walking without pushing leaves all box positions unchanged, so $h$ is unchanged. A push moves one box to an adjacent non-wall cell. Its maze distance to any fixed goal can change by at most one; keeping the other box-to-goal assignments fixed therefore shows that the minimum matching cost can decrease by at most the push cost of one.

### Heuristic Design

For each goal, BFS computes shortest-path distances over floor cells while treating other boxes as absent. Let $d(b,g)$ be the resulting maze distance. The heuristic is the minimum-cost one-to-one assignment of boxes to distinct goals:

$$h(s)=\min_{\pi}\sum_{i=1}^{k} d(b_i,g_{\pi(i)}).$$

The assignment is computed with the Hungarian algorithm through `scipy.optimize.linear_sum_assignment`. A nearest-goal sum is weaker because several boxes can all choose the same goal, effectively using one goal multiple times. One-to-one matching avoids that underestimate caused by goal reuse.

Manhattan distance can pass through walls and ignores the map's corridors. Maze distance respects static walls. It is still optimistic for Sokoban: it ignores other boxes and whether the player can stand behind a box to push it. Every real solution must move each box to a distinct goal, and each push costs at least one action, so the summed assignment distance is a lower bound on the real remaining action cost.

### Deadlocks

A box in a non-goal corner, where one vertical neighbor and one horizontal neighbor are walls or outside the map, cannot be moved out. The heuristic returns infinity for such states, and A* prunes them before adding them to the frontier. A box on a goal is not classified as a corner deadlock. This is a sound but intentionally limited detector: it does not detect every freeze, tunnel, or box-to-box deadlock.

### Empirical Checks

For each solvable sample state, UCS gives the exact remaining cost $h^*(n)$; compare it with $h(n)$ and count violations of $h(n) \le h^*(n)$. States for which UCS finds no solution must be counted separately, not treated as having cost zero. For consistency, check every sampled legal transition against $h(n) \le c(n,a,n')+h(n')$.

These checks provide evidence for the tested states and transitions; finite experiments do not prove the property for every possible Sokoban state. The proof sketches above establish why the selected heuristic has the properties, subject to the movement and cost model in the project.

## Slide Draft (4:3, No Raw Source Code)

### Slide 4: Heuristic for Sokoban

- BFS on static floor cells gives maze distances from each goal.
- Hungarian matching assigns each box to a distinct goal with minimum total distance.
- Non-goal corner boxes are deadlocks and are pruned with $h=\infty$.
- Strength: accounts for walls and goal competition. Limitation: ignores box blocking and player push access.
- Visual: a small box-to-goal cost matrix with the chosen one-to-one assignment; mark one non-goal corner as deadlocked.

### Slide 5: Admissible and Consistent

- Admissible means $h(n) \le h^*(n)$; it preserves A* optimality.
- Consistent means $h(n) \le c(n,a,n')+h(n')$; the estimate cannot drop by more than one action cost.
- The heuristic ignores constraints that can only make the real puzzle harder, so its assignment distance is a lower bound.
- Evidence table: `Map | Solvable samples | Admissibility violations | Transitions checked | Consistency violations`.
- Fill the table with actual output from `verify_admissibility` and `verify_consistency`.

### Slide 6: A* Search

- A* selects the frontier state with the lowest $f(n)=g(n)+h(n)$.
- $g(n)$ is the cost already paid; $h(n)$ estimates the remaining cost.
- UCS is the special case $h(n)=0$. A useful admissible heuristic can reduce expansions while retaining optimal cost.
- Results table: `Algorithm | Solution cost | Expanded nodes | Runtime (ms)` for UCS and A* on the same maps.
- Only claim measured speedups or node reductions when the benchmark confirms them.

## 90-Second Speaking Draft

"Ở phần tìm kiếm có thông tin, nhóm dùng khoảng cách mê cung thay vì Manhattan vì Manhattan có thể đi xuyên tường. BFS tính khoảng cách trên sàn cho từng đích, sau đó thuật toán Hungarian ghép mỗi hộp với một đích khác nhau để giảm tổng chi phí ước lượng. Cách ghép này tránh việc nhiều hộp cùng chọn một đích gần nhất. Heuristic vẫn là cận dưới vì phép tính bỏ qua các hộp chắn đường và điều kiện người chơi phải đứng phía sau để đẩy; các ràng buộc bị bỏ qua chỉ làm bài toán thực tế khó hơn. Hộp ở góc tường mà không nằm trên đích được nhận diện là deadlock và nhánh đó bị loại. Admissible nghĩa là heuristic không vượt quá chi phí tối ưu còn lại, nhờ vậy A* vẫn giữ lời giải tối ưu. Consistent nghĩa là ước lượng không giảm nhiều hơn chi phí của một bước. Cuối cùng, nhóm đối chiếu A* với UCS trên cùng bản đồ: UCS cho chi phí chuẩn, còn số node mở rộng và thời gian sẽ được báo cáo theo kết quả benchmark thực tế."