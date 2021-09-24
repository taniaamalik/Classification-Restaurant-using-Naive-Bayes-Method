from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import pandas as pd
import nltk
import re
import string
# import stopwords
# import punkt

def testing(komentar, myConProb, termsMain, resultBoolean, inputKomentar):
    
    commentCaseFolding = komentar.translate(str.maketrans('', '', string.punctuation)).lower()
    commentToken = nltk.tokenize.word_tokenize(commentCaseFolding)
    listStopword = set(stopwords.words('english'))

    commentStopword = []
    for word in commentToken:
        if word not in listStopword:
            commentStopword.append(word)

    st = PorterStemmer()

    listStem = []
    for word in commentStopword:
        listStem.append(st.stem(word))

    termsNewDocument = []
    for word in listStem:
        if word not in termsNewDocument:
            termsNewDocument.append(word)

    usedTerms = []
    for term in termsNewDocument:
        if term in termsMain:
            usedTerms.append(term)

    usedTermsWithConProb = {}
    for term in usedTerms:
        temp = []
        temp.append(myConProb[term][0])
        temp.append(myConProb[term][1])
        usedTermsWithConProb[term] = temp

    def getTotalDocument():
        return len(inputKomentar)

    def getTotalDocumentWithSpecificCategory(category):
        if category == 1:
            return int(len(inputKomentar)/2)
        elif category == 0:
            return int(len(inputKomentar)/2)
        else:
            return 0

    probabiltyPositif = getTotalDocumentWithSpecificCategory(
        1) / getTotalDocument()
    probabiltyNegatif = getTotalDocumentWithSpecificCategory(
        0) / getTotalDocument()

    positif = 1
    negatif = 1
    
    for term in usedTerms:
        positif *= usedTermsWithConProb[term][0]
        negatif *= usedTermsWithConProb[term][1]

    positif = positif * probabiltyPositif
    negatif = negatif * probabiltyNegatif

    finalResult = True if positif > negatif else False

    expectedResult = 'Positif' if resultBoolean == True else 'Negatif'
    outputResult = 'Positif' if finalResult == True else 'Negatif'
    nitip = [komentar, expectedResult, outputResult]
    print()
    print('Komentar yang diuji : ' + komentar)
    print('Expected Result : ' + expectedResult)
    print('Output Result : ' + outputResult)

    returnvalue = [nitip,finalResult == resultBoolean]
    return returnvalue
