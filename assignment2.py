from collections import deque
from typing import List, Optional, Tuple


#33855137 Assignment 2
#Question 1: A Fun Weekend Away

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




#Question 2 Customized Spell Checker:

class TrieNode:
    def __init__(self) -> None:
        """
        Function Description: Initialises the TrieNode Class.

        Approach Description:
        - The node contains an array called children which has 62 slots to represent characters 'a'-'z', 'A'-'Z' and and '0'-'9'
        -is_end_of_word is initalised as a boolean that indicates the end of a word
        -frequency represents the amount of times this word has been added
        -word stores the complete word for reference

        Inputs: None
        Outputs: None

        Time Complexity: O(1) - it only involves constant time operations like creating a fixed size array

        Space Complexity: O(1)
        - There is just a fixed size for children O(62) = O(1)
        """
        self.children = [None] * 62  # A list of size 62 to represent a-z, A-Z, 0-9
        self.is_end_of_word = False
        self.frequency = 0  # Track the frequency of the word
        self.word = None  # Store the full word for suggestions

def char_to_index(char: str) -> int:
    """ 
    Function Description: Converts a character to a specific index between 0-61.

    Approach: 
    -Characters are mapped as follows: 0-25 for 'a'-'z', 26-51 for 'A'-'Z', 52-61 for '0'-'9' 

    Input:
    -char: a single character that is converted
    
    Output:
    - An integer representing the index that corresponds to the character

    TIme Complexity: O(1)
    - Only involves creating fixed size arrays and simple assignments

    Space Complexity: O(1)
    -Uses a constant amount of memory
    
    """
    if 'a' <= char <= 'z':
        return ord(char) - ord('a')
    elif 'A' <= char <= 'Z':
        return ord(char) - ord('A') + 26
    elif '0' <= char <= '9':
        return ord(char) - ord('0') + 52
    return -1

class SpellChecker:
    def __init__(self, filename: str) -> None:
        """
        Function Description: Initializes the SpellChecker class by reading a file contianing messages and creating a trie for efficient word lookup

        Approach Description:
        - The method opens the provided filename (input) and reads each line
        - It splits each line into words and then inserts these words into the trie structure

        Input:
        - filename: A string representing the path to the file containing the messages that are to be interpreted
        
        Output:
        - None

        Time Complexity: O(T) where T is the total number of characters in the file

        Time Complexity Analysis:
        - Each word is processed character by character, and inserted into the trie.
        - Therefore, the time complexity is proportional to the number of characters T in the file.

        Space Complexity: O(T) where T is the total number of characters in the file

        Space Complexity Analysis:
        - The space complexity is dominated by the size of the Trie, which grows in proportion to the number of characters in the file.
        """

        self.root = TrieNode()
        self.build_trie(filename)

    def build_trie(self, filename: str) -> None:
        """
        Funciton description: Reads the file and inserts each word into the trie

        Approach:
        -Each line is split into words, which are then inserted into the trie

        Input:
        -filename: a string representing the path to the file that contains the messages that will be processed

        Output: 
        - None (The purpose of the function is to build the trie in place)

        Time Complexity: O(T) where T is the total number of characters in each file

        Time Complexity Analysis:
        - Every character in the file is inserted into the trie, leading to a complexity of O(T)

        Space Complexity: O(T)

        Space Complexity Analysis:
        - Space Complexity is O(T) as the trie grows in size proportional to the number of characters in each file
        
        """
        with open(filename, 'r') as file:
            for line in file:
                words = self.extract_words(line)
                for word in words:
                    self.insert_word(word)

    def extract_words(self, line: str) -> List[str]:
        """
        Function Description: Extracts words from a line by replacing all non alphanumerical characters with a space.

        Approach:
        -Iterates through every character in the line, keeping only alphanumerical characters and spaces, splitting the resulting string up

        Input:
        -line: a stirng representing a single line from the file

        Output:
        - A list of words (strings) from the line

        Time Complexity: O(T) where T is the total number of characters in the line

        Space Complexity: O(T)
        - T space is required for the cleaned up words in the line

        """
        return ''.join(c if c.isalnum() else ' ' for c in line).split()

    def insert_word(self, word: str) -> None:
        """
        Function description:
        Inserts a word into the Trie structure. Each character in the word is mapped to a specific index (0-25 for 'a'-'z', 26-51 for 'A'-'Z', and 52-61 for '0'-'9').

        Approach description:
        - For each character in the word, it determines the index and navigates to the corresponding child node in the trie
        - If a child node does not exist for a character, a new node is created
        - Once the word is completely inserted, the last node is marked as an end-of-word node, and its frequency counter is incremented
        
        Input:
        - word: A string representing the word to be inserted into the Trie
        
        Output
        - None
        
        Time complexity: O(M), where M is the length of the word being inserted
        
        Time complexity analysis:
        -Each character in the word is processed exactly once. Since the number of characters in the word is M, the time complexity for inserting a single word is O(M)
        
        Space Complexity: O(M), where M is the length of the word being inserted.
    
        
        Space complexity analysis:
        - Space is required for each character in the word to create Trie nodes, leading to a space complexity proportional to M.
        """

        node = self.root
        for char in word:
            index = char_to_index(char)
            if node.children[index] is None:
                node.children[index] = TrieNode()
            node = node.children[index]
        node.is_end_of_word = True
        node.frequency += 1  # Increment frequency
        node.word = word

    def check(self, input_word: str) -> List[str]:
        """
        Function description: This function checks if the input word exists in the trie. If the word is not found, it suggests up to three words that share a common prefix with the input word.

        Approach description:
        - This method navigates the trie using the characters of the input word
        - If the input word is not found in this trie (it does not find an end-of-word node associated with the word), it returns an empty list
        - If the word is not found, it retrieves suggestions by performing a DFS from the deepest matched node
        
        Input:
        - input_word: A string that represents the word to be checked
        
        Output:
        - Returns a list of up to three suggested words that share a common prefix with the input word, or an empty list if the word is found exactly or no suggestions exist
        
        Time complexity: O(M + U), where M is the length of the input word and U is the Total number of characters in the returned suggestions
        
        Time complexity analysis:
        -Traversing the Trie for the input word takes O(M), and collecting suggestions using DFS has a complexity of O(U). Therefore, the overall complexity is O(M + U).
        
        Space complexity: O(M + U), where M is the length of the input word and U is the total number of characters in the suggestions.
        
        Space complexity analysis:
        - The space complexity is dominated by the input word length (M) and the storage for the returned suggestions (U).
        """
        node = self.root
        current_prefix = ""
        
        for char in input_word:
            current_prefix += char
            index = char_to_index(char)
            if index == -1 or node.children[index] is None:
                return self.get_suggestions(current_prefix)
            node = node.children[index]
        
        if node.is_end_of_word:
            return []
        
        return self.get_suggestions(current_prefix)

    def get_suggestions(self, prefix: str) -> List[str]:
        """
        Function description: Finds all words in the Trie that share a given prefix and ranks them by prefix length, word frequency, and ASCII order.

        Approach description:
        - The trie is traversed to the deepest node matching the prefix
        - From this node, a DFS is performed to find all words that share the prefix
        - If the prefix does not match completely, the function backtracks to shorter prefixes (reducing one character at a time) and performs a dfs from these nodes to gather more suggestions
        - Once all suggestions are gathered it ranks them by the common prefix length, then by word frequency and finally by ASCII ordering
        
        Input:
        - prefix: A string representing the prefix to search for in the Trie.
        
        Output:
        - A list of up to three suggested words based on the given prefix, ranked by the common prefix length, then by word frequency and finally by ASCII ordering
        
        Time complexity: O(U), where U is the total number of characters in the returned suggestions
        
        Time complexity analysis:
        - The DFS explores all nodes corresponding to valid suggestions, and the complexity is proportional to the number of characters in the suggestions, which is O(U).
        
        Space complexity: O(U), where U is the total number of characters in the returned suggestions.
        
        Space complexity analysis:
        - The space complexity is determined by the number of valid suggestions collected and stored, which is proportional to U.
        """
        node = self.root
        suggestions = []
        seen_words = []

        current_prefix = ""
        longest_matching_prefix = ""
        matched_length = 0 

        for char in prefix:
            current_prefix += char
            index = char_to_index(char)
            if node.children[index] is None:
                break
            node = node.children[index]
            longest_matching_prefix = current_prefix
            matched_length += 1

        suggestions.extend(self.dfs(node, longest_matching_prefix, seen_words))

        while matched_length > 1:
            matched_length -= 1
            node = self.root
            current_prefix = prefix[:matched_length]
            for char in current_prefix:
                index = char_to_index(char)
                node = node.children[index]

            suggestions.extend(self.dfs(node, current_prefix, seen_words))

        suggestions.sort(key=lambda x: x[0])  

        suggestions.sort(key=lambda x: -x[1]) 

        for i in range(len(suggestions)):
            suggestion_word = suggestions[i][0]
            common_prefix_len = self.calculate_common_prefix_length(suggestion_word, prefix)
            suggestions[i] = (suggestion_word, suggestions[i][1], common_prefix_len)

        suggestions.sort(key=lambda x: -x[2])  

        top_suggestions = [word for word, _, _ in suggestions[:3]]
        return top_suggestions


    def calculate_common_prefix_length(self, word: str, prefix: str) -> int:
        """
        Function Description: Calculates the length of the common prefix between a word and the given prefix

        Approach:
        - The funciton iterates through both the word and the prefix, comparing characters one at a time
        - The comparison continues until the characters do not match or one of the strings are fully traversed
        -The length of the matching prefix is returned 

        Input: 
        -word: a string that represents the full word
        -prefix: a string that represents the prefix to be compared with the word
        
        Output:
        - An integer that represensts the length of the common prefix between the word and the prefix

        Time Complexity: O(M) where M is the length of the shorter string (either the word or the initial prefix)

        Time Complexity Analysis:
        - This function compares characters until a mismatch is found or one of the strings is fully traversed, meaning it depends on the length of the shorter string

        Space Complexity: O(1)

        Space Complexity Analysis:
        -The Function only uses a constant amount of space to store the common length (just one integer)
        
        """
        common_length = 0
        for i in range(min(len(word), len(prefix))):
            if word[i] == prefix[i]:
                common_length += 1
            else:
                break
        return common_length


    def dfs(self, node: TrieNode, prefix: str, seen_words: List[str]) -> List[Tuple[str, int, int]]:
        """
        Function description: Performs a depth-first search (DFS) from the given node in the Trie to collect valid word suggestions.

        Approach description:
        - The dfs is implemented iteratively using a stack starting from the node representing the prefix
        - The loop continues as long as the stack is not empty. In each iteration, the current node and its prefix are popped from the stack for processing
        - If the current node marks the end of a word (`is_end_of_word` is True) and the word is not in the `seen_words` list, the word is added to the suggestions list along with its frequency and the length of the prefix
        - The word is also added to seen_words to avoid duplication.
        - The function then explores all child nodes of the current node in lexicographical order. 
        - For each valid child node, the node and updated prefix are pushed onto the stack
        - The DFS terminates when the stack is empty, meaning all reachable nodes from the starting node have been explored

        Input:
        - node: The TrieNode to start the DFS from
        - prefix: A string representing the current prefix leading to the node
        - seen_words: A list of words already seen to avoid any duplicate words
        
        Output:
        - A list of valid word suggestions starting from the given node.
        
        Time complexity: O(U), where U is the total number of characters in the words collected during DFS.
        
        Time complexity analysis:
        - The DFS explores nodes for each valid suggestion, with the complexity depending on the number of characters 
        in the collected suggestions, leading to O(U) complexity overall
        
        Space Complexity: O(U), where U is the total number of characters in the collected suggestions
        
        Space complexity analysis:
        - The space complexity is proportional to the depth of the Trie being traversed and the number of suggestions collected

        """
        suggestions = []
        
        stack = [(node, prefix)]
        
        while stack:
            current_node, current_prefix = stack.pop()

            if current_node.is_end_of_word and current_node.word not in seen_words:
                suggestions.append((current_node.word, current_node.frequency, len(current_prefix)))
                seen_words.append(current_node.word)

            for i in range(62): 
                if current_node.children[i] is not None:
                    stack.append((current_node.children[i], current_prefix + self.index_to_char(i)))

        return suggestions

    def index_to_char(self, index: int) -> str:
        """
        Function description: Converts an index (0-61) back to its corresponding character (a-z, A-Z, 0-9)

        Approach:
        -The function checks the index and determines the corresponding character: 0-25 for 'a'-'z', 26-51 for 'A'-'Z', 52-61 for '0'-'9' and returns the corresponding character or empty string if index is out of range

        Input:
        -index: An integer between 0-61 representing the character position

        Output: 
        -a string representing the character corresponding to the given index, or an empty string if the index is not valid

        Time Complexity: O(1) as it performs a constant number of operations

        Space Complexity: O(1) as the function only uses a constant amount of space to store the result
        
        """
        if 0 <= index <= 25:
            return chr(index + ord('a'))
        elif 26 <= index <= 51:
            return chr(index - 26 + ord('A'))
        elif 52 <= index <= 61:
            return chr(index - 52 + ord('0'))
        return ''