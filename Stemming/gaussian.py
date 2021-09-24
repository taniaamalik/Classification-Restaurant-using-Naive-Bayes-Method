from nltk.stem import PorterStemmer
from nltk.corpus import stopwords	
from math import sqrt
from math import pi
from math import exp
import pandas as pd
import nltk
import re
import string
# import punkt
import math
import csv

def testing(listTesting, meanPositif, meanNegatif, stdevPositif, stdevNegatif, priorPositif, priorNegatif):
    listComment = listTesting
    listCommentLower = listTesting
    for indexComment in range(0, len(listComment)):
        sentence = listComment[indexComment].translate(
            str.maketrans('', '', string.punctuation)).lower()
        listCommentLower[indexComment] = sentence

    listCommentAfterToken = []
    for comment in listCommentLower:
        tokenWord = nltk.tokenize.word_tokenize(comment)
        listCommentAfterToken.append(tokenWord)

    listStopword = set(stopwords.words('english'))

    listCommentStopwords = []

    for comment in listCommentAfterToken:
        notRemoved = []
        for word in comment:
            if word not in listStopword:
                notRemoved.append(word)
        listCommentStopwords.append(notRemoved)

    # CETAK STOPWORD REMOVAL
    # for comment in listCommentStopwords:
    #     print(str(comment))

    # print('')
    # print('=========================== Stemminng ===========================')
    # print('')

    st = PorterStemmer()

    listCommentStem = []

    for comment in listCommentStopwords:
        listStem = []
        for word in comment:
            listStem.append(st.stem(word))
        listCommentStem.append(listStem)

    # CETAK STEMMING
    # for test in listCommentStem:
    #     print(str(test))

    # #################################################################################
    # 5. TERM

    # MENGGABUNGKAN SEMUA TERM MENJADI SATU DAN MENGHILANGKAN TERM YANG BERSIFAT LEBIH DARI 1
    termsTesting = []
    for indexKomentar in range(0, len(listTesting)):
        for word in listCommentStem[indexKomentar]:
            if word not in termsTesting:
                termsTesting.append(word)

    # MEMBUAT METHOD UNTUK MENGHITUNG JUMLAH SUATU KATA DALAM SUATU DOKUMEN
    # KEPERLUAN RUMUS RAW TF

    def countWord(term, document):
        # documentArray = document.split(" ")
        count = 0
        for word in document:
            if term == word:
                count += 1
        return count

    myTerms = {}
    # print("\nTerm Frequency Weighting")
    for term in termsTesting:
        temp = []
        for indexKomentar in range(0, len(listCommentStem)):
            nitip = countWord(term, listCommentStem[indexKomentar])
            final = 0
            if nitip == 0:
                final = 0
            else:
                final = 1 + math.log(nitip, 10)
            temp.append(final)
        myTerms[term] = temp

    def pengecekan(wtf):
        count = 0
        for number in wtf:
            if number != 0:
                count += 1
        return count

    idf = []
    index = 0
    for word in termsTesting:
        temp = pengecekan(myTerms[word])
        idft = math.log(len(listTesting)/temp, 10)
        idf.append(idft)
        # print("IDF " + word + " = " + str(idf[index]))
        index += 1

    # (TF-IDF)
    tfidf = {}
    index = 0
    for term in termsTesting:
        temp = []
        for indexDocument in range(0, len(listTesting)):
            temp.append(myTerms[term][indexDocument] * idf[index])
        tfidf[term] = temp
        # print("TF-IDF " + term + " = " + str(tfidf[term]))
        index += 1
        # print(term+str(tfidf[term]))

    def calculate_probability(x, mean, stdev):
	    exponent = exp(-((x-mean)**2 / (2 * stdev**2 )))
	    return (1 / (sqrt(2 * pi) * stdev)) * exponent

    likelihood = {}
    for indexComment in range (len(listComment)):
        temp = []
        calculate_probabilityPositif = 10**300
        calculate_probabilityNegatif = 10**300
        for term in termsTesting:
            # print('cek calculate ' + str(calculate_probability(tfidf[term][indexComment],meanPositif,stdevPositif)))
            calculate_probabilityPositif = calculate_probabilityPositif * calculate_probability(tfidf[term][indexComment],meanPositif,stdevPositif)
            calculate_probabilityNegatif = calculate_probabilityNegatif * calculate_probability(tfidf[term][indexComment],meanNegatif,stdevNegatif)
            # print('cek ' +str(calculate_probabilityPositif))
        temp.append(calculate_probabilityPositif * priorPositif)
        temp.append(calculate_probabilityNegatif * priorNegatif)
        likelihood[indexComment] = temp
    
   
    akurasi = 0

    nitip = []
    for indexComment in range(len(likelihood)):
        komentar = listComment[indexComment]
        expectedResult = 'Positif' if indexComment % 2 == 0 else 'Negatif'
        actualResult = 'Positif' if likelihood[indexComment][0] > likelihood[indexComment][1] else 'Negatif'
        temp = [komentar, expectedResult, actualResult]
        nitip.append(temp)
        
        print('Komentar : ' + komentar)
        print('Expected Result : '+ expectedResult)
        print('Actual Result : '+ actualResult)
        print()
        
        # print('Probabilitas positif ' + str(likelihood[indexComment][0]))
        # print('Probabilitas negatif ' + str(likelihood[indexComment][1]))
        
        if expectedResult == actualResult:
            akurasi+=1

    print('Akurasi : '+str(akurasi))
    returnvalue = [akurasi, nitip]
    return returnvalue
        # result = 'Positif' if likelihood[indexComment][0] > likelihood[indexComment][1] else 'Negatif'
        # print('Document '+str(indexComment) + str(likelihood[indexComment])+result)

    
def gaussian(listTraining, listTesting):
    listComment = listTraining
    listCommentLower = listTraining
    for indexComment in range(0, len(listComment)):
        sentence = listComment[indexComment].translate(
            str.maketrans('', '', string.punctuation)).lower()
        listCommentLower[indexComment] = sentence

    # CETAK CASE FOLDING
    # for comment in range(0, len(listComment)):
    #     print(str(listCommentLower[comment]))

    # print('')
    # print('=========================== Tokenization ===========================')
    # print('')

    listCommentAfterToken = []
    for comment in listCommentLower:
        tokenWord = nltk.tokenize.word_tokenize(comment)
        listCommentAfterToken.append(tokenWord)

    # CETAK TOKENISASI
    # for comment in listCommentAfterToken:
    #     print(str(comment))

    # print('')
    # print('=========================== Stopword Removal ===========================')
    # print('')

    listStopword = set(stopwords.words('english'))

    listCommentStopwords = []

    for comment in listCommentAfterToken:
        notRemoved = []
        for word in comment:
            if word not in listStopword:
                notRemoved.append(word)
        listCommentStopwords.append(notRemoved)

    # CETAK STOPWORD REMOVAL
    # for comment in listCommentStopwords:
    #     print(str(comment))

    # print('')
    # print('=========================== Stemminng ===========================')
    # print('')

    st = PorterStemmer()

    listCommentStem = []

    for comment in listCommentStopwords:
        listStem = []
        for word in comment:
            listStem.append(st.stem(word))
        listCommentStem.append(listStem)

    # CETAK STEMMING
    # for test in listCommentStem:
    #     print(str(test))

    # #################################################################################
    # 5. TERM

    # MENGGABUNGKAN SEMUA TERM MENJADI SATU DAN MENGHILANGKAN TERM YANG BERSIFAT LEBIH DARI 1
    termsTraining = []
    for indexKomentar in range(0, len(listTraining)):
        for word in listCommentStem[indexKomentar]:
            if word not in termsTraining:
                termsTraining.append(word)

    # MEMBUAT METHOD UNTUK MENGHITUNG JUMLAH SUATU KATA DALAM SUATU DOKUMEN
    # KEPERLUAN RUMUS RAW TF

    def countWord(term, document):
        # documentArray = document.split(" ")
        count = 0
        for word in document:
            if term == word:
                count += 1
        return count

    myTerms = {}
    # print("\nTerm Frequency Weighting")
    for term in termsTraining:
        temp = []
        for indexKomentar in range(0, len(listCommentStem)):
            nitip = countWord(term, listCommentStem[indexKomentar])
            final = 0
            if nitip == 0:
                final = 0
            else:
                final = 1 + math.log(nitip, 10)
            temp.append(final)
        myTerms[term] = temp

    # IDF

    def pengecekan(wtf):
        count = 0
        for number in wtf:
            if number != 0:
                count += 1
        return count

    idf = []
    index = 0
    for word in termsTraining:
        temp = pengecekan(myTerms[word])
        idft = math.log(len(listTraining)/temp, 10)
        idf.append(idft)
        index += 1

    # (TF-IDF)
    tfidf = {}
    index = 0
    for term in termsTraining:
        temp = []
        for indexDocument in range(0, len(listTraining)):
            temp.append(myTerms[term][indexDocument] * idf[index])
        tfidf[term] = temp
        # print("TF-IDF " + word + " = " + str(tfidf[word]))
        index += 1
        # print(term+str(tfidf[term]))
    
    def countMean(numbers):
        return sum(numbers)/float(len(numbers))

    def countStdev(numbers):
        avg = countMean(numbers)
        variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
        return sqrt(variance)

    tfidfPositif = {}
    tfidfNegatif = {}
    for term in termsTraining:
        tempPositif = []
        tempNegatif = []
        for indexDocument in range(len(listTraining)):
            if indexDocument % 2 == 0:
                tempPositif.append(tfidf[term][indexDocument])
            else:
                tempNegatif.append(tfidf[term][indexDocument])
        tfidfPositif[term] = tempPositif
        tfidfNegatif[term] = tempNegatif
        # print(term + ' : ' + str(tfidfPositif[term]))

    sumtfidfPositif = []
    sumtfidfNegatif = []
    for term in termsTraining:
        sumtfidfPositif.append(sum(tfidfPositif[term]))
        sumtfidfNegatif.append(sum(tfidfNegatif[term]))
    
    meanPositif = countMean(sumtfidfPositif)
    meanNegatif = countMean(sumtfidfNegatif)
    stdevPositif = countStdev(sumtfidfPositif)
    stdevNegatif = countStdev(sumtfidfNegatif)

    priorPositif = (len(termsTraining)/2) / len(termsTraining)
    priorNegatif = (len(termsTraining)/2) / len(termsTraining)
    return testing(listTesting, meanPositif, meanNegatif, stdevPositif, stdevNegatif, priorPositif, priorNegatif)
