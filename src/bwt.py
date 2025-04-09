def bwt_transform(string):
    """
    Realiza a transformação de Burrows-Wheeler (BWT) de uma string.
    A string é rotacionada, ordenada lexicograficamente e a última coluna é extraída.
    """
    string+= '$'  # Adiciona o símbolo de fim de string
    n= len(string)
    
    # Criação das rotações da string
    rotations= [string[i:] + string[:i] for i in range(n)]
    rotations.sort()
    
    # Extração da última coluna das rotações
    bwt_result= ''.join(rotation[-1] for rotation in rotations)
    
    return bwt_result, rotations


def bwt_reverse_transform(string):
    """
    Reverte a transformação de Burrows-Wheeler (BWT) e reconstrói a string original.
    Utiliza o mapeamento Last-to-First (LF) para reconstrução.
    """
    n= len(string)
    first_col= sorted(string)
    
    # Criação do mapeamento Last-to-First (LF)
    count= {}
    lf_mapping= []
    for i in range(n):
        char= string[i]
        if char not in count:
            count[char]= 0
        first_index= first_col.index(char)
        lf_mapping.append(first_index + count[char])
        count[char]+= 1

    # Reconstrução da string original a partir do mapeamento LF
    result= []
    current= string.index('$')
    while len(result)< n:
        result.append(string[current])
        current= lf_mapping[current]

    return ''.join(reversed(result))

    # Exemplo de uso
string = input("Digite a string: ")
bwt_result, rotations = bwt_transform(string)
print(f"{string}'s BWT is: {bwt_result}")
print(f"{string}'s rotations are:\n" + "\n".join(rotations))
decoded = bwt_reverse_transform(bwt_result)
print(f"BWT {bwt_result} decoded: {decoded}")
