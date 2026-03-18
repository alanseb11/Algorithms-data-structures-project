from collections import deque

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

    def backtrack_leader_swap(self, participant_idx):
        """
        Backtracking function to attempt all possible swaps of leaders to resolve conflicts.
        Tries promoting participants to leaders and backtracks if the swap fails.
        """
        # If we've tried all participants, return success (base case)
        if participant_idx == self.n:
            return True

        # Only consider participants who are not already leaders
        if not self.leader_assigned[participant_idx]:
            for j in range(self.m):
                if self.preferences[participant_idx][j] == 2:  # Participant can lead activity j
                    # Try swapping this participant with current leaders in activity j
                    for leader in self.assignments[j]:
                        # Perform the swap: promote the participant to leader, demote the current leader
                        print(f"Attempting swap: Participant {participant_idx} as leader of activity {j}, replacing leader {leader}")
                        self.leader_assigned[leader] = False
                        self.leader_assigned[participant_idx] = True
                        self.assignments[j].remove(leader)
                        self.assignments[j].append(participant_idx)

                        # Recurse to see if this swap leads to a valid solution
                        if self.backtrack_leader_swap(participant_idx + 1):
                            return True  # Successful configuration

                        # Backtrack if this swap does not work
                        print(f"Backtracking: Undoing swap of participant {participant_idx} with leader {leader}")
                        self.leader_assigned[participant_idx] = False
                        self.leader_assigned[leader] = True
                        self.assignments[j].remove(participant_idx)
                        self.assignments[j].append(leader)

        # If no valid swap was found, return False (backtracking step)
        return False

    def greedy_leader_assignment(self):
        """
        Greedily assign leaders to each activity.
        Leaders are participants with preference 2.
        """
        print("Assigning leaders...")
        for j in range(self.m):  # For each activity
            leaders = [i for i in range(self.n) if self.preferences[i][j] == 2 and not self.leader_assigned[i]]
            if len(leaders) >= 2:  # At least 2 leaders available
                self.leader_assigned[leaders[0]] = True
                self.leader_assigned[leaders[1]] = True
                self.assignments[j].extend([leaders[0], leaders[1]])
                print(f"Assigned leaders {leaders[0]} and {leaders[1]} to activity {j}")
            else:
                print(f"Failed to assign 2 leaders for activity {j}")
                return False  # Not enough leaders for this activity
        return True

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

        # Connect activities to the sink, subtracting leader spots
        for j in range(self.m):
            available_places = self.places[j] - 2  # Reserve 2 places for leaders
            if available_places > 0:
                self.capacity[self.n + j][self.sink] = available_places
                print(f"Connected activity {j} to sink with {available_places} places")

    def bfs(self, parent):
        """
        Perform BFS to find an augmenting path in the residual graph.
        Returns True if a path from source to sink is found.
        """
        visited = [False] * self.V
        queue = deque([self.source])
        visited[self.source] = True

        while queue:
            u = queue.popleft()
            for v in range(self.V):
                # Check if there is residual capacity and the vertex has not been visited yet
                if not visited[v] and self.capacity[u][v] - self.flow[u][v] > 0:
                    parent[v] = u  # Track the path
                    if v == self.sink:  # If sink is reached, we found an augmenting path
                        return True
                    queue.append(v)
                    visited[v] = True
        return False

    def ford_fulkerson(self):
        """
        Implement Ford-Fulkerson to find maximum flow using BFS.
        """
        parent = [-1] * self.V
        max_flow = 0

        # Augment the flow while there is an augmenting path
        while self.bfs(parent):
            # Find the maximum flow through the path found by BFS
            path_flow = float('Inf')
            s = self.sink
            while s != self.source:
                path_flow = min(path_flow, self.capacity[parent[s]][s] - self.flow[parent[s]][s])
                s = parent[s]

            # Update residual capacities of the edges and reverse edges along the path
            v = self.sink
            while v != self.source:
                u = parent[v]
                self.flow[u][v] += path_flow
                self.flow[v][u] -= path_flow
                v = parent[v]

            max_flow += path_flow
            print(f"Augmented path with flow {path_flow}. Current max flow: {max_flow}")

        return max_flow

    def assign_activities(self):
        """
        Main method to assign participants and leaders using greedy leader assignment,
        leader reassignment for conflicts, and Ford-Fulkerson for participant assignment.
        """
        print("Starting assignment process...")

        # First, try assigning leaders using the greedy approach
        if not self.greedy_leader_assignment():
            print("Failed to assign leaders")
            return None

        print("Leaders successfully assigned. Building flow graph for participants...")
        self.build_flow_graph()

        # Run Ford-Fulkerson to assign the remaining participants
        max_flow = self.ford_fulkerson()
        print(f"Max flow after Ford-Fulkerson: {max_flow}")

        # If max flow doesn't assign enough participants, try backtracking to swap leaders
        for j in range(self.m):
            if len(self.assignments[j]) < self.places[j]:
                print(f"Not enough participants assigned to activity {j}. Starting backtracking.")
                if not self.backtrack_leader_swap(0):
                    print("Unable to reassign leaders to accommodate all participants.")
                    return None  # If leader reassignment fails, return None

        print("Final assignments:", self.assignments)
        return self.assignments

def assign(preferences, places):
    """
    This is the function that creates an instance of the Assign class and returns the 
    assignments of participants and leaders to activities.
    """
    assignment = Assign(preferences, places)
    return assignment.assign_activities()
