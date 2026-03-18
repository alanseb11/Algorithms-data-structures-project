# Algorithms & Data Structures Project (Python)

A collection of algorithmic problem-solving implementations focused on efficient data structures, graph algorithms, and structured testing.

This repository demonstrates strong fundamentals in:

- algorithm design
- time and space complexity analysis
- modular Python code
- unit testing and validation

---

## Projects

### 1. Trie-Based Spell Checker

A custom spell checker built using a Trie (prefix tree) data structure.

#### Features

- Efficient word insertion using a fixed-size 62-character Trie (`a-z`, `A-Z`, `0-9`)
- Exact word lookup
- Prefix-based suggestion generation
- Ranking based on:
  - longest common prefix
  - word frequency
  - ASCII ordering
- Handles:
  - empty datasets
  - punctuation filtering
  - unusual alphanumeric inputs
  - large test files

#### Implementation Details

- Uses a custom `TrieNode` with an array of 62 child references
- Extracts valid words by filtering non-alphanumeric characters
- Traverses the Trie character by character for lookup
- Performs DFS from the deepest matched prefix node to collect candidate words
- Backtracks to shorter prefixes when necessary to gather additional suggestions

#### Complexity

- Trie construction: **O(T)**, where `T` is the total number of characters in the input file
- Querying: intended to follow **O(M + U)** behaviour, where:
  - `M` = input word length
  - `U` = total number of characters in returned suggestions

---

### 2. Weekend Activity Assignment

A participant allocation system implemented using a **maximum flow network** and the **Edmonds-Karp algorithm**.

#### Features

- Assigns participants to activities based on preferences and experience
- Supports:
  - leader allocation
  - non-leader allocation
  - per-activity capacity constraints
- Returns:
  - a valid assignment if one exists
  - `None` if the constraints cannot be satisfied

#### Implementation Details

- Models the problem as a **flow network**
- Uses:
  - a source node
  - participant nodes
  - leader activity nodes
  - non-leader activity nodes
  - a sink node
- Participants with experience can connect to both leader and non-leader activity nodes
- Participants without experience can only connect to non-leader nodes
- Uses BFS inside Edmonds-Karp to find augmenting paths and compute maximum flow
- Reconstructs final participant assignments from the resulting flow graph

#### Complexity

- Overall worst-case time complexity: **O(n³)**
- Space complexity: **O(n²)** due to the flow and capacity matrices

---

## Project Structure

```text
Algorithms-data-structures-project/
│
├── spell_checker/
│   ├── spell_checker.py
│   ├── text_files/
│   └── tests/
│
├── weekend_assign/
│   ├── weekend_assign.py
│   └── tests/
│
├── README.md
└── .gitignore
```

---

## Testing

Both tasks include unit tests covering:

- correctness checks
- edge cases
- invalid inputs
- multiple valid outputs
- stress / large input scenarios

### Spell Checker Tests

- empty files
- punctuation-only files
- small files
- ranking and prefix-matching test cases
- large dataset stress testing

### Weekend Assignment Tests

- impossible assignment cases
- valid assignment cases
- multiple valid solutions
- capacity validation
- participant uniqueness checks

---

## Key Concepts Demonstrated

- Trie data structures
- Depth-first search (DFS)
- Breadth-first search (BFS)
- Maximum flow / Edmonds-Karp
- Graph modelling
- Time and space complexity analysis
- Unit testing with `unittest`

---

## Running the Tests

From the project root, run:

```bash
python -m unittest discover
```

---

## What This Project Demonstrates

This project highlights strong problem-solving ability and understanding of core computer science concepts, including:

- designing efficient data structures
- modelling allocation problems as graphs
- implementing flow-based algorithms
- handling edge cases and large inputs
- writing clean, modular, and testable code

---

## Author

Alan Sebastian  
Monash University – Software Engineering & Commerce
