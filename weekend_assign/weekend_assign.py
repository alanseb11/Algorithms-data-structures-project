from collections import deque
from typing import List, Optional, Tuple


class Assign:
    def __init__(self, preferences: List[List[int]], places: List[int]) -> None:
        """
        Function Description: Initialises the Assign class with inputs of preferences and activity capacities

        Approach Description:
        -Finds and initialises the number of participants denoted by n and activities by m
        -Sets up total number of activity nodes (2 times the number of activities to account for leaders and non-leaders), the source and the sink for the flow graph
        -Initializes the capacity matrix to track the graph capacity and flow matricies to track the flow at each edge
        -Initializes an assignment list that stores the final participant to activity assignments which is what will be used for the final output

        Input:
        - preferences: A list in which preferences[i][j] represents the interest level of participant i in activity j.
            This is denoted through the numbers 0, 1 and 2 which represent no interest, interest but no experience and interested with experience respectively
        -  capacity: A list where capacity[j] represents the number of participants allowed in activity j

        Output: None

        Time Complexity: O((n + m)^2) where n is the number of participants and m is the number of activities

        Time Complexity Analysis:
        - Finding the number of participants and activities only has O(1) compleixty
        - Initializing the capacity and flow matrices requires creating two V x V matricies where V = 2 + n + 2*m (number of participants, activities and the source and sink nodes)
        - The time complexity for initializing each matrix is O(V^2) as a result which is therefore O((n + 2m)^2) which simplifies to O((n + m)^2)
        - Creating the assignment list takes O(m) because it initializes an empty list for each activity.
        -Therefore, the overall complexity is dominated by O((n + m)^2) for the __init__ method.

        Space Complexity: O((n + m)^2) dominated by the capacities and flow matrices and n is the number of participants and m is the number of activities

        Space Complexity Analysis:
        - self.n and self.m are integers that take up O(1) space
        - self.preferences is a list of lists that has a complexity of O(n *m)
        - self.places is a list with m elements meaning that it has a complextiy of O(m)
        - self.capacities is a V x V matrix in which V = 2 + n + 2*m (number of participants, activities and the source and sink nodes)
        - self.flow is also a V x V matrix which has O((n + m)^2) similar to self.capacities
        - self.assignments is a list of m lists meaning a list for each activity with a total space complexity of O(m) as a result

        """
        self.n = len(preferences)
        self.m = len(places)
        self.preferences = preferences
        self.places = places
        self.total_activities = 2 * self.m
        self.source = 1
        self.sink = 0
        self.V = 2 + self.n + self.total_activities
        self.capacities = [[0] * self.V for _ in range(self.V)]
        self.flow = [[0] * self.V for _ in range(self.V)]
        self.assignments = [[] for _ in range(self.m)]

    def add_edge(self, start: int, end: int, capacity: int) -> None:
        """
        Function description: Adds an edge between nodes start and end with a given capacity

        Approach Description:
        - The use of a seperate add_edge function allows for the adding of a an edge from the start node to the end node to be easily completed,
        updating the capacity matrix with this edge and new capacity

        Input:
        - start: the start node in the flow
        - end: the node that the start node is being connected to
        - capacity: the capacity of the edge from start to end

        Output: None

        Time Complexity: O(1)

        Time Complexity Analysis:
        -Updating the capacity between the two nodes in the capacity matrix is done in constant time

        Space Complexity: O(1)
        - There is no need for additional space to update the existing matrix, so it's constant space
        """
        self.capacities[start][end] = capacity

    def build_flow(self) -> None:
        """
        Function description: Builds the flow network by adding edges from the participants to activites based on preferences and capacities

        Approach Description:
        - Adds edges from the source to each participant
        - For each participant, it adds edges to the leader and non leader nodes of each activity based on the participants preferences
        If a person has a preference of 2, it connects them to both leader and non leader nodes and if it is 1 it connects them to non leaders and 0 does not connect them to anything
        - Adds edges from the leader and non leader node s to the sink with th the capacities for these edges coming from the activity capacities
        This works by having 2 as the capacity for leaders and the total capacity - 2 for the non leaders.

        Input: None

        Output: None

        Time Complexity: O(n *m) where n is the number of participants and m is the number of activities

        Time Complexity Analysis:
        - To add edges form the source to participants, the loop runs n times - once for each participant, with O(1) complexity for adding the edge, giving it overall O(n) complexity
        - To add edges from participants to activites, it is derived from the loop for participants O(n) running an inner loop over all participants O(m)
        - To add edges from leaders and non leaders to the sink, the loop runs m times (once for each activity), giving it a complexity of O(m)
        - Therefore the adding edges participants to activities loop dominates, giving it a complexity of O(n *m)

        Space Complexity: O(1)

        Space Complexity Analysis:
        - No additional data structures are created in this function, leading to only constant variables taking up space
        - The capacity and flow matricies are modified in this funciton, but these area already initialised in the __init__() method


        """
        for i in range(self.n):
            participant_node = 2 + i
            self.add_edge(self.source, participant_node, 1)

        for i in range(self.n):
            participant_node = 2 + i
            for j in range(self.m):
                leader_node = 2 + self.n + j
                non_leader_node = 2 + self.n + self.m + j

                if self.preferences[i][j] == 2:
                    self.add_edge(participant_node, leader_node, 1)
                    self.add_edge(participant_node, non_leader_node, 1)
                elif self.preferences[i][j] == 1:
                    self.add_edge(participant_node, non_leader_node, 1)

        for j in range(self.m):
            leader_node = 2 + self.n + j
            non_leader_node = 2 + self.n + self.m + j

            self.add_edge(leader_node, self.sink, 2)
            non_leader_capacity = max(0, self.places[j] - 2)
            self.add_edge(non_leader_node, self.sink, non_leader_capacity)

    def bfs(self, parent: List[int]) -> bool:
        """
        Function description: Performs a BFS to find an augmenting path in the residual graph from the source to the sink

        Approach Description:
        - Initialises a queue and uses it to explore the graph layer by layer
        - Checks if there is a path from the source to the sink with the remaining capacity, storing the parent of each node

        Input:
        - parent: A list used to store the parent of each node to track the path for the residual graph

        Output:
        - Returns True if an augmenting path is found, or it returns False.

        Time Complexity: O(V^2) where V is the number of verticies
        In the context of this problem, V = 2 + n + 2*m (participants, activities, source and sink)

        Time Complexity Analysis:
        -The BFS visits each of V nodes, and at each node checks all other V nodes
        - This means the time complexity is O(V^2) where V is the number of verticies in the graph

        Space Complexity: O(V) where V is the number of verticies (V = 2 + n + 2*m)

        - This space is used by the visited list and queue. Each of these have a size proportional to the number of verticies V

        """
        visited = [False] * self.V
        queue = deque([self.source])
        visited[self.source] = True

        while queue:
            u = queue.popleft()
            for v in range(self.V):
                if not visited[v] and self.capacities[u][v] - self.flow[u][v] > 0:
                    parent[v] = u
                    if v == self.sink:
                        return True
                    queue.append(v)
                    visited[v] = True
        return False

    def edmonds_karp(self) -> int:
        """
        Function Description: This function implements Edmonds-Karp algorithm to compute the maximum flow from source to sink.

        Approach Description:
        - Repeatedly finds augmenting paths by using BFS  and increases the flow along the found paths.
        - Updates the flow and capacity in the residual graph for each augmenting path

        Input: None

        Ouput: Returns the maximum flow from the source to sink.

        Time Complexity: O(V^2 * E) where V is the number of verticies and E is the number of edges

        Time Complexity Analysis:
        -The BFS runs in O(V^2) time, and each time an augmenting path is found, the flow is updated
        - In the worst case, we need to find augmenting paths up to E times, the number of edges, resulting in O(V^2 *E). The number of edges E can be proportional to the number of verticies V.
        - This means that E is approx V in the worst case. Since V = 2 + n + 2*m (participants, activities, source and sink) and m <= n/2, we can approximate V is equal to O(n).
        - This means that the total time complexity becomes O(n^3) as O(V^2 * E) simplifies to O(V^3) which is just O(n^3)

        Space Complexity: O(V) where V is the number of verticies

        Space Complexity analysis:
        - The additional space used by this method is the 'parent' list, which has a size of O(V)
        - The capacity and flow matrices are modified but were initialised in the __init__() method, so their space complexity is not counted here

        """
        parent = [-1] * self.V
        max_flow = 0

        while self.bfs(parent):
            path_flow = 1
            s = self.sink
            while s != self.source:
                u = parent[s]
                self.flow[u][s] += path_flow
                self.flow[s][u] -= path_flow
                s = parent[s]

            max_flow += path_flow

        return max_flow

    def assign_participants(self) -> None:
        """
        Fucntion Descripton: Assigns participants to acitivies based on the residual flow graph

        Approach Description:
        - Iterates over the flow graph and assigns participants to activies based on the flow from participant to leader and non leader nodes

        Input: None

        Output: None

        Time Complexity: O(n * m) where n is the number of participants and m is the number of activities

        Time Complexity Analysis:
        - The function checks the flow for each participant n for each activity (leader and non leader nodes) m resulting in a complexity of O(n * m)

        Space Complexity: O(1)

        Space Complexity Analysis:
        - No additional data structures are created in this method as the assignments list was already initialised in the __init__() method, leading to only constant variables taking up space

        """
        for i in range(self.n):
            participant_node = 2 + i
            for j in range(self.m):
                leader_node = 2 + self.n + j
                non_leader_node = 2 + self.n + self.m + j
                if self.flow[participant_node][leader_node] > 0:
                    self.assignments[j].append(i)
                elif self.flow[participant_node][non_leader_node] > 0:
                    self.assignments[j].append(i)

    def assign_activities(self) -> Optional[List[List[int]]]:
        """
        Funciton Description: The main method to assign participants and leaders to activities using Edmonds-Karp algorithm.

        Approach Description:
        - First it constructs the flow network by calling build_flow(), which sets up all the edges aswell as the capacities between the source, leader and non leader nodes and the sink
        - It then calls edmonds_karp() to compute the maximum flow in the constructed network, checking if it is possible to assign all participants to activities
        - After this, if the maximum flow is equal to the number of participants n, it proceeds to assign participants to activities by calling assign_participants(), which maps participants to the residual flow graph
        - If the maximum flow is not sufficient (the max flow is less than n), the method returns None to indicate that it is impossible to assign participants to activities while also meeting given constraints

        Input: None

        Output:
        - If a valid assignment is possible (max_flow == n), it returns a list of lists (assignments) in which each sublist contains the indicies of participants assigned to that particular activity
        - If no valid assignment is possible, it returns None

        Time Complexity: O(n^3)

        Time Complexity Analysis:
        -The build flow method has a complexity of O(n*m) where n is the number of participants and m is the number of activities
        -The edmonds_karp() method has a worse case time complexity of O(n^3) as explained previously, as the number of verticies and edges are proportional to n.
        -The assign_participants() method has a worse case time complexity of O(n*m), but this is dominated by the complexity of the edmond karp algorithm
        -Therefore the overall complexity is dominated by edmonds_karp, with a complexity of O(n^3)

        Space Complexity: O(n)
        -The main additional data structure used in this method is the 'parent' list, which stores the parent nodes for tracking augmenting paths in the BFS.
        -Since the flow and capacity matricies are initialised in the __init__() method, the rest of these methods only update them meaning no extra space is required for this method for them
        """
        self.build_flow()
        max_flow = self.edmonds_karp()
        if max_flow == self.n:
            self.assign_participants()
            return self.assignments
        else:
            return None

def assign(preferences: List[List[int]], places: List[int]) -> Optional[List[List[int]]]:
    """
    Function Description:
    This is a wrapper function that creates an instance of the Assign class and returns the result of the assign_activities() method

    Approach Description:
    - The function initializes an instance of the Assign class with two inputs preferences and places
    - After initializing the Assign instance, it calls the assign_activities() method of that instance to perform the maximum flow calculation and find a valid assignment of participants to activities whilst fulfilling all requirements
    - The function returns the output of assign_activities(), which is a list of assignments (if there was a successful assignment) or None (if there was no valid assignment).

    Input:
    - preferences: A list of lists where preferences[i][j] describes the interest level of participant i in activity j.
    - places: A list where each element represents the maximum capacity of participants for each activity.

    Output:
    - A list of lists which are the assignments where each sublist contains the indices of participants assigned to a particular activity, if a valid assignment is possible.
    - If no valid assignment is possible, it returns None.

    Time Complexity: O(n^3) where n is the number of participants
    - First, an instance of the assign class is initialised leading to an initialization complexity of O((n + m)^2) (as explained in __init__())
    - The assign_activities method uses the Edmonds-Karp algorithm, which has a time complexity of O(n^3) (refer to assign_activities() and edmonds_karp())
    - Therefore, the overall time complexity of the assign function is dominated by the assign_activities method, resulting in a time complexity of O(n^3).

    Space Complexity: O(n^2)
    -The Assign class maintains two matrices: capacities and flow, each of size V x V, where V is the number of vertices in the flow network (V = 2 + n + 2m). Since m ≤ n/2, this results in a space complexity of O(n^2).
    - More space is used for storing the preferences and places lists, which have Space Complexities of O(n * m) and O(m) respectively, but these are small compared to O(n^2).
    - The assign_activities method itself uses space for the parent list and some constant space for variables, but these are also dominated by the O(n^2) space for the flow and capacity matrices.
    - Therefore, the total space complexity is O(n^2).
    """
    assign = Assign(preferences, places)
    return assign.assign_activities()
