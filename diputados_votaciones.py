
import requests
from bs4 import BeautifulSoup
import json
import re
import pprint

def get_name_and_id(diputado):
	res = []
	nombre = diputado.text.strip()
	link = diputado.attrs['href']
	dip_id = p.match(link).group(1)

	return {
		'dip_id': dip_id,
		'nombre': nombre 
	}

url = "https://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=31786"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
p = re.compile('^../camara/diputado\_detalle\.aspx\?prmID=(\d+)$')


n_boletin = soup.find_all('h2')[3].text.strip().replace('Boletín N° ','')
dia = soup.find_all('div','stress')[0].find_all('p')[0].text.split()[1]
mes = soup.find_all('div','stress')[0].find_all('p')[0].text.split()[3]
anno = soup.find_all('div','stress')[0].find_all('p')[0].text.split()[5]
hora = soup.find_all('div','stress')[0].find_all('p')[0].text.split()[6]
materia = " ".join(soup.find_all('div','stress')[0].find_all('p')[1].text.split()[1:])
tramite = " ".join(soup.find_all('div','stress')[0].find_all('p')[4].text.split())
tipo = " ".join(soup.find_all('div','stress')[0].find_all('p')[5].text.split()).replace('Tipo de votación: ','')
quorum = " ".join(soup.find_all('div','stress')[0].find_all('p')[6].text.split()).replace('Quorum: ','')
resultado = " ".join(soup.find_all('div','stress')[0].find_all('p')[7].text.split()).replace('Resultado: ','')

lista_aprobados = soup.find_all('table')[1].find_all('a')
lista_en_contra = soup.find_all('table')[2].find_all('a')
lista_abstencion = soup.find_all('table')[3].find_all('a')
aprobados = []
en_contra = []
abstencion = []

for diputado in lista_aprobados:
	aprobados.append(get_name_and_id(diputado))

for diputado in lista_en_contra:
	en_contra.append(get_name_and_id(diputado))

for diputado in lista_abstencion:
	abstencion.append(get_name_and_id(diputado))

output = {
	'numero_boletin': n_boletin,
	'fecha': '{}-{}-{}'.format(anno, mes, dia),
	'materia': materia,
	'tramite': tramite,
	'tipo': tipo,
	'quorum': quorum,
	'resultado': resultado,
	'a_favor': aprobados,
	'en_contra': en_contra,
	'abstenciones': abstencion
}


with open('output/diputados_votaciones.json', 'w') as json_file:
    json.dump(output, json_file)