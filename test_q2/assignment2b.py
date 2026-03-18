from typing import List, Optional, Tuple

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