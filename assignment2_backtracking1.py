# Alan Sebastian 33855137
# Question 1

class Assign:
    def __init__(self, preferences, places):
        self.n = len(preferences)
        self.m = len(places)
        self.preferences = preferences
        self.places = places
        self.leaders = [[] for _ in range(self.m)]
        self.assignments = [[] for _ in range(self.m)]
        self.used = [False] * self.n
        self.graph = [[] for _ in range(self.n)]  # Adjacency list for participants to activities

    def build_graph(self):
        """
        Builds an adjacency list representing participants and their interests.
        """
        for i in range(self.n):
            for j in range(self.m):
                if self.preferences[i][j] > 0:
                    self.graph[i].append(j)
        print(f"Graph (participants to activities): {self.graph}")  # Debug print

    def find_leaders(self):
        """
        Identifies leaders for each activity. Each activity needs two distinct leaders.
        Leaders must have previous experience (i.e., a '2' in preferences).
        """
        for i in range(self.n):
            for j in range(self.m):
                if self.preferences[i][j] == 2:
                    self.leaders[j].append(i)
        print(f"Leaders for each activity: {self.leaders}")  # Debug print

    def backtrack_leaders(self, activity_index):
        """
        Recursively assigns leaders for each activity using backtracking.
        Each activity requires exactly two distinct leaders.
        """
        if activity_index == self.m:
            # After assigning leaders, try assigning participants and verify the assignment
            print(f"Leaders assigned so far: {self.assignments}")  # Debug print
            self.assign_participants()
            if self.verify_assignments():
                print(f"Assignments after participants added: {self.assignments}")  # Debug print
                return True
            else:
                return False

        if len(self.leaders[activity_index]) < 2:
            print(f"Not enough leaders for activity {activity_index}")  # Debug print
            return False

        for i in range(len(self.leaders[activity_index])):
            for j in range(i + 1, len(self.leaders[activity_index])):
                leader_1 = self.leaders[activity_index][i]
                leader_2 = self.leaders[activity_index][j]

                if not self.used[leader_1] and not self.used[leader_2]:
                    self.assignments[activity_index].extend([leader_1, leader_2])
                    self.used[leader_1] = True
                    self.used[leader_2] = True
                    print(f"Assigned leaders {leader_1}, {leader_2} to activity {activity_index}")  # Debug print

                    if self.backtrack_leaders(activity_index + 1):
                        return True

                    # Backtrack if failed
                    self.assignments[activity_index].remove(leader_1)
                    self.assignments[activity_index].remove(leader_2)
                    self.used[leader_1] = False
                    self.used[leader_2] = False
                    print(f"Backtracked from activity {activity_index}, leaders {leader_1}, {leader_2} removed")  # Debug print

        return False

    def assign_participants(self):
        """
        Assigns the remaining participants to activities based on their preferences.
        Uses the adjacency list to efficiently check valid activities.
        """
        for i in range(self.n):
            if not self.used[i]:  # If participant is not already used as a leader
                for j in self.graph[i]:  # Iterate over valid activities from adjacency list
                    if len(self.assignments[j]) < self.places[j]:
                        self.assignments[j].append(i)
                        self.used[i] = True
                        print(f"Assigned participant {i} to activity {j}")  # Debug print
                        break

    def verify_assignments(self):
        """
        Ensures all activities have the correct number of participants as per 'places'.
        """
        for j in range(self.m):
            if len(self.assignments[j]) != self.places[j]:
                print(f"Activity {j} has incorrect number of participants: {len(self.assignments[j])}, expected {self.places[j]}")  # Debug print
                return False
        return True

    def assign_activities(self):
        """
        Main method to find an assignment of participants to activities.
        First, it assigns leaders using backtracking, then fills in the remaining participants.
        Returns None if a valid assignment cannot be made.
        """
        self.build_graph()  # Build the adjacency list
        self.find_leaders()

        if not self.backtrack_leaders(0):
            print("Failed to assign leaders")  # Debug print
            return None

        return self.assignments

def assign(preferences, places):
    assignment = Assign(preferences, places)
    return assignment.assign_activities()

# Question 2
# Alan Sebastian 33855137



