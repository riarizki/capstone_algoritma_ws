from flask import Flask, render_template 
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import dateparser

app = Flask(__name__)

def scrap(url):
    #This is function for scrapping
    url_get = requests.get(url)
    soup = BeautifulSoup(url_get.content,"html.parser")
    
    #Find the key to get the information
    table = soup.find('table', attrs={'class':'table'})
    tr = table.find_all('tr')

    temp = [] #initiating a tuple

    for i in range(1, len(tr)):
        row = table.find_all('tr')[i]
        #use the key to take information here
        #name_of_object = row.find_all(...)[0].text
        #get periode
        Tanggal = row.find_all('td')[0].text
        Tanggal = Tanggal.strip() #remove excess whitespace
        Tanggal = Tanggal.replace(u'\xa0', u' ')
    
        #get Kurs_jual (ASK)
        Kurs_jual = row.find_all('td')[1].text
        Kurs_jual = Kurs_jual.strip() #for removing the excess whitespace
    
        #get Kurs_beli (BID)
        Kurs_beli = row.find_all('td')[2].text
        Kurs_beli = Kurs_beli.strip() #for removing the excess whitespace
    
        temp.append((Tanggal,Kurs_jual,Kurs_beli)) #append the needed information
    
    temp = temp[::-1]  #remove the header
    
    kurs = pd.DataFrame(temp, columns = ('Tanggal','Kurs_jual','Kurs_beli')) #creating the dataframe
    
    #data wranggling - try to change the data type to right data type
    
    kurs['Kurs_jual'] = kurs['Kurs_jual'].str.replace("," , ".",regex = True)
    kurs['Kurs_beli'] = kurs['Kurs_beli'].str.replace("," , ".",regex = True)
    
    kurs['Tanggal'] = kurs['Tanggal'].apply(lambda x: dateparser.parse(x))
    
    kurs[['Kurs_jual', 'Kurs_beli']] = kurs[['Kurs_jual', 'Kurs_beli']].astype('float64')
    
    kurs['periode'] = kurs['Tanggal'].dt.to_period('M')
    
    kurs = kurs.groupby('periode').mean().round(2)
                           
    #end of data wranggling

    return kurs

@app.route("/")
def index():
    kurs = scrap('https://monexnews.com/kurs-valuta-asing.htm?kurs=JPY&searchdatefrom=01-01-2019&searchdateto=31-12-2019') #insert url here

    #This part for rendering matplotlib
    fig = plt.figure(figsize=(5,2),dpi=300)
    kurs.plot()
    
    #Do not change this part
    plt.savefig('plot1',bbox_inches="tight") 
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]
    #This part for rendering matplotlib

    #this is for rendering the table
    kurs = kurs.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])

    return render_template("index.html", table=kurs, result=result)


if __name__ == "__main__": 
    app.run()
