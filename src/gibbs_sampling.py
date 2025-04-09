import random

def inicializar_posicoes_aleatorias(seqs, tam_motif):
    """
    Inicializa posições aleatórias para o início dos *motifs* em cada sequência.

    Parâmetros:
    -----------
    seqs : list of str
        Lista de sequências de DNA.
    tam_motif : int
        Comprimento do *motif* a ser identificado.

    Retorna:
    --------
    list of int
        Lista com as posições de início dos *motifs* para cada sequência.
    int
        Valor máximo possível de início de *motif* (limite).
    """
    tam_seq = min(len(seq) for seq in seqs)
    limite = tam_seq - tam_motif + 1
    return [random.randint(0, limite - 1) for _ in seqs], limite

def construir_pwm(seqs, start_pos, tam_motif, excluir_idx):
    """
    Constrói a matriz de peso de posição (PWM) a partir dos *motifs* das sequências,
    excluindo uma delas.

    Parâmetros:
    -----------
    seqs : list of str
        Lista de sequências de DNA.
    start_pos : list of int
        Lista com as posições iniciais dos *motifs* em cada sequência.
    tam_motif : int
        Tamanho fixo do *motif*.
    excluir_idx : int
        Índice da sequência a ser excluída da construção da PWM.

    Retorna:
    --------
    list of dict
        PWM onde cada posição contém um dicionário com a frequência normalizada das bases A, T, C e G.
    list of str
        Lista de *motifs* utilizados na construção da PWM.
    """
    motifs = [
        seqs[i][start_pos[i]:start_pos[i] + tam_motif]
        for i in range(len(seqs)) if i != excluir_idx
    ]

    count_bp = [
        {base: col.count(base) + 1 for base in "ATCG"}
        for col in zip(*motifs)
    ]

    PWM = [
        {base: count[base] / (len(seqs) - 1 + 4) for base in "ATCG"}
        for count in count_bp
    ]
    
    return PWM, motifs

def calcular_probabilidades_motifs(seq, PWM, tam_motif, limite):
    """
    Calcula as probabilidades de todos os *motifs* possíveis de uma sequência com base na PWM.

    Parâmetros:
    -----------
    seq : str
        Sequência de DNA da qual os *motifs* serão avaliados.
    PWM : list of dict
        Matriz de peso de posição com frequências normalizadas.
    tam_motif : int
        Comprimento dos *motifs* a serem avaliados.
    limite : int
        Posição máxima de início de *motif*.

    Retorna:
    --------
    dict
        Dicionário com probabilidades normalizadas para cada *motif* possível.
    dict
        Dicionário com as probabilidades brutas (não normalizadas) dos *motifs*.
    """
    random_seq_motifs = [seq[i:i + tam_motif] for i in range(limite)]

    prob_motif = {
        motif: round(sum(PWM[i][base] for i, base in enumerate(motif)), 6)
        for motif in random_seq_motifs
    }

    total_prob = sum(prob_motif.values())
    norm_prob = {motif: prob / total_prob for motif, prob in prob_motif.items()}

    return norm_prob, prob_motif

def selecionar_motif(norm_prob):
    """
    Seleciona aleatoriamente um *motif* com base em uma distribuição de probabilidade.

    Parâmetros:
    -----------
    norm_prob : dict
        Dicionário com probabilidades normalizadas para cada *motif*.

    Retorna:
    --------
    str
        *Motif* selecionado.
    """
    return random.choices(list(norm_prob.keys()), weights=list(norm_prob.values()))[0]

def algoritmo_motif(seqs, tam_motif, max_iter=100, stagnation_limit=10):
    """
    Executa o algoritmo de identificação de *motifs* baseado em amostragem probabilística.

    Parâmetros:
    -----------
    seqs : list of str
        Lista de sequências de DNA.
    tam_motif : int
        Comprimento do *motif* a ser identificado.
    max_iter : int, opcional
        Número máximo de iterações do algoritmo (padrão: 100).
    stagnation_limit : int, opcional
        Número máximo de iterações sem melhoria no escore antes de parar (padrão: 10).

    Retorna:
    --------
    list of str
        Lista com os melhores *motifs* encontrados.
    float
        Melhor escore alcançado durante a execução.
    """
    num_seqs = len(seqs)
    start_pos, limite = inicializar_posicoes_aleatorias(seqs, tam_motif)

    best_motifs = []
    best_score = float('-inf')
    stagnation_count = 0

    for iteration in range(max_iter):
        excluir_idx = random.randint(0, num_seqs - 1)
        seq_excluida = seqs[excluir_idx]

        PWM, motifs = construir_pwm(seqs, start_pos, tam_motif, excluir_idx)
        norm_prob, prob_motif = calcular_probabilidades_motifs(seq_excluida, PWM, tam_motif, limite)

        novo_motif = selecionar_motif(norm_prob)
        nova_pos = seq_excluida.find(novo_motif)
        if nova_pos != -1:
            start_pos[excluir_idx] = nova_pos

        score_atual = sum(prob_motif.values())

        if score_atual > best_score:
            best_score = score_atual
            best_motifs = motifs[:excluir_idx] + [novo_motif] + motifs[excluir_idx:]
            stagnation_count = 0
        else:
            stagnation_count += 1

        if stagnation_count >= stagnation_limit:
            print(f"Parou por estagnação após {iteration + 1} iterações.")
            break

    return best_motifs, best_score

def validar_sequencias(seqs):
    """
    Valida se todas as sequências contêm apenas as bases A, T, C e G.

    Parâmetros:
    -----------
    seqs : list of str
        Lista de sequências de DNA a serem validadas.

    Lança:
    ------
    ValueError
        Se alguma sequência contiver caracteres inválidos.
    """
    for seq in seqs:
        if not all(base in "ATCG" for base in seq):
            raise ValueError(f"Sequência inválida detectada: {seq}. Apenas caracteres A, T, C e G são permitidos.")

def main():
    """
    Função principal que executa o pipeline de validação e busca de *motifs* em um conjunto de sequências exemplo.
    """
    seqs = "GTAAACAATATTTATAGC AAAATTTACCTCGCAAGG CCGTACTGTCAAGCGTGG TGAGTAAACGACGTCCCA TACTTAACACCCTGTCAA".split()
    tam_motif = 8

    validar_sequencias(seqs) 

    best_motifs, best_score = algoritmo_motif(seqs, tam_motif)
    print("Melhores motifs encontrados:", best_motifs)
    print("Melhor score:", best_score)

if __name__ == "__main__":
    main()
