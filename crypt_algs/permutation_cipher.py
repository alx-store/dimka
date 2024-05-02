import math


def encrypt_per(plain_text,  key):
    
    if key == 0:
        raise ZeroDivisionError

    text = []
    for letter in plain_text:
        text.append(letter)

    while len(text) % 4 != 0:
        text.append("_")

    text = [text[i : i + 4] for i in range(0, len(text), 4)]

    cipher = []
    tmp = 0
    for count in range(math.ceil(len(text) / key)):
        if len(text[count * key :]) < (key):
            new_key = len(text[count * key :])

            for s_count in range(new_key):
                cipher.append(text[s_count + tmp][1])

            for s_count in range(new_key):
                cipher.append(text[s_count + tmp][0])
                cipher.append(text[s_count + tmp][2])

            for s_count in range(new_key):
                cipher.append(text[s_count + tmp][3])

        else:
            for s_count in range(key):
                cipher.append(text[s_count + tmp][1])

            for s_count in range(key):
                cipher.append(text[s_count + tmp][0])
                cipher.append(text[s_count + tmp][2])

            for s_count in range(key):
                cipher.append(text[s_count + tmp][3])

        tmp += key
    return "".join(cipher)


def decrypt_per(pre_cipher, key, alph):

    if len(pre_cipher) % 4 != 0:
        raise IndexError
    
    if key == 0:
        raise ZeroDivisionError

    for symb in pre_cipher:
        if not (symb in alph):
            raise ValueError("Неверно указаны аргументы для алгоритма")

    cipher = []
    for letter in pre_cipher:
        cipher.append(letter)

    text = [["", "", "", ""] for i in range(len(cipher) // 4)]
    tmp = 0

    for count in range(math.ceil(len(cipher) / (key * 4))):

        if len(cipher[count * key * 4 :]) < (key * 4):
            new_key = len(cipher[count * key * 4 :]) // 4

            for s_count in range(new_key):
                text[s_count + tmp][1] = cipher[s_count + tmp * 4]

            s_tmp = 0
            for s_count in range(new_key):
                text[s_count + tmp][0] = cipher[new_key + s_tmp + tmp * 4]
                text[s_count + tmp][2] = cipher[new_key + s_tmp + tmp * 4 + 1]
                s_tmp += 2

            for s_count in range(new_key):
                text[s_count + tmp][3] = cipher[new_key * 3 + s_count + tmp * 4]

        else:
            for s_count in range(key):
                text[s_count + tmp][1] = cipher[s_count + tmp * 4]

            s_tmp = 0
            for s_count in range(key):
                text[s_count + tmp][0] = cipher[key + s_tmp + tmp * 4]
                text[s_count + tmp][2] = cipher[key + s_tmp + tmp * 4 + 1]
                s_tmp += 2

            for s_count in range(key):
                text[s_count + tmp][3] = cipher[key * 3 + s_count + tmp * 4]

        tmp += key

    str_text = ""

    for i in text:
        str_text += "".join(i)

    return str_text
