
import requests
from bs4 import BeautifulSoup
import json

url = 'https://senado.cl/wspublico/senadores_vigentes.php'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

senadores = soup.find_all('senador')
partidos = {
'P.S.':'Partido Socialista', 
'Independiente': 'Independiente', 
'P.D.C.': 'Partido Demócrata Cristiano', 
'U.D.I.': 'Unión Demócrata Independiente', 
'Revolución Democrática': 'Revolución Democrática', 
'Pais Progresista': 'Pais Progresista', 
'R.N.': 'Renovación Nacional', 
'P.P.D.': 'Partido Por la Democracia', 
'Evopoli': 'Evopoli'
}

output = []
for senador in senadores:
	nombre = senador.find('parlnombre').text
	apellido = senador.find('parlapellidopaterno').text
	region = senador.find('region').text.replace('&apos','\'')
	circunscripcion = senador.find('circunscripcion').text
	partido = partidos[senador.find('partido').text]
	mail = senador.find('email').text
	output.append({
		'nombre': "{} {}".format(apellido, apellido),
		'region': region,
		'circunscripcion': circunscripcion,
		'partido': partido,
		'mail': mail
		})

with open('output/senadores.json', 'w') as json_file:
    json.dump(output, json_file)