from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pyshadow.main import Shadow
import os
import time
from copy import deepcopy
import random
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.chrome.options import Options

accented_letters = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e", "í": "i", "ó": "o", "ô": "o", "õ": "o", "ú": "u", "ü": "u", "ç": "c", 'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y','z': 'z', 'ï' : 'i'}

dirname = os.path.dirname(__file__)
file = open(os.path.join(dirname, "Palavras/real_five_letters.txt"), "r", encoding="utf-8")
dicio = file.read().splitlines()
file.close()

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

def verificar_letra(texto):
    lista = texto.split()
    if len(lista) > 3:
        return 1, accented_letters[lista[1][1].lower()]
    elif lista[2] == 'correta':
        return 2, accented_letters[lista[1][1].lower()]
    elif lista[2] == 'errada':
        return 0, accented_letters[lista[1][1].lower()]

def pesquisa(dicio, atuais, informacao):
    tem = informacao[0]
    nao_tem = informacao[1]
    nao = informacao[2]
    sim = informacao[3]


    if atuais != []:
        for i in range(5):
            if atuais[i][0] == 0 and atuais[i][1] not in tem:
                nao_tem.append(atuais[i][1])
            elif atuais[i][0] == 1:
                tem.append(atuais[i][1])
                nao[i].append(atuais[i][1])
            elif atuais[i][0] == 2:
                tem.append(atuais[i][1])
                sim[i].append(atuais[i][1])
    
    final = []

    for word in dicio:
        if has_certain_characters(word, tem) and doesnt_have_certain_characters(word, nao_tem) and doesnt_have_certain_characters(word[0], nao[0]) and doesnt_have_certain_characters(word[1], nao[1]) and doesnt_have_certain_characters(word[2], nao[2]) and doesnt_have_certain_characters(word[3], nao[3]) and doesnt_have_certain_characters(word[4], nao[4]) and has_certain_characters(word[0], sim[0]) and has_certain_characters(word[1], sim[1]) and has_certain_characters(word[2], sim[2]) and has_certain_characters(word[3], sim[3]) and has_certain_characters(word[4], sim[4]):
            final.append(word)

    everything = [tem, nao_tem, nao, sim]

    return final, everything
    
def count_letters(lista, tem):
    count = {'a': 0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}

    for word in lista:
        for letter in word:
            if accented_letters[letter] not in tem:
                count[accented_letters[letter]] += 1

    return count

def check_errada(element):
    texto = element.get_attribute('style')
    return 'normal' in texto
    
def counter(how_many, lista, ter):
    count_all = {'a': 0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}

    count = []
    for i in range(how_many):
        count.append(count_letters(lista[i], ter))
    
    for i in range(how_many):
        for j in count[i]:
            count_all[j] += count[i][j]
    
    letters_count = []
    for i in count_all.keys():
        letters_count.append([i, count_all[i]])
    letters_count.sort(key=lambda x: x[1], reverse=True)

    return letters_count


def solucionar_multiplos(shadow, driver, dicio, input_field, how_many):
    lista = []
    for i in range(how_many):
        lista.append(deepcopy(dicio))

    cont = -1

    wrong_checker = shadow.find_element('div[aria-live="assertive"]')

    informacao = [[] for i in range(how_many)]
    for i in range(how_many):
        aux = [[] for i in range(4)]
        aux[2] = [[] for i in range(5)]
        aux[3] = [[] for i in range(5)]
        informacao[i] = deepcopy(aux)
    certo = [False for i in range(how_many)]
    check = [False for i in range(how_many)]
    while sum([len(lista[i]) for i in range(how_many)]) != how_many:
        cont += 1
        time.sleep(2)
        row_board = []
        board = 0
        for i in range(how_many):
            element = shadow.find_element('wc-board[id="board' + str(i) + '"]')
            row = [shadow.find_element(element, 'div[lid="0"][termo-row="%i"]' % cont), shadow.find_element(element,'div[lid="1"][termo-row="%i"]' % cont), shadow.find_element(element,'div[lid="2"][termo-row="%i"]' % cont), shadow.find_element(element,'div[lid="3"][termo-row="%i"]' % cont), shadow.find_element(element,'div[lid="4"][termo-row="%i"]' % cont)]
            row_board.append(row)

        atuais = []

        for i in row_board:
            info = []
            for j in range(5):
                aux = i[j].get_attribute('aria-label')
                if aux != '':
                    info.append(verificar_letra(aux))
            atuais.append(info)
        
        print(atuais)
        
        for i in range(how_many):
            lista[i], informacao[i] = pesquisa(lista[i], atuais[i], informacao[i])
        
        print(informacao)

        ter = []

        lenghtt = []
        for i in range(how_many):
            lenghtt.append(len(lista[i]))

        indice = lenghtt.index(max(lenghtt))


        for j in informacao[indice][0]:
            ter.append(j)
        for j in informacao[indice][1]:
            ter.append(j)

        ter = []
        for i in range(how_many):
            if not(check[i]):
                for j in informacao[i][0]:
                    ter.append(j)
                for j in informacao[i][1]:
                    ter.append(j)

        quant_letras = 3
        palavras = ['']
        sair = False
        
        while len(palavras) != 0 and not(sair):
            passou = 0
            passou_ter = 0
            this = False
            passou_la = 0
            while (len(palavras) == 0 or palavras == ['']) and not(any(certo)):
                
                letters_count = counter(how_many, lista, ter)

                aux_inf = [[] for i in range(4)]
                aux_inf[2] = [[] for i in range(5)]
                aux_inf[3] = [[] for i in range(5)]

                letras = letters_count[:5]

                letras_selecionadas = [i[0] for i in letras]
                letters = []
                letters.append(letras_selecionadas.pop(0))
                if not(this):
                    for i in letras_selecionadas:
                        letters.append(i)
                        this = True
                else:
                    if passou_la == 0:
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(0))
                        passou_la += 1
                    elif passou_la == 1:
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(0))
                        passou_la += 1
                    elif passou_la == 2:
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(1))
                        passou_la += 1
                    elif passou_la == 3:
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(1))
                        letters.append(letras_selecionadas.pop(1))
                        passou_la += 1
                    elif passou_la == 4:
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(0))
                        passou_la += 1
                    elif passou_la == 5:
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(1))
                        passou_la += 1
                    elif passou_la == 6:
                        letters.append(letras_selecionadas.pop(0))
                        letters.append(letras_selecionadas.pop(2))
                        passou_la += 1
                    elif passou_la == 7:
                        letters.append(letras_selecionadas.pop(1))
                        letters.append(letras_selecionadas.pop(1))
                        letters.append(letras_selecionadas.pop(1))
                        passou_la += 1
                    elif passou_la == 8:
                        letters.append(letras_selecionadas.pop(1))
                        letters.append(letras_selecionadas.pop(1))
                        passou_la += 1
                    elif passou_la == 9:
                        letters.append(letras_selecionadas.pop(0))
                        passou_la += 1
                    elif passou_la == 10:
                        letters.append(letras_selecionadas.pop(1))
                        letters.append(letras_selecionadas.pop(2))
                        passou_la += 1
                    else:
                        ter = []
                        for i in range(how_many):
                            for j in informacao[i][0]:
                                ter.append(j)
                        passou_la = 0

                print(letras_selecionadas)
                print(letters)

                aux_inf[0] = letters

                palavras, aux = pesquisa(dicio, [], aux_inf)

            denovo = True
            while denovo and not(any(certo)) and len(palavras) != 0:
                let = [i for i in letters_count if i[1] > 0]
                let = [i[0] for i in let]
                palavres = []
                for i in palavras:
                    word_without_accents = ""
                    for letter in i:
                        word_without_accents += accented_letters[letter]
                    for j in range(5):
                        if word_without_accents[j] not in let:
                            break
                        if j == 4:
                            palavres.append(i)
                if palavres == []:
                    palavres = palavras
                palavra = palavres[palavres.index(random.choice(palavres))]
                word_without_accents = ""
                for letter in palavra:
                    word_without_accents += accented_letters[letter]
                input_field.send_keys(word_without_accents)
                input_field.send_keys(Keys.ENTER)
                denovo = False
                sair = True
            for i in range(how_many):
                print(len(lista[i]))
            for i in range(how_many):
                if len(lista[i]) == 1 and check[i] == False:
                    certo[i] = True
            print(certo)
            if any(certo):
                    sair = True
        length = [len(lista[i]) for i in range(how_many)]
        time.sleep(1)
        while True in certo:
            for i in range(how_many):
                if certo[i] == True:
                    time.sleep(2)
                    word_without_accents = ''

                    for letter in lista[i][0]:
                        word_without_accents += accented_letters[letter]
                    input_field.send_keys(word_without_accents)
                    input_field.send_keys(Keys.ENTER)

                    certo[i] = False
                    check[i] = True
            cont += 1

def solucionar(shadow, dicio, input_field):
    lista = deepcopy(dicio)
    cont = 0

    wrong_checker = shadow.find_element('div[aria-live="assertive"]')

    informacao = [[] for i in range(4)]
    informacao[2] = [[] for i in range(5)]
    informacao[3] = [[] for i in range(5)]
    


    while len(lista) != 1:

        time.sleep(1)

        row = [shadow.find_element('div[lid="0"][termo-row="%i"]' % cont), shadow.find_element('div[lid="1"][termo-row="%i"]' % cont), shadow.find_element('div[lid="2"][termo-row="%i"]' % cont), shadow.find_element('div[lid="3"][termo-row="%i"]' % cont), shadow.find_element('div[lid="4"][termo-row="%i"]' % cont)]

        atuais = []
        for i in row:
            info = (i.get_attribute('aria-label'))
            atuais.append(verificar_letra(info))
        
        lista, informacao = pesquisa(lista, atuais, informacao)
        quant_letras = 5
        palavras = ['']
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
                aux_inf = [[] for i in range(4)]
                aux_inf[2] = [[] for i in range(5)]
                aux_inf[3] = [[] for i in range(5)]
                letras = letters_count[:5]
                letras_selecionadas = random.sample(letras, quant_letras)
                letras_selecionadas = [i[0] for i in letras_selecionadas]
                aux_inf[0] = letras_selecionadas
                palavras, aux = pesquisa(dicio, [], aux_inf)
                if len(palavras) == 0 and quant_letras > 3:
                    quant_letras -= 1
                elif quant_letras == 3 and passou == 5:
                    quant_letras = 4
                    passou += 1
                else:
                    ter = deepcopy(informacao[0])

            denovo = True
            print("Tem um total de:", len(lista), "palavras.")
            while denovo and len(lista) != 1 and len(palavras) != 0:
                palavra = palavras.pop(palavras.index(random.choice(palavras)))
                word_without_accents = ""
                for letter in palavra:
                    word_without_accents += accented_letters[letter]
                input_field.send_keys(word_without_accents)
                input_field.send_keys(Keys.ENTER)
                if check_errada(wrong_checker):
                    denovo = True
                    input_field.send_keys(Keys.BACKSPACE)
                    input_field.send_keys(Keys.BACKSPACE)
                    input_field.send_keys(Keys.BACKSPACE)
                    input_field.send_keys(Keys.BACKSPACE)
                    input_field.send_keys(Keys.BACKSPACE)
                else:
                    denovo = False
                    sair = True
                time.sleep(0.2)
            if len(lista) == 1:
                sair = True
            cont += 1
            time.sleep(0.2)

    word_without_accents = ''

    for letter in lista[0]:
        word_without_accents += accented_letters[letter]
        
    input_field.send_keys(word_without_accents)
    input_field.send_keys(Keys.ENTER)

PATH = "C:\Program Files (x86)\chromedriver.exe"

#chromeOptions = Options()
#chromeOptions.add_argument("")
driver = webdriver.Chrome(PATH)
shadow = Shadow(driver)

driver.get("https://term.ooo/")

time.sleep(2)

elem = driver.find_element_by_tag_name("html")

ac = ActionChains(driver)

ac.move_to_element(elem).click().perform()

time.sleep(2)

element = driver.find_element_by_tag_name("body")

element.send_keys("serao")

element.send_keys(Keys.ENTER)

time.sleep(2)

solucionar_multiplos(shadow, driver, dicio, element, 1)

time.sleep(3)

duo = shadow.find_element('a[id="duo"]')

duo.click()

time.sleep(1)

elem = driver.find_element_by_tag_name("html")

ac.move_to_element(elem).click().perform()

element = driver.find_element_by_tag_name("body")

element.send_keys("serao")

element.send_keys(Keys.ENTER)

solucionar_multiplos(shadow, driver, dicio, element, 2)

time.sleep(3)

quarteto = shadow.find_element('a[id="quatro"]')

quarteto.click()

time.sleep(1)

element = driver.find_element_by_tag_name("body")

elem = driver.find_element_by_tag_name("html")

ac.move_to_element(elem).click().perform()

element.send_keys("serao")

element.send_keys(Keys.ENTER)

solucionar_multiplos(shadow, driver, dicio, element, 4)

time.sleep(5)

driver.quit()
