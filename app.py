from flask import Flask, render_template 
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

def scrap(url):
    #This is fuction for scrapping
    url_get = requests.get('https://monexnews.com/kurs-valuta-asing.htm?kurs=JPY&searchdatefrom=01-01-2019&searchdateto=31-12-2019')
    soup = BeautifulSoup(url_get.content,"html.parser")
    
    # for tidyness purpose
    soup = BeautifulSoup(url_get.content,"html.parser")
    print(type(soup))
    
    #Find the key to get the information
    table = soup.find('table', attrs={'class':'table'})
    print(table.prettify()[1:500])
    tr = table.find_all('tr')
    tr[:] 

    temp = [] #initiating a tuple

    for i in range(1, len(tr)):
        row = table.find_all('tr')[i]
        #use the key to take information here
        #name_of_object = row.find_all(...)[0].text

        #get periode
        tanggal = row.find_all('td')[0].text
        tanggal = tanggal.replace(u'\xa0', u' ')
    
        #get ASK
        kurs_jual = row.find_all('td')[1].text
        kurs_jual = kurs_jual.strip() 
    
        #get BID
        kurs_beli = row.find_all('td')[2].text
        kurs_beli = kurs_beli.strip() 
    
        temp.append((tanggal,kurs_jual,kurs_beli)) #append the needed information
    
temp = temp[::-1] #remove the header
    kurs = pd.DataFrame(temp, columns = ('tanggal','kurs_jual', 'kurs_beli')) #creating the dataframe
    #data wranggling -  try to change the data type to right data type

import dateparser

    # convert period to standard format in phyton
    kurs['tanggal']=kurs['tanggal'].apply(lambda x: dateparser.parse(x))
    kurs = kurs.set_index("tanggal")

    # to change coma into dot to make floating data
    kurs['kurs_jual'] = kurs['kurs_jual'].str.replace("," , ".",regex = True)
    kurs['kurs_beli'] = kurs['kurs_beli'].str.replace("," , ".",regex = True)

    # change data type 
    kurs['kurs_jual'] = kurs['kurs_jual'].astype('float64')
    kurs['kurs_beli'] = kurs['kurs_beli'].astype('float64')


   #end of data wranggling

   return kurs

@app.route("/")
def index():
    kurs = scrap('https://monexnews.com/kurs-valuta-asing.htm?kurs=JPY&searchdatefrom=01-01-2019&searchdateto=31-12-2019') # insert url here

    #This part for rendering matplotlib
    fig = plt.figure(figsize=(5,2),dpi=300)
    df.plot()
    
    #Do not change this part
    plt.savefig('plot1',bbox_inches="tight") 
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]
    #This part for rendering matplotlib

    #this is for rendering the table
    df = df.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])

    return render_template("index.html", table=df, result=result)


if __name__ == "__main__": 
    app.run()
