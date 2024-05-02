def matrix_gen(l_len, c_len, alph, key):
    matrix = []
    line = []

    for count in range(l_len):
        line.append("")

    for count in range(c_len):
        matrix.append(line)

    for symb in key:
        if not (symb in alph):
            return None

    new_alph = []
    for letter in key:
        if not (letter in new_alph):
            new_alph.append(letter)

    for letter_sec in alph:
        if not (letter_sec) in new_alph:
            new_alph.append(letter_sec)

    matrix = [new_alph[i : i + l_len] for i in range(0, len(new_alph), l_len)]

    return matrix


def encrypt_rep(alph, line, column, key, text):

    for symb in text:
        if not (symb in alph):
            raise ValueError("Неверно указаны аргументы для алгоритма")

    matrix = matrix_gen(line, column, alph, key)
    if matrix == None:
        return matrix

    cipher = ""
    for letter in text:
        for counter in range(0, len(matrix), 1):
            if letter in matrix[counter]:
                cipher += matrix[(counter + 1) % (len(matrix))][
                    matrix[counter].index(letter)
                ]
    return cipher


def decrypt_rep(alph, line, column, key, cipher):

    matrix = matrix_gen(line, column, alph, key)
    if matrix == None:
        return matrix

    plain_text = ""
    for letter in cipher:
        for counter in range(0, len(matrix), 1):
            if letter in matrix[counter]:
                if (counter - 1) < 0:
                    plain_text += matrix[len(matrix) - 1][matrix[counter].index(letter)]
                else:
                    plain_text += matrix[(counter - 1)][matrix[counter].index(letter)]
    return plain_text
