# Web-Scrapping JPY to IDR Kurs

## Description

![](plot1.PNG)


Webapp ini merupakan hasil dari web scrapping data kurs Japan Yen (JPY) terhadap Indonesia Rupiah (IDR) tahun 2019 dari `monexnews.com/kurs-valuta-asing.htm?kurs=JPY`.

Webapp ini menampilkan interactive visualization dari plot pergerakan kurs (Kurs Jual dan Kurs Beli) pada tahun 2019.


## Dependencies

- beautifulSoup4
- pandas
- flask
- matplotlib


## Conclusion

- Setelah melakukan data scrapping dan data wrangling dari `monexnews.com/kurs-valuta-asing.htm?kurs=JPY` dengan mencari data kurs jual dan kurs beli JPY to IDR pada tahun 2019, maka didapatkan 246 data berdasarkan hari kerja yang ada di tahun 2019.
- Dari hasil scrapping data Kurs Yen to IDR Tahun 2019 diketahui bahwa Kurs menempati posisi terendah pada Tanggal 18 April 2019 dengan perolehan nilai yaitu:
1. Kurs Jual sebesar 125,84
2. Kurs Beli 124,55 
dan menempati posisi tertinggi pada Tanggal 26 Agustus 2019 dengan perolehan nilai, yaitu:
1. Kurs Jual sebesar 136,20 
2. Kurs Beli 134,81 
