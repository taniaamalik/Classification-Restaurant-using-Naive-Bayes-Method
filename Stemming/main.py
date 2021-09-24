import testingMultinomial as tsM
import trainingMultinomial as trM
import gaussian as gaus
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import pandas as pd
import nltk
import re
import csv
import string
# import stopwords
# import punkt

output_excel = {}
indexOutput = 1

# method memanggil kelas training dengan metode gaussian
def gaussian(listTraining, listTesting):
    hasilBenar = gaus.gaussian(listTraining,listTesting)
    print('Hasil benar : ' + str(hasilBenar[0]) +
          ' / ' + str(len(listTesting)))
    akurasiPersentase = (hasilBenar[0]/len(listTesting)) * 100
    print('Akurasi Gaussian: ' + str(akurasiPersentase))
    print()
    return hasilBenar

# method untuk menjalankan metode multinomial dengan memanggil kelas training Multinomial dan testing
def multinomial(listTraining, listTesting):
    trainingReturnValue = trM.training(listTraining)
    myConProb = trainingReturnValue[0]
    termsMain = trainingReturnValue[1]

    indexOutput = len(output_excel)+1
    hasilBenar = 0
    totalKomentarTesting = len(listTesting)
    for indexKomentar in range(len(listTesting)):
        # proses untuk menemukan hasil expected
        positif = False
        if indexKomentar % 2 == 0:
            positif = True
        returnvalue = tsM.testing(listTesting[indexKomentar], myConProb, termsMain, positif, inputKomentar)
        output_excel[indexOutput] = returnvalue[0]
        indexOutput+=1
        if returnvalue[1]:
            hasilBenar += 1
    
    print()
    print('Hasil benar : ' + str(hasilBenar) +
          ' / ' + str(totalKomentarTesting))
    akurasiPersentase = (hasilBenar/totalKomentarTesting) * 100

    print('Akurasi Multinomial: ' + str(akurasiPersentase))
    listAkurasi.append(akurasiPersentase)
    print()
    print('#########################')
    print()

# inputDocument = pd.read_excel(
#     r'C:/Users/ASUS/Documents/FIX PROJEK AKHIR PENGPOL/Stemming/dataset.xlsx')
inputDocument = pd.read_excel(
    r'D:/Tania/UB/Semester 5/PENGPOL/Project Akhir/Final Project/dataset.xlsx')
# MENGAMBIL KOLOM KOMENTAR DARI INPUT DOCUMENT
inputKomentar = inputDocument['Comment']
inputHasilAkhir = inputDocument['Result']

listKomentarPositif = []
listKomentarNegatif = []

for indexKomentar in range(len(inputDocument)):
    if inputHasilAkhir[indexKomentar] == 1:
        listKomentarPositif.append(inputKomentar[indexKomentar])
    else:
        listKomentarNegatif.append(inputKomentar[indexKomentar])

print('1. Multinomial')
print('2. Gaussian')
metode = input('Masukan nomor metode :')

listAkurasi = []
kFold = 10
batasBawah = 0
batasAtas = 50

output_excel = {}
indexOutput = 1
# Proses k-fold
for fold in range(kFold):
    print('Fold ke-'+str(fold+1))
    listTesting = []
    listTraining = []
    myConProb = {}
    termsMain = []
    for indexKomentar in range(len(listKomentarPositif)):
        if indexKomentar >= batasBawah and indexKomentar < batasAtas:
            listTesting.append(listKomentarPositif[indexKomentar])
            listTesting.append(listKomentarNegatif[indexKomentar])
        else:
            listTraining.append(listKomentarPositif[indexKomentar])
            listTraining.append(listKomentarNegatif[indexKomentar])
    batasAtas += 50
    batasBawah += 50

    if metode == '1':
        multinomial(listTraining, listTesting)
    else:
        returnvalue = gaussian(listTraining,listTesting)
        hasilakurasi = returnvalue[0]
        result = returnvalue[1]
        listAkurasi.append(hasilakurasi)
        for i in range (len(result)):
            output_excel[indexOutput]=result[i]
            indexOutput+=1

with open('hasil_excel.csv', 'w') as output:
    writer = csv.writer(output)
    for key, value in output_excel.items():
        writer.writerow([key, value[0], value[1], value[2]])
    
print(str(listAkurasi))

average = 0
for hasilBenar in listAkurasi:
    average += hasilBenar
print('Akurasi akhir : ' + str(average/kFold))
