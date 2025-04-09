def branch_and_bound(seqs, num_seqs, motif_size, partial_pos=[], level=0, max_score=0):
    """
    Implements the Branch and Bound search recursively to find the best motif in DNA sequences.
    
    Parameters:
    seqs (list): List of DNA sequences.
    num_seqs (int): Total number of sequences.
    motif_size (int): Size of the motif to be searched.
    partial_pos (list, optional): List of partial motif positions in each sequence.
    level (int, optional): Current level of the recursive search.
    max_score (int, optional): Best score found so far.
    
    Returns:
    A tuple containing the list of best positions and the corresponding score.
    """
    
    #Check if there are no sequences or invalid motif size
    if not seqs or num_seqs == 0 or motif_size == 0:
        return [], 0

    #Check if all sequences have the same length
    if any(len(s) != len(seqs[0]) for s in seqs):
        raise ValueError("All sequences must have the same length")

    #Check if the motif size is larger than the sequence length
    if motif_size > len(seqs[0]):
        raise ValueError("Motif size cannot be greater than the sequence length")
    
    #Calculate and return the current score, extract the motifs and correcting score calculation per column
    if level == num_seqs:
        motifs = [s[p:p+motif_size] for p, s in zip(partial_pos, seqs)]
        
        current_score = sum(max(col.count(base) for base in set(col)) for col in zip(*motifs))
        return partial_pos, current_score

    best_pos, best_score = None, max_score

    #Iterate over all possible positions for the current level
    for pos in range(len(seqs[level]) - motif_size + 1):
        #Update the list of partial positions to include the current position
        new_pos = partial_pos + [pos]
        
        #Extract the motifs from the sequences based on the new positions
        motifs = [s[p:p+motif_size] for p, s in zip(new_pos, seqs)]
        
        #Calculate the partial score, evaluating the motifs column by column
        partial_score = sum(max(col.count(base) for base in set(col)) for col in zip(*motifs))
        
        #Estimate the score if the search were to continue from here
        estimate = partial_score + (num_seqs - len(new_pos)) * motif_size
        
        #If the estimated score is better than the current best, recurse to explore this branch
        if estimate > max_score:
            possible_new_pos, new_score = branch_and_bound(seqs, num_seqs, motif_size, new_pos, level + 1, best_score)
            #Update the best position and score if the new score is better
            if new_score > best_score:
                best_pos, best_score = possible_new_pos, new_score

    return best_pos, best_score

if __name__ == "__main__":
    seqs = input("Enter DNA sequences separated by space: ").split()
    motif_size = int(input("Enter the motif size: "))
    num_seqs = len(seqs)

    best_motif, best_score = branch_and_bound(seqs, num_seqs, motif_size)

    print("Best motif positions:", best_motif)
    print("Best score found:", best_score)
