import random
from alpha import pesquisa
import jsonpickle
from copy import deepcopy
import os

accented_letters = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e", "í": "i", "ó": "o", "ô": "o", "õ": "o", "ú": "u", "ü": "u", "ç": "c", 'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y','z': 'z', 'ï' : 'i'}

def count_letters(lista, tem):
    count = {'a': 0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}

    for word in lista:
        for letter in word:
            if accented_letters[letter] not in tem:
                count[accented_letters[letter]] += 1

    return count

def solve_termo(opcao, dicio):
    if opcao == 1:
        print("Use a palavra \"CRANE\" primeiro:")
    else:
        print("Use a palavra \"SERÃO\" ou \"RÓSEA\" primeiro.")
    print("Digite as informações mostradas no jogo:")
    lista = dicio
    informacao = [[] for i in range(12)]
    cont = 0
    while len(lista) != 1:
        lista, informacao = pesquisa(lista, False, True, informacao, cont)
        cont += 1
        palavras = ['']
        quant_letras = 5
        sair = False
        ter =  deepcopy(informacao[0])
        for i in informacao[1]:
            ter.append(i)
        while len(palavras) != 0 and not(sair):
            passou = 0
            while len(palavras) == 0 or palavras == ['']:
                count = count_letters(lista, ter)
                letters_count = []
                for letter in count.keys():
                    letters_count.append([letter, count[letter]])
                letters_count.sort(key=lambda x: x[1], reverse=True)
                aux_inf = [[] for i in range(12)]
                letras = letters_count[:5]
                letras_selecionadas = random.sample(letras, quant_letras)
                letras_selecionadas = [i[0] for i in letras_selecionadas]
                aux_inf[0] = letras_selecionadas
                palavras, aux = pesquisa(dicio, False, False, aux_inf, 0)
                if len(palavras) == 0 and quant_letras > 3:
                    quant_letras -= 1
                elif quant_letras == 3 and passou == 5:
                    quant_letras = 4
                    passou += 1
                else:
                    ter = deepcopy(informacao[0])


            #print a random word from palavras
            denovo = True
            print("Tem um total de:", len(lista), "palavras.")
            while denovo and len(lista) != 1 and len(palavras) != 0:
                palavra = palavras.pop(palavras.index(random.choice(palavras)))
                print("Tente essa palavra: ", palavra)
                print("Essa palavra funcionou? (S/N)")
                resposta = input().upper()
                if resposta == 'S':
                    denovo = False
                    sair = True
                else:
                    denovo = True
            if len(lista) == 1:
                sair = True

    print("Sua palavra é: ", lista[0])

def chechar_palavras_todas_letras(dicio):
    #list with all letter

    file = open("C:/Users/ianga/letras_nao_tem.json", "w+", encoding="utf-8")

    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    letras_nao_tem = []

    cont = 0

    for letter in letras:
        for letter2 in letras:
            for letter3 in letras:
                if letter != letter2 and letter != letter3 and letter2 != letter3:
                    palavras, tem = pesquisa(dicio, False, False, [letter, letter2, letter3])
                    if len(palavras) == 0:
                        letras_nao_tem.append([letter, letter2, letter3])
                    print(cont)
                    cont += 1
    
    encodado = jsonpickle.encode(letras_nao_tem)

    file.write(encodado)

    print('Fim')

def contar_letras():

    file = open("C:/Users/ianga/letras_nao_tem.json", "r", encoding="utf-8")
    letras_nao_tem = jsonpickle.decode(file.read())
    file.close()

    count = {'a': 0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}

    for letter in letras_nao_tem:
        for letter2 in letter:
            count[letter2] += 1
    
    letters_count = []

    for letter in count.keys():
            letters_count.append([letter, count[letter]])
    
    letters_count.sort(key=lambda x: x[1], reverse=True)

    for i in letters_count:
        print(i[0], i[1])    
    
    




print("BEM-VINDO AO SISTEMA DE SOLUÇÃO DO TERMO")

continuar = True

while continuar:
    dirname = os.path.dirname(__file__)
    print('Você deseja usar o Wordle ou o Termo?'
          '\n1 - Wordle'
          '\n2 - Termo'
          )
    opcao = int(input())
    if opcao == 1:
        file = open(os.path.join(dirname, "Palavras/words.txt"), "r", encoding="utf-8")
        dicio = file.read().splitlines()
        file.close()
    else:
        file = open(os.path.join(dirname, "Palavras/five_letters.txt"), "r", encoding="utf-8")
        dicio = file.read().splitlines()
        file.close()

    print('O que deseja fazer?\n'
          '1 - Pesquisar Termo\n'
          '2 - Solução\n'
          '3 - Sair'
          )
    opc = input()
    if opc == '1':
        informacao = [[] for i in range(12)]
        pesquisa(dicio, True, True, informacao, 0)
    elif opc == '2':
        solve_termo(opcao, dicio)
    elif opc == '3':
        continuar = False
    elif opc == '4':
        chechar_palavras_todas_letras()
    elif opc == '5':
        contar_letras()