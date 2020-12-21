# Deber 5 - Matriz de Similitudes

import collections
import math
# Integrantes: Andrade Carlos
#             Coba Alexander
#             Sánchez Sthefany
#             Vega Stalin
import os
import re

import nltk
# trabajar con matrices
import numpy as np
import pandas as pd

from core_project.settings import BASE_DIR

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

porter = PorterStemmer()
from timeit import default_timer as timer


# NLP

def NLP(lista):
    t2 = []
    stopW = list(stopwords.words(['english']))
    for i in range(len(lista)):
        if isinstance(lista[i], str):
            f2 = lista[i].lower()
            f3 = re.sub('[^A-Za-z]+', ' ', f2)
            f4 = f3.split()
            token = [w for w in f4 if not w in stopW]
            Aporter = [porter.stem(i) for i in token]
            t2.append(Aporter)

    return t2


# Comparacion

def comparacion(clave, frase):
    # El método enumerate () agrega un contador a un iterable y lo devuelve
    c = [i for i, x in enumerate(frase) if x == clave]
    for i in range(len(c)):
        c[i] = c[i] + 1
    return c


def creaFrase(listadelistas):
    frase = []
    for r in listadelistas:
        doc = ""
        for i in r:
            doc += i + " "
        frase.append(doc)
    return frase


def diccionario(lista):
    diccionario = {}

    f1 = creaFrase(lista)
    for i in range(len(f1)):
        f3 = f1[i].split()
        f5 = dict(collections.Counter(f3))
        for clave in f5:
            if diccionario.get(clave) == None:
                diccionario.setdefault(clave, [[i + 1, f5[clave], comparacion(clave, f3)]])
            else:
                valor = diccionario.pop(clave)
                valor.append([i + 1, f5[clave], comparacion(clave, f3)])
                diccionario.update({clave: valor})

    return diccionario


def unirFrase(listapalabras):
    frase = ""
    for i in listapalabras:
        frase = frase + " " + i
    return frase


def jaccard(val1, val2):
    val1 = unirFrase(val1)
    val2 = unirFrase(val2)
    str1 = set(val1.split())
    str2 = set(val2.split())
    return float(len(str1 & str2)) / len(str1 | str2)


def Mjaccard(nlp):
    matriz = []
    for i in range(len(nlp)):
        matriz.append([])
        for j in range(len(nlp)):
            dist = jaccard(nlp[i], nlp[j])
            matriz[i].append(dist)
    return matriz


def TF(dic, abs):
    matrizTF = []
    cont = 0
    for i in dic:
        matrizTF.append([])
        for j in range(len(abs)):
            if i in abs[j]:
                lista = dic[i]

                for r in lista:

                    if (j + 1) == r[0]:
                        matrizTF[cont].append(r[1])
            else:
                matrizTF[cont].append(0)
        cont = cont + 1
    return matrizTF


def MDF(diccionario):
    matrizDF = []
    for r in diccionario:
        matrizDF.append(len(diccionario[r]))
    return matrizDF


def peso_tf(ma):
    matriz_pesoTF = []
    for i in range(len(ma)):
        matriz_pesoTF.append([])
        for j in range(len(ma[0])):
            if ma[i][j] > 0:
                x = 1 + math.log10(ma[i][j])
                matriz_pesoTF[i].append(x)
            else:
                x = 0
                matriz_pesoTF[i].append(x)
    return matriz_pesoTF


def peso_idf(lis, n):
    matriz_pesoDF = []

    for i in range(len(lis)):
        l = math.log10(n / lis[i])
        matriz_pesoDF.append(l)
    return matriz_pesoDF


def tf_idf(lis, mat):
    matriz_tfidf = []
    for i in range(len(lis)):
        matriz_tfidf.append([])
        for j in range(len(mat[0])):
            matriz_tfidf[i].append(lis[i] * mat[i][j])
    return matriz_tfidf


def norm(pTF, x):
    aux = 0
    for i in range(len(pTF)):
        aux = aux + pow(pTF[i][x], 2)
    return math.sqrt(aux)


def matrizNorm(tf, pesoTFIDF):
    matriz_norma = []
    for i in range(len(tf[0])):
        matriz_norma.append([])
        norma = norm(pesoTFIDF, i)
        for j in range(len(pesoTFIDF)):
            matriz_norma[i].append(pesoTFIDF[j][i] / norma)

    return matriz_norma


def ppunto(x, y):
    aux = 0
    for i in range(len(x)):
        aux = aux + (x[i] * y[i])
    return aux


def matrizCos(matNorm):
    matriz_coseno = []
    for i in range(len(matNorm)):
        matriz_coseno.append([])
        indice = matNorm[i]
        for j in range(len(matNorm)):
            matriz_coseno[i].append(round(ppunto(indice, matNorm[j]), 2))
    return matriz_coseno


def matrizPonderacion(matabs, matkey, mattit):
    MatPtot = []
    for i in range(len(matabs)):
        MatPtot.append([])
        for j in range(len(matabs[0])):
            matabsdef = matabs[i][j] * 0.5
            matkeydef = matkey[i][j] * 0.4
            mattitdef = mattit[i][j] * 0.1

            suma = matabsdef + matkeydef + mattitdef
            MatPtot[i].append(round(suma, 3))

    return MatPtot


def get_vars():
    start = timer()
    filepath = os.path.join(BASE_DIR, 'static/data.csv')  # Seleccionando archivo que contiene la data
    repositorio = pd.read_csv(filepath)
    abstracts = pd.unique(repositorio['abstract'])
    nlp_abstracts = NLP(abstracts)

    bolsa_palabras = diccionario(nlp_abstracts)

    matriz_tf = TF(bolsa_palabras, nlp_abstracts)
    matriz_pesoTF = peso_tf(matriz_tf)

    lista_df = MDF(bolsa_palabras)
    lista_pesoIDF = peso_idf(lista_df, len(matriz_tf[0]))
    TF_IDF = tf_idf(lista_pesoIDF, matriz_pesoTF)

    mn = matrizNorm(matriz_tf, TF_IDF)
    mc = matrizCos(mn)

    # titulos = pd.unique(repositorio['title'])
    # keywords = pd.unique(repositorio['keywords'])
    # nlp_titulos = NLP(titulos)
    # nlp_keywords = NLP(keywords)
    # matriz_dist_keywords = Mjaccard(nlp_keywords)
    # matriz_dist_titulos = Mjaccard(nlp_titulos)
    # matriztotal = matrizPonderacion(mc, matriz_dist_keywords, matriz_dist_titulos)
    # matriz_final = np.array(matriztotal)

    # print("************ Matriz  de Similitud *****************")
    # print("numero de filas: ", len(matriz_final))
    # print("numero de columnas", len(matriz_final[0]))
    # print(matriz_final)

    end = timer()

    # print("===================== TIEMPO DE EJECUCION ================================")

    tiempo_ejecucion = (end - start)
    # print('El tiempo fue:', tiempo_ejecucion, "seg")
    return {
        'mc': mc,
        'tf_idf': TF_IDF,
        'seconds': tiempo_ejecucion,
    }


if __name__ == '__main__':
    get_vars()
