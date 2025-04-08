# High-Level Project Plan - Naïve Finite Automaton (FA) for Pattern Recognition

## 1. Description

This project implements a deterministic finite automaton (DFA) for pattern recognition within sequences.  
It systematically evaluates an input sequence using a predefined transition table, ensuring fast and accurate matching.

Unlike advanced algorithms like Knuth-Morris-Pratt (KMP), this project focuses on a naïve, direct state transition approach.  
Its main goal is to provide simple and efficient pattern detection with minimal overhead.

---

## 2. Key Features of the Project

### 🔹 **Pattern Recognition using FA**
- Uses a **state-driven deterministic model** to identify occurrences of the given pattern.
- Supports **any alphabet** (DNA `{A, C, G, T}`, English letters `{a-z}`, or user-defined symbols).

### 🔹 **Transition Table Generation**
- Dynamically constructs a **state transition table** based on the pattern.
- **Handles mismatches efficiently**, ensuring the correct reset behavior.

### 🔹 **Efficient Execution**
- Executes **in linear time `O(n)`**, scanning the input **in a single pass**.
- **No backtracking or recursion**, making it computationally lightweight.

### 🔹 **Overlapping Matches Handling**
- Ensures multiple occurrences of the pattern **are detected correctly**.

### 🔹 **Flexibility & User Input**
- Allows **custom pattern input**.
- **Interactive testing** via CLI.

### 🔹 **Unit Testing**
- Validates correctness with **test cases including edge conditions**.
- Ensures **robustness** against incorrect inputs.

---

# Low-Level Project Plan - Naïve Finite Automaton (FA) for Pattern Recognition

## a) Problem Understanding

### 1. **Goal Definition**
- Recognize **exact matches** of a given pattern within an input sequence.
- Use **finite automaton (FA) transition logic** to ensure fast processing.
- Allow **overlapping occurrences** to be detected.

### 2. **Pattern Processing**
- Constructs a **transition table** dynamically based on input pattern.
- Handles mismatches using a **reset strategy**, ensuring correct alignment.

---

## b) Design

### 1. **Search Space Representation**
- Represents each **character transition as state changes**.
- Uses **DFA mechanics**, where each **state tracks pattern progression**.

### 2. **Transition Table Construction**
- Moves to **next state if match occurs**.
- Resets to **zero on mismatches**.

### 3. **Handling Edge Cases**
- **Short sequences:** If input < pattern length, handle gracefully.
- **Overlapping matches:** Ensure patterns appearing at multiple locations are detected.

---

## c) Implementation

### 1. **Finite Automaton Execution**
- Define states dynamically based on **pattern length (`k+1` states)**.
- Implements **efficient state transitions** without recursion.

### 2. **Pattern Matching Logic**
- Scans input character-by-character, **tracking visited states**.
- Stores **positions of full matches** when reaching the final state.

### 3. **User Configurable Input**
- Accept **pattern and sequence** dynamically.
- Prints **transition table, visited states, and match positions**.

---

## d) Validation

### 1. **Unit Tests**
- **Verify correctness** for:
  - Known sequences (`"xyzabc"` should return match at `3`).
  - Overlapping occurrences (`"abcabc"` → `[0,3]`).
  - Edge cases (`""`, `"xyzxyz"`, `"abcdefg"`).

### 2. **Performance Testing**
- Measure execution time on **long sequences (`>1000 characters`)**.
- Ensure **memory efficiency** for large pattern sets.

---

## 📌 Final Notes
This project provides a **deterministic finite automaton (DFA) implementation**, offering **simplicity and efficiency** for basic pattern detection.  
Future improvements could include **more advanced matching techniques** for faster or more complex searches.
