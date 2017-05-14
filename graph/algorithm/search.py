from collections import deque
from typing import Set, Callable, TypeVar, Optional, Any

from graph import Graph, Vertex

Test = Callable[[Vertex], bool]


def dfs(g: Graph, current: Vertex, condition: Test,
        visited: Set = None) -> Optional[Vertex]:

    visited = visited or set()

    if current in visited:
        return None

    visited.add(current)

    if condition(current):
        return current

    for n in g.neighbors(current):
        v = dfs(g, n, condition, visited)

        if v is not None:
            return v

    return None


def bfs(g: Graph, start: Vertex,
        condition: Test) -> Optional[Vertex]:
    deq = deque()  # type: Any
    visited = set()

    deq.append(start)
    visited.add(start)

    while len(deq) > 0:
        cur = deq.popleft()

        if condition(cur):
            return cur

        for n in g.neighbors(cur):
            if n not in visited:
                deq.append(n)
                visited.add(n)

    return None
