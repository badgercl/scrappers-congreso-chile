
import requests
from bs4 import BeautifulSoup
import json
import pprint

url = 'https://www.bcn.cl/siit/divisionelectoral/index.htm'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

rows = soup.find_all('tbody')[1].find_all('tr')

region = ""
circunscripcion = ""
distrito = ""
comuna = ""

regiones = {}
comunas = {}
for row in rows:
	tds = row.find_all('td')

	if len(tds) == 4:
		region = tds[0].text.strip()
		circunscripcion = tds[1].text.split()[0].replace('ª','')
		distrito = tds[2].text.split()[1]
		comuna = tds[3].a.text.replace('*', '').strip()

		regiones[region] = { 
			circunscripcion:  { distrito: [comuna] } 
		}
	elif len(tds) == 2:
		distrito = tds[0].text.split()[1]
		comuna = tds[1].a.text.replace('*', '').strip()
		regiones[region][circunscripcion][distrito] = [comuna]
	else:
		comuna = tds[0].a.text.replace('*', '').strip()
		regiones[region][circunscripcion][distrito].append(comuna)

	comunas[comuna] = {
		'circunscripcion': circunscripcion,
		'distrito': distrito,
		'region': region
	}



pp = pprint.PrettyPrinter(indent=4)
pp.pprint(comunas)