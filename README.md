# Bioinformatics Sequence Analysis Toolkit
## A suite of Python tools for biological sequence analysis and Motif Discovery
## Introduction
Motif discovery is a fundamental task in bioinformatics used to identify recurring patterns in DNA, RNA, or protein sequences. These motifs often play crucial roles in gene regulation, transcription factor binding, and evolutionary analysis.

### This repository provides two algorithms for motif discovery:

    - Branch and Bound Algorithm – A deterministic approach that efficiently finds the optimal motif.
    - Gibbs Sampling Algorithm – A probabilistic method used to discover motifs in a flexible and iterative manner.

## Features
### 1. Branch and Bound Algorithm
### Overview
The Branch and Bound algorithm is a combinatorial optimization technique used to efficiently search for the best motif. Instead of exhaustively checking all possible motif positions, it prunes unnecessary search branches based on upper-bound estimates of potential scores.
### How It Works
    - Uses a recursive approach to explore motif positions across sequences.
    - Prunes search paths when they are guaranteed to not yield better results than the best found so far.
    - Returns the optimal motif positions with the highest score.

### Advantages and Disadvantages

✅ Guarantees the best possible solution.

✅ Efficient pruning avoids unnecessary computations.

❌ Computationally expensive for large datasets.

### 2. Gibbs Sampling Algorithm
### Overview
Gibbs Sampling is a probabilistic approach to motif discovery. It is particularly useful when dealing with large datasets, as it provides a fast and flexible way to identify motifs without exhaustively searching all possibilities.
### How It Works
    - Randomly selects initial motif positions from sequences.
    - Iteratively refines the motif set by:
        - Removing one sequence at a time.
        - Constructing a probabilistic profile based on the remaining motifs.
        - Sampling a new motif for the removed sequence using the profile.
    - Repeats until convergence (or after a set number of iterations).

### Advantages and Disadvantages

✅ Works well for large datasets.

✅ Can escape local optima due to its stochastic nature.

❌ May not always find the globally optimal solution.


## Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/klopesb/portfolio_de_sequencias.git
```
```bash
pip install -r requirements.txt
```

## Usage
Each module includes example cases that demonstrate basic functionality:
```python
# Run Branch and Bound example with the sequences in the instructions below:
python -m code.branch_and_bound

# Run Gibbs Sampling example with the sequences in the instructions below:
python -m code.gibbs_sampling
```
For actual use in your code, import the modules and use their functions:
```python
# Example: Perform Branch and Bound Algorithm
from codes.branch_and_bound import branch_and_bound

# Example sequences
seqs = "ATGGTCGC TTGTCTGA CCGTAGTA"

# Parameters (Motif lenght, number of sequences)
tam_motif = 3
num_seqs = len(seqs)

# Run Branch & Bounch algorithm
best_motif, best_score = branch_and_bound(seqs, num_seqs, motif_size)

# Print results
print("Best motif positions:", best_motif)
print("Best score found:", best_score)
```

```python
# Example: Perform Gibbs Sampling Algorithm
from codes.gibbs_sampling import gibbs_sampler

# Example sequences
seqs = "GTAAACAATATTTATAGC AAAATTTACCTCGCAAGG CCGTACTGTCAAGCGTGG TGAGTAAACGACGTCCCA TACTTAACACCCTGTCAA"

# Parameters (Motif lenght, number of sequences)
k = 8
num_seqs = len(sequences)

# Run Gibbs Sampling algorithm
best_motifs, best_positions, best_score = gibbs_sampler(seqs, k)

# Print results
print(f"Termination criterion reached after {iteration + 1} iterations.")
print(f"Sequence {i + 1}: Position {pos}, Motif: {motif}")
print("Best Score:", best_score)

```

## Running Tests
The project includes comprehensive unit tests in the tests folder. To run the tests:

```bash
# Run all tests
python -m unittest discover -s tests

# Run specific test files
python -m unittest tests/tests_branch_and_bound.py
python -m unittest tests/tests_gibbs_sampling.py

```

## Dependencies 
- Python 3.x
- Collections
- Random
- Unittest


## Contribution
-  [Cátia Rosário](https://github.com/bluecanguru)
-  [Elidiane Rosário](https://github.com/ely-24)
-  [Karolina Barbosa](https://github.com/klopesb)
-  [Vanessa Rodriguez](https://github.com/VaneBR)

## License
This project is open source and available under the MIT License.
