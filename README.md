# Bioinformatics Sequence Analysis Toolkit

A suite of Python tools for biological sequence analysis, featuring:

## Features
- Motif Analysis
    - Branch and Bound
    - Gibbs Sampling

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
