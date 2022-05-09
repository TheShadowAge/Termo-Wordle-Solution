import unicodedata

file = open("C:/Users/ianga/five_letters.txt", "r", encoding="utf-8")
dicio = []
for line in file:
    dicio.append(unicodedata.normalize('NFC', line.strip()))
file.close()

accented_letters = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e", "í": "i", "ó": "o", "ô": "o", "õ": "o", "ú": "u", "ü": "u", "ç": "c", 'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y','z': 'z', 'ï' : 'i'}

def has_certain_characters(word, characters):
    validate = []
    word_without_accents = ""
    for letter in word:
        word_without_accents += accented_letters[letter]
    if len(characters) == 0:
        return True
    for letter in characters:
        validate.append(letter in word_without_accents)
    if len(validate) > 0:
        return all(validate)
    return False

def doesnt_have_certain_characters(word, characters):
    validate = []
    word_without_accents = ""
    for letter in word:
        word_without_accents += accented_letters[letter]
    if len(characters) == 0:
        return True
    for letter in characters:
        validate.append(letter in word_without_accents)
    if len(validate) > 0:
        return not(any(validate))
    return True

def pesquisa(dicio, print_results, receive_information, informacao, cont):
    tem = informacao[0]
    nao_tem = informacao[1]
    nao1 = informacao[2]
    nao2 = informacao[3]
    nao3 = informacao[4]
    nao4 = informacao[5]
    nao5 = informacao[6]
    sim1 = informacao[7]
    sim2 = informacao[8]
    sim3 = informacao[9]
    sim4 = informacao[10]
    sim5 = informacao[11]

    if receive_information:
        print("Quais letras tem? (Digite em letra minúscula e sem acento, separadas por espaço) ")
        aux = input().split()
        for i in aux:
            tem.append(i)
        print("Quais letras não tem? (Digite em letra minúscula e sem acento, separadas por espaço) ")
        aux = input().split()
        for i in aux:
            nao_tem.append(i)
        print("Quais letras não tem na primeira letra? (Digite em letra minúscula e sem acento, separadas por espaço) ")
        aux = input().split()
        for i in aux:
            nao1.append(i)
        print("Quais letras não tem na segunda letra? (Digite em letra minúscula e sem acento, separadas por espaço) ")
        aux = input().split()
        for i in aux:
            nao2.append(i)
        print("Quais letras não tem na terceira letra? (Digite em letra minúscula e sem acento, separadas por espaço) ")
        aux = input().split()
        for i in aux:
            nao3.append(i)
        print("Quais letras não tem na quarta letra? (Digite em letra minúscula e sem acento, separadas por espaço) ")
        aux = input().split()
        for i in aux:
            nao4.append(i)
        print("Quais letras não tem na quinta letra? (Digite em letra minúscula e sem acento, separadas por espaço) ")
        aux = input().split()
        for i in aux:
            nao5.append(i)
        print("Qual letra tem na primeira letra? (Digite em letra minúscula e sem acento) ")
        aux = input().split()
        for i in aux:
            sim1.append(i)
        print("Qual letra tem na segunda letra? (Digite em letra minúscula e sem acento) ")
        aux = input().split()
        for i in aux:
            sim2.append(i)
        print("Qual letra tem na terceira letra? (Digite em letra minúscula e sem acento) ")
        aux = input().split()
        for i in aux:
            sim3.append(i)
        print("Qual letra tem na quarta letra? (Digite em letra minúscula e sem acento) ")
        aux = input().split()
        for i in aux:
            sim4.append(i)
        print("Qual letra tem na quinta letra? (Digite em letra minúscula e sem acento) ")
        aux = input().split()
        for i in aux:
            sim5.append(i)

    final = []

    for word in dicio:
        if has_certain_characters(word, tem) and doesnt_have_certain_characters(word, nao_tem) and doesnt_have_certain_characters(word[0], nao1) and doesnt_have_certain_characters(word[1], nao2) and doesnt_have_certain_characters(word[2], nao3) and doesnt_have_certain_characters(word[3], nao4) and doesnt_have_certain_characters(word[4], nao5) and has_certain_characters(word[0], sim1) and has_certain_characters(word[1], sim2) and has_certain_characters(word[2], sim3) and has_certain_characters(word[3], sim4) and has_certain_characters(word[4], sim5):
            final.append(word)
    if print_results:
        for word in final:
            print(word)

    informacao = [tem, nao_tem, nao1, nao2, nao3, nao4, nao5, sim1, sim2, sim3, sim4, sim5]

    return final, informacao


if __name__ == "__main__":
    pesquisa(dicio, True)