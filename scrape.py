from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

df = pd.DataFrame(columns=["Title", "Price","Locali","Superficie","Bagni","Grantito","Description"])
address =  "https://www.immobiliare.it/vendita-case/roma/?criterio=rilevanza&pag="
row=0
for i in range(1,500):
	address = "https://www.immobiliare.it/vendita-case/roma/?criterio=rilevanza&pag="+str(i)
	url = requests.get(address)
	page =BeautifulSoup(url.text, 'lxml') 


	for x in page.find_all('ul',{'class','annunci-list'}):
		for y in x.find_all('li', {'class', 'listing-item vetrina js-row-detail'}):
			try:
				content = y.find('div',class_='listing-item_body--content')
				title = content.p.text
				price = content.find('li', class_='lif__item lif__pricing').text
				locali_superficie = content.find_all(class_= 'text-bold')
				locali = locali_superficie[0].text
				superficie = locali_superficie[1].text
				bagni = locali_superficie[2].text
				grantito = content.find('li',class_='lif__item lif__guaranteed').text
				description = content.find('div',class_="descrizione").text
				#print(title.strip())

				df.loc[row] = [title.strip(),price.strip(),locali,superficie,bagni,grantito[:8],description]
				row+=1
			except:
				print("Not considering a column")



	print("Page Number:"+str(i))

df.to_csv("scrape.csv")
