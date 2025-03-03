import random
from collections import Counter

# Função para calcular a matriz de perfil a partir dos motifs atuais
def get_profile(motifs, k):
    """
    Constrói uma matriz de perfil baseada nos motifs atuais, com pseudocontagens para evitar zeros.
    
    Parâmetros:
        motifs: Lista de motifs selecionados.
        k: Comprimento do motif.
    
    Retorna:
        Matriz de perfil contendo probabilidades de cada base por posição.
    """
    profile = [{"A": 1, "C": 1, "G": 1, "T": 1} for _ in range(k)]
    
    # Conta a ocorrência de cada base em cada posição do motif
    for motif in motifs:
        for i, base in enumerate(motif):
            profile[i][base] += 1
    
    # Normaliza os valores para converter em probabilidades
    for i in range(k):
        total = sum(profile[i].values())
        for base in "ACGT":
            profile[i][base] /= total  
    
    return profile

# Função para calcular a probabilidade de cada possível motif de tamanho k dentro da sequência
def get_probability(sequence, profile, k):
    """
    Calcula a probabilidade de cada possível motif dentro da sequência, com base no perfil gerado.
    
    Parâmetros:
        sequence: Sequência de DNA analisada.
        profile: Matriz de perfil contendo probabilidades de bases.
        k: Comprimento do motif.
    
    Retorna:
        Lista de probabilidades associadas a cada possível motif na sequência.
    """
    probs = []
    
    # Percorre todos os possíveis motifs dentro da sequência
    for i in range(len(sequence) - k + 1):
        motif = sequence[i:i + k]
        prob = 1.0
        
        # Calcula a probabilidade do motif conforme o perfil gerado
        for j, base in enumerate(motif):
            prob *= profile[j][base]
        probs.append(prob)
    
    # Normaliza as probabilidades para que somem 1
    total_prob = sum(probs)
    return [p / total_prob for p in probs] if total_prob > 0 else [1 / len(probs)] * len(probs)

# Função para selecionar um novo motif com base nas probabilidades calculadas
def select_motif(sequence, profile, k):
    """
    Seleciona probabilisticamente um novo motif dentro da sequência com base no perfil.
    
    Parâmetros:
        sequence: Sequência de DNA.
        profile: Matriz de perfil com probabilidades.
        k: Comprimento do motif.
    
    Retorna:
        Índice da posição inicial do motif selecionado.
    """
    probabilities = get_probability(sequence, profile, k)
    return random.choices(range(len(probabilities)), weights=probabilities)[0]

# Implementação do Algoritmo de Gibbs Sampling para encontrar motifs em várias sequências
def gibbs_sampler(sequences, k, max_iter=100, stagnation_limit=20):
    """
    Implementa o algoritmo de Gibbs Sampling para encontrar motifs comuns em um conjunto de sequências de DNA.
    
    Parâmetros:
        sequences: Lista de sequências de DNA.
        k: Comprimento do motif.
        max_iter: Número máximo de iterações.
        stagnation_limit: Número máximo de iterações sem melhoria antes da parada.
    
    Retorna:
        Melhor conjunto de motifs, suas posições e a melhor pontuação encontrada.
    """
    num_seqs = len(sequences)
    tam_seq = min(len(seq) for seq in sequences)
    limite = tam_seq - k + 1
    
    # Inicializa posições aleatórias para os motifs em cada sequência
    positions = [random.randint(0, limite - 1) for _ in sequences]
    best_motifs = [sequences[i][positions[i]:positions[i] + k] for i in range(num_seqs)]
    best_score = float('-inf')
    stagnation_count = 0
    
    # Loop principal do algoritmo
    for iteration in range(max_iter):
        # Escolhe aleatoriamente uma sequência para remover temporariamente
        seq_idx = random.randint(0, num_seqs - 1)
        
        # Constrói o perfil sem considerar a sequência removida
        remaining_motifs = [sequences[i][positions[i]:positions[i] + k] for i in range(num_seqs) if i != seq_idx]
        profile = get_profile(remaining_motifs, k)
        
        # Seleciona um novo motif probabilisticamente para a sequência removida
        positions[seq_idx] = select_motif(sequences[seq_idx], profile, k)
        
        # Atualiza a lista de motifs baseada nas novas posições
        motifs = [sequences[i][positions[i]:positions[i] + k] for i in range(num_seqs)]
        
        # Calcula o score do conjunto de motifs (maior frequência da base mais comum em cada posição do motif)
        score = sum(Counter(col).most_common(1)[0][1] for col in zip(*motifs))
        
        # Atualiza os melhores motifs caso haja melhoria no score
        if score > best_score:
            best_score = score
            best_motifs = motifs[:]
            best_positions = positions[:]
            stagnation_count = 0
        else:
            stagnation_count += 1
        
        # Critério de parada baseado em estagnação
        if stagnation_count >= stagnation_limit:
            print(f"Critério de terminação alcançado após {iteration + 1} iterações.")
            break
    
    print("Motifs encontrados:")
    for i, (pos, motif) in enumerate(zip(best_positions, best_motifs)):
        print(f"Sequência {i + 1}: Posição {pos}, Motif: {motif}")
    print("Melhor score:", best_score)
    
    return best_motifs, best_positions, best_score

if __name__ == "__main__":
    seqs = ["GTAAACAATATTTATAGC", "AAAATTTACCTCGCAAGG", "CCGTACTGTCAAGCGTGG", "TGAGTAAACGACGTCCCA", "TACTTAACACCCTGTCAA"]
    k = 8
    gibbs_sampler(seqs, k)

#unittest: python -m unittest tests_gibbs_sampling.py