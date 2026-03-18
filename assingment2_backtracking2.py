from collections import deque
from itertools import combinations

class Assign:
    def __init__(self, preferences, places):
        self.n = len(preferences)  # Number of participants
        self.m = len(places)  # Number of activities
        self.preferences = preferences
        self.places = places
        self.source = self.n + self.m  # Virtual source node
        self.sink = self.n + self.m + 1  # Virtual sink node
        self.V = self.n + self.m + 2  # Total number of vertices (participants + activities + source + sink)
        self.capacity = [[0] * self.V for _ in range(self.V)]
        self.flow = [[0] * self.V for _ in range(self.V)]
        self.assignments = [[] for _ in range(self.m)]
        self.leader_assigned = [False] * self.n  # Track participants who are leaders

        print(f"Initialized Assign with {self.n} participants and {self.m} activities")

    def build_flow_graph(self):
        """
        Builds a flow network from participants to activities.
        Leaders are participants with preference 2.
        """
        print("Building flow graph...")

        # Connect source to participants
        for i in range(self.n):
            if not self.leader_assigned[i]:  # Only non-leaders can be connected for flow assignment
                self.capacity[self.source][i] = 1
                print(f"Connected source to participant {i}")

        # Connect participants to activities based on their preferences
        for i in range(self.n):
            for j in range(self.m):
                if self.preferences[i][j] > 0 and not self.leader_assigned[i]:  # Non-leaders only
                    self.capacity[i][self.n + j] = 1
                    print(f"Connected participant {i} to activity {j}")

        # Connect activities to the sink
        for j in range(self.m):
            available_places = self.places[j] - 2  # Reserve 2 places for leaders
            if available_places > 0:
                self.capacity[self.n + j][self.sink] = available_places
                print(f"Connected activity {j} to sink with {available_places} places")

    def bfs(self, parent):
        """
        Perform BFS to find an augmenting path.
        """
        print("Starting BFS...")
        visited = [False] * self.V
        queue = deque([self.source])
        visited[self.source] = True

        while queue:
            u = queue.popleft()
            for v in range(self.V):
                if not visited[v] and self.capacity[u][v] - self.flow[u][v] > 0:  # Residual capacity
                    parent[v] = u
                    if v == self.sink:
                        print("Found augmenting path to sink")
                        return True
                    queue.append(v)
                    visited[v] = True
        print("No augmenting path found")
        return False

    def edmonds_karp(self):
        """
        Implement Edmonds-Karp to find maximum flow.
        """
        parent = [-1] * self.V
        max_flow = 0

        print("Running Edmonds-Karp...")

        while self.bfs(parent):
            # Find the minimum residual capacity of the augmenting path
            path_flow = float('Inf')
            s = self.sink
            while s != self.source:
                path_flow = min(path_flow, self.capacity[parent[s]][s] - self.flow[parent[s]][s])
                s = parent[s]

            print(f"Augmenting path flow: {path_flow}")

            # Update flow
            v = self.sink
            while v != self.source:
                u = parent[v]
                self.flow[u][v] += path_flow
                self.flow[v][u] -= path_flow
                v = parent[v]

            max_flow += path_flow
            print(f"Current max flow: {max_flow}")

        return max_flow

    def try_leader_assignments(self, activity_idx):
        """
        Try all possible leader assignments for the given activity using backtracking.
        """
        print(f"Trying to assign leaders for activity {activity_idx}")

        if activity_idx == self.m:
            print("Successfully assigned leaders to all activities")
            return True  # Successfully assigned leaders to all activities

        leaders = [i for i in range(self.n) if self.preferences[i][activity_idx] == 2 and not self.leader_assigned[i]]
        print(f"Leaders available for activity {activity_idx}: {leaders}")
        
        if len(leaders) < 2:
            print(f"Not enough leaders for activity {activity_idx}")
            return False

        # Try all pairs of leaders for this activity
        for leader_pair in combinations(leaders, 2):
            print(f"Trying leaders {leader_pair} for activity {activity_idx}")
            self.leader_assigned[leader_pair[0]] = True
            self.leader_assigned[leader_pair[1]] = True
            self.assignments[activity_idx].extend(leader_pair)

            # Recurse to try assigning leaders to the next activity
            if self.try_leader_assignments(activity_idx + 1):
                return True

            # Backtrack: Remove the leaders properly from assignments
            print(f"Backtracking from leaders {leader_pair}")
            self.leader_assigned[leader_pair[0]] = False
            self.leader_assigned[leader_pair[1]] = False
            self.assignments[activity_idx].remove(leader_pair[0])
            self.assignments[activity_idx].remove(leader_pair[1])

        return False

    def assign_activities(self):
        """
        Main method to assign participants and leaders using backtracking for leader assignment,
        and Edmonds-Karp for participant assignment.
        """
        print("Starting assignment process...")

        # First, try assigning leaders using backtracking
        if not self.try_leader_assignments(0):
            print("Failed to assign leaders")
            return None

        print("Leaders successfully assigned. Building flow graph for participants...")
        self.build_flow_graph()

        # Run Edmonds-Karp to assign the remaining participants
        max_flow = self.edmonds_karp()
        print(f"Max flow after Edmonds-Karp: {max_flow}")

        # Extract assignments based on the flow matrix
        for i in range(self.n):
            for j in range(self.m):
                if self.flow[i][self.n + j] == 1:  # Participant i assigned to activity j
                    self.assignments[j].append(i)
                    print(f"Participant {i} assigned to activity {j}")

        print("Final assignments:", self.assignments)
        return self.assignments

def assign(preferences, places):
    """
    This is the function that creates an instance of the Assign class and returns the 
    assignments of participants and leaders to activities.
    """
    assignment = Assign(preferences, places)
    return assignment.assign_activities()
