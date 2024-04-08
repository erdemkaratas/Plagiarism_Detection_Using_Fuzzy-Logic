import os
from os import listdir
from os.path import isfile, join
from fuzzywuzzy import fuzz as fw_fuzz
from fuzzywuzzy import process as fw_process
import numpy as np
import skfuzzy as fuzz
from skfuzzy import interp_membership, trimf, centroid, trapmf
import matplotlib.pyplot as plt
import math as m
import skfuzzy.membership as mf

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def dosyaOku():
    chatgpt_dosyasi = open("./file/chatgpt.py", 'r')
    chatgpt_icerik = chatgpt_dosyasi.read()

    for diger_dosya in dosyaisimleri:
        if diger_dosya == "chatgpt.py":
            continue

        diger_dosya_yolu = "./file/" + diger_dosya
        dosya = open(diger_dosya_yolu, 'r')
        dosya_icerik = dosya.read()

        print("Islem Yapilan Dosya: chatgpt.py -- {}".format(diger_dosya))

        chatgpt_icerik = "".join(chatgpt_icerik.split())
        dosya_icerik = "".join(dosya_icerik.split())
        
        # CountVectorizer kullanarak belge vektörlerini oluştur
        vectorizer = CountVectorizer().fit_transform([chatgpt_icerik, dosya_icerik])

        # Cosine similarity hesapla
        cosine_sim = cosine_similarity(vectorizer)

        # İki döküman arasındaki cosine similarity değeri
        icerikbenzerlik = cosine_sim[0, 1]*99
        
        dilbenzerlikoran = dilBenzerlikOranıBul("chatgpt.py", diger_dosya)
        kontrollistesi.append(("chatgpt.py", diger_dosya, icerikbenzerlik, dilbenzerlikoran))

        dosya.close() 

    chatgpt_dosyasi.close()

kontrollistesi = []

progDilBenzerlikMatrisi = [[100, 25, 30, 35, 10], [25, 100, 30, 20, 5], [30, 30, 100, 25, 5], [35, 20, 25, 100, 10], [10, 5, 5, 10, 100]]
sozluk = {"java": 0, "c": 1, "cpp": 2, "cs": 3, "py": 4}
yol = "./file"
dosyaisimleri = [f for f in listdir(yol) if isfile(join(yol, f))]

benzerlik_degiskeni = np.arange(0, 101, 1)
dil_benzerlik_degiskeni = np.arange(0, 101, 1)
kopya_degiskeni = np.arange(0, 101, 1)

benzerlik_az = mf.trimf(benzerlik_degiskeni, [0, 0, 50])
benzerlik_orta = mf.trimf(benzerlik_degiskeni, [30, 50, 70])
benzerlik_cok = mf.trimf(benzerlik_degiskeni, [50, 100, 100])

dil_benzerlik_dusuk = mf.trimf(dil_benzerlik_degiskeni, [0, 0, 100])
dil_benzerlik_yuksek = mf.trimf(dil_benzerlik_degiskeni, [0, 100, 100])

kopya_yok = mf.trapmf(kopya_degiskeni, [0, 0, 30, 50])
kopya_ihtimali = mf.trapmf(kopya_degiskeni, [30, 55, 55, 70])
kopya_var = mf.trapmf(kopya_degiskeni, [60, 80, 100, 100])

def bulanikMantik(input_benzerlik, input_dil_benzerlik):
    benzerlik_az_uyelik = interp_membership(benzerlik_degiskeni, benzerlik_az, input_benzerlik)
    benzerlik_orta_uyelik = interp_membership(benzerlik_degiskeni, benzerlik_orta, input_benzerlik)
    benzerlik_cok_uyelik = interp_membership(benzerlik_degiskeni, benzerlik_cok, input_benzerlik)

    dil_benzerlik_dusuk_uyelik = interp_membership(dil_benzerlik_degiskeni, dil_benzerlik_dusuk, input_dil_benzerlik)
    dil_benzerlik_yuksek_uyelik = interp_membership(dil_benzerlik_degiskeni, dil_benzerlik_yuksek, input_dil_benzerlik)

    kural1 = np.fmin(np.fmin(benzerlik_az_uyelik, dil_benzerlik_yuksek_uyelik), kopya_yok)
    kural2 = np.fmin(np.fmin(benzerlik_az_uyelik, dil_benzerlik_dusuk_uyelik), kopya_yok)
    kural3 = np.fmin(np.fmin(benzerlik_orta_uyelik, dil_benzerlik_yuksek_uyelik), kopya_var)
    kural4 = np.fmin(np.fmin(benzerlik_orta_uyelik, dil_benzerlik_dusuk_uyelik), kopya_ihtimali)
    kural5 = np.fmin(np.fmin(benzerlik_cok_uyelik, dil_benzerlik_yuksek_uyelik), kopya_var)
    out_var = np.fmax.reduce([kural1, kural2, kural3, kural4,kural5])
    defuzzified = fuzz.defuzz(kopya_degiskeni, out_var, 'centroid')

    return defuzzified

def grafik():
    fig, (ax0, ax1, ax2) = plt.subplots(nrows = 3, figsize =(6, 10))

    ax0.plot(benzerlik_degiskeni, benzerlik_az, 'r', linewidth = 2, label = 'Düşük')
    ax0.plot(benzerlik_degiskeni, benzerlik_orta, 'g', linewidth = 2, label = 'Orta')
    ax0.plot(benzerlik_degiskeni, benzerlik_cok, 'b', linewidth = 2, label = 'Yüksek')
    ax0.set_title('Kod Benzerlik')
    ax0.legend()

    ax1.plot(dil_benzerlik_degiskeni,dil_benzerlik_dusuk, 'r', linewidth = 2, label = 'Düşük')
    ax1.plot(dil_benzerlik_degiskeni, dil_benzerlik_yuksek, 'b', linewidth = 2, label = 'Yüksek')
    ax1.set_title('Programlama Dil Benzerliği')
    ax1.legend()

    ax2.plot(kopya_degiskeni, kopya_yok, 'r', linewidth = 2, label = 'Zayıf')
    ax2.plot(kopya_degiskeni, kopya_ihtimali, 'g', linewidth = 2, label = 'Orta')
    ax2.plot(kopya_degiskeni, kopya_var, 'b', linewidth = 2, label = 'Güçlü')
    ax2.set_title('Kopya İhtimali')
    ax2.legend()

    plt.tight_layout()
    plt.show()

def kopyaBul():
    with open('Karsilastirma Sonuclari.txt', 'w') as dosya:
        dosya.write("{:<30} {:<30} {:<25} {:<25} {:<25}\n".format("Dosya 1", "Dosya 2", "Kod Benzerlik (%)", "Dil Benzerlik (%)", "Benzerlik Sonuc (%)"))
        for i in range(len(kontrollistesi)):
            kopyaOrani = m.ceil(bulanikMantik(kontrollistesi[i][2], kontrollistesi[i][3]))
            dosya.write("{:<30} {:<30} {:<25} {:<25} {:<25}\n".format(kontrollistesi[i][0], kontrollistesi[i][1], kontrollistesi[i][2], kontrollistesi[i][3], kopyaOrani))
            dosya.write("--------------------------------------------------------------------------\n")

# Geri kalan kodu buraya ekleyin
    
    dosya.close()

def dilBenzerlikOranıBul(dosyaAdi1, dosyaAdi2):
    liste1 = dosyaAdi1.split(".")
    uzanti1 = liste1[1]
    liste2 = dosyaAdi2.split(".")
    uzanti2 = liste2[1]
   
    struzanti1 = sozluk[str(uzanti1)]
    struzanti2 = sozluk[str(uzanti2)]
    return progDilBenzerlikMatrisi[struzanti1][struzanti2]

dosyaOku()
kopyaBul()
grafik()
kopyaOrani = m.ceil(bulanikMantik(55, 100))
print(kopyaOrani)