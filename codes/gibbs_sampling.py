import random
from collections import Counter

def get_profile(motifs, k):
    """
    Constructs a profile matrix based on the current motifs, with pseudocounts to avoid zeros.
    
    Parameters:
    motifs: List of selected motifs.
    k: Length of the motif.
    
    Returns:
    Profile matrix containing probabilities of each base at each position.
    """
    profile = [{"A": 1, "C": 1, "G": 1, "T": 1} for _ in range(k)]
    
    #Count the occurrences of each base at each position in the motif
    for motif in motifs:
        for i, base in enumerate(motif):
            profile[i][base] += 1
    
    #Normalize the values to convert them into probabilities
    for i in range(k):
        total = sum(profile[i].values())
        for base in "ACGT":
            profile[i][base] /= total  
    
    return profile

def get_probability(sequence, profile, k):
    """
    Calculates the probability of each possible motif within the sequence, based on the generated profile.
    
    Parameters:
    sequence: The DNA sequence being analyzed.
    profile: The profile matrix containing base probabilities.
    k: Length of the motif.
    
    Returns:
    A list of probabilities associated with each possible motif in the sequence.
    """
    probs = []

    #Iterate over all possible motifs within the sequence
    for i in range(len(sequence) - k + 1):
        motif = sequence[i:i + k]
        prob = 1.0
        
        #Calculate the probability of the motif according to the generated profile
        for j, base in enumerate(motif):
            prob *= profile[j][base]
        probs.append(prob)
    
    #Normalize the probabilities so they sum to 1
    total_prob = sum(probs)
    return [p / total_prob for p in probs] if total_prob > 0 else [1 / len(probs)] * len(probs)

def select_motif(sequence, profile, k):
    """
    Selects a new motif probabilistically within the sequence based on the profile.
    
    Parameters:
    sequence: The DNA sequence.
    profile: The profile matrix with probabilities.
    k: Length of the motif.
    
    Returns:
    The index of the starting position of the selected motif.
    """
    #Get the probabilities for each motif in the sequence
    probabilities = get_probability(sequence, profile, k)
    return random.choices(range(len(probabilities)), weights=probabilities)[0]

def gibbs_sampler(sequences, k, max_iter=100, stagnation_limit=20):
    """
    Implements the Gibbs Sampling algorithm to find common motifs in a set of DNA sequences.
    
    Parameters:
    sequences: List of DNA sequences.
    k: Length of the motif.
    max_iter: Maximum number of iterations.
    stagnation_limit: Maximum number of iterations without improvement before stopping.
    
    Returns:
    The best set of motifs, their positions, and the best score found.
    """
    num_seqs = len(sequences)
    
    #Find the shortest sequence length to limit the motif positions
    seq_len = min(len(seq) for seq in sequences)
    limit = seq_len - k + 1
    
    #Initialize random positions for the motifs in each sequence
    positions = [random.randint(0, limit - 1) for _ in sequences]
    
    #Extract motifs from the initial positions; initialize the best score to a very low value
    best_motifs = [sequences[i][positions[i]:positions[i] + k] for i in range(num_seqs)]
    best_score = float('-inf')
    stagnation_count = 0
    
    for iteration in range(max_iter):
        #Randomly choose a sequence to temporarily remove, then build the profile without it
        seq_idx = random.randint(0, num_seqs - 1)
        remaining_motifs = [sequences[i][positions[i]:positions[i] + k] for i in range(num_seqs) if i != seq_idx]
        profile = get_profile(remaining_motifs, k)
        
        #Select a new motif probabilistically for the removed sequence, update the positions
        positions[seq_idx] = select_motif(sequences[seq_idx], profile, k)
        motifs = [sequences[i][positions[i]:positions[i] + k] for i in range(num_seqs)]
        
        #Calculate the score of the motif set (highest frequency of the most common base in each motif position)
        score = sum(Counter(col).most_common(1)[0][1] for col in zip(*motifs))
        
        #Update the best motifs if there is an improvement in the score
        if score > best_score:
            best_score = score
            best_motifs = motifs[:]
            best_positions = positions[:]
            stagnation_count = 0
        else:
            stagnation_count += 1
        
        #Stagnation stopping criterion
        if stagnation_count >= stagnation_limit:
            print(f"Termination criterion reached after {iteration + 1} iterations.")
            break
    
    print("Motifs found:")
    
    for i, (pos, motif) in enumerate(zip(best_positions, best_motifs)):
        print(f"Sequence {i + 1}: Position {pos}, Motif: {motif}")
    print("Best score:", best_score)
    
    return best_motifs, best_positions, best_score

if __name__ == "__main__":
    seqs = input("Enter DNA sequences separated by space: ").split()
    k = int(input("Enter the motif length: "))
    gibbs_sampler(seqs, k)
