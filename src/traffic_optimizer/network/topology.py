from collections import deque
from dataclasses import dataclass
import heapq
from enum import Enum


class RoutingAlgorithm(str, Enum):
    BFS = "BFS"
    DJIKSTRAS = "DJIKSTRAS"


@dataclass
class Topology:
    def shortest_path(
        self,
        origin: tuple[int],
        destination: tuple[int],
        rows: int,
        cols: int,
        grid_weights: list[list[float]],
        routing_algorithm: RoutingAlgorithm = RoutingAlgorithm.DJIKSTRAS
    ) -> list[tuple[int]]:
        return self.shortest_path_djikstra(
            origin=origin,
            destination=destination,
            rows=rows,
            cols=cols,
            grid_weights=grid_weights,
        )


    def shortest_path_bfs(
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

    def shortest_path_djikstra(
        self,
        origin: tuple[int],
        destination: tuple[int],
        rows: int,
        cols: int,
        grid_weights: list[list[float]],
    ) -> list[tuple[int]]:
        """
        Use Djikstra's to generate the shortest path between origin and destination
        Params:
            origin: list of ints representing [row, col] in 2d grid map
            destination: list of ints representing [row, col] in 2d grid map
            grid_weights: 2D array of shapes (rows, cols) containing edge/cell weights
        Returns:
            List of vertices to optimally traverse between the nodes
        """
        if origin == destination:
            return [origin]

        pq = [(0, origin)]
        distances = {origin: 0}
        parent_map = {origin: None}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_node == destination:
                break

            if current_dist > distances.get(current_node, float('inf')):
                continue

            r, c = current_node

            for dr, dc in directions:
                neighbor = (r + dr, c + dc)
                nr, nc = neighbor

                # Check grid boundaries
                if 0 <= nr < rows and 0 <= nc < cols:

                    # 2. Use the destination cell's weight instead of a static value of 1
                    edge_weight = grid_weights[nr][nc]
                    new_dist = current_dist + edge_weight

                    # Relaxation step
                    if new_dist < distances.get(neighbor, float('inf')):
                        distances[neighbor] = new_dist
                        parent_map[neighbor] = current_node
                        heapq.heappush(pq, (new_dist, neighbor))

        if destination not in parent_map:
            return []

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
