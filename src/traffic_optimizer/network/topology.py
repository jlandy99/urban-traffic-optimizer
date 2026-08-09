from collections import deque
from dataclasses import dataclass


@dataclass
class Topology:
    def shortest_path(
        self,
        origin: tuple[int],
        destination: tuple[int],
        rows: int,
        cols: int,
    ) -> list[tuple[int]]:
        """
        Use BFS to generate the shortest path between origin and destination
        Params:
            origin: list of ints representing [row, col] in 2d grid map
            destination: list of ints representing [row, col] in 2d grid map
        Returns:
            List of vertices to optimally traverse between the nodes
        """

        if origin == destination:
            return [origin]

        queue = deque([origin])
        parent_map = {origin: None}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            curr = queue.popleft()
            if curr == destination:
                break

            r, c = curr
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                neighbor = (nr, nc)

                # Boundary check and visited check combined
                if 0 <= nr < rows and 0 <= nc < cols and neighbor not in parent_map:
                    parent_map[neighbor] = curr
                    queue.append(neighbor)

        # Reconstruct path
        if destination not in parent_map:
            return None

        path = []
        curr = destination
        while curr is not None:
            path.append(curr)
            curr = parent_map[curr]
        return path[::-1]

    def path_to_sumo_edges(
        self,
        path: list[tuple[int]],
    ) -> list[str]:
        """
        Converts a list of vertices into a list of edges, such that
        it can be consumed by SUMO in routing
        Params:
            path: list of tuples representing row, col vertices in the map
        Returns:
            List of strings representing directional edges in the graph
        """
        sumo_edges = []
        for idx in range(len(path) - 1):
            row = path[idx][0]
            col = path[idx][1]
            # If row doesn't change, we're moving east / west
            if path[idx][0] == path[idx + 1][0]:
                # If col increases, we are moving east, otherwise west
                if path[idx][1] < path[idx + 1][1]:
                    sumo_edges.append(f"east_{row}_{col}")
                else:
                    sumo_edges.append(f"west_{row}_{col}")
            else:
                # If row increases, we are moving south, otherwise north
                if path[idx][0] < path[idx + 1][0]:
                    sumo_edges.append(f"south_{row}_{col}")
                else:
                    sumo_edges.append(f"north_{row}_{col}")

        return sumo_edges
