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
```python
from codes.branch_and_bound import branch_and_bound

#Example sequences
seqs = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]

# Parâmetros
num_seqs = len(seqs)
tam_motif = 3

#Run Branch & Bounch algorithm
melhor_motif, score_melhor = branch_and_bound(seqs, num_seqs, tam_motif)

#Print results
print("Best motif:", melhor_motif)
print("Best score:", score_melhor)

```

```python
from codes.gibbs_sampling import gibbs_sampler

#Example sequences
seqs = ["GTAAACAATATTTATAGC", "AAAATTTACCTCGCAAGG", "CCGTACTGTCAAGCGTGG", "TGAGTAAACGACGTCCCA", "TACTTAACACCCTGTCAA"]

#Parameter (Motif lenght)
k = 8

#Run Gibbs Sampling algorithm
best_motifs, best_positions, best_score = gibbs_sampler(seqs, k)

#Print results
print("Best Motifs:", best_motifs)
print("Best Positions:", best_positions)
print("Best Score:", best_score)

```

## Running Tests
The project includes comprehensive unit tests in the tests folder. To run the tests:

```bash
python -m unittest discover tests

python -m unittest tests/branch_and_bound_test.py
python -m unittest tests/gibbs_sampling_tests.py

```

## Dependencies 
- Python 3.x
- NumPy
- Collections
- Random
- Unittest




## Contribution
-  [Cátia Rosário](https://github.com/bluecanguru)
-  [Elidiane Rosário](https://github.com/ely-24)
-  [Karolina Barbosa](https://github.com/klopesb)
-  [Vanessa Rodriguez](https://github.com/VaneBR)
  
