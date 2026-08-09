from collections import deque
from dataclasses import dataclass
import heapq

@dataclass
class Topology:
    def shortest_path(
        self,
        origin: tuple[int],
        destination: tuple[int],
        rows: int,
        cols: int,
    ) -> list[tuple[int]]:
        # For now, we default to Djikstra's
        return self.shortest_path_djikstra(
            origin=origin,
            destination=destination,
            rows=rows,
            cols=cols,
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
    ) -> list[tuple[int]]:
        """
        Use Djikstra's to generate the shortest path between origin and destination
        Params:
            origin: list of ints representing [row, col] in 2d grid map
            destination: list of ints representing [row, col] in 2d grid map
        Returns:
            List of vertices to optimally traverse between the nodes
        """
        # 1. Edge case: origin is the destination
        if origin == destination:
            return [origin]

        # 2. Priority queue stores tuples of (distance, current_node)
        # Priority queue starts with the origin at a distance of 0
        pq = [(0, origin)]

        # Track minimum distance to each cell
        distances = {origin: 0}

        # Track the parent pointers to reconstruct the final path
        parent_map = {origin: None}

        # Direction vectors for moving Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # 3. Main Loop
        while pq:
            current_dist, current_node = heapq.heappop(pq)

            # Early exit if we reached the destination
            if current_node == destination:
                break

            # If we found a longer path to an already processed node, skip it
            if current_dist > distances.get(current_node, float('inf')):
                continue

            r, c = current_node

            # 4. Explore Neighbors
            for dr, dc in directions:
                neighbor = (r + dr, c + dc)
                nr, nc = neighbor

                # Check boundaries of the rows x cols grid
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Assume a standard uniform grid weight of 1 per step
                    new_dist = current_dist + 1

                    # Relaxation step
                    if new_dist < distances.get(neighbor, float('inf')):
                        distances[neighbor] = new_dist
                        parent_map[neighbor] = current_node
                        heapq.heappush(pq, (new_dist, neighbor))

        # 5. Path Reconstruction
        if destination not in parent_map:
            return []  # Return empty list if destination is unreachable

        path = []
        curr = destination
        while curr is not None:
            path.append(curr)
            curr = parent_map[curr]

        # Reverse path so it goes from origin -> destination
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
