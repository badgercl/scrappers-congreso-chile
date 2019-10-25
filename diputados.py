
import requests
from bs4 import BeautifulSoup
import json
import re

url = 'https://www.camara.cl/camara/diputados.aspx'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
p = re.compile('^diputado_detalle\.aspx\?prmid=(\d+)$')

regiones = {'RM': 'Región Metropolitana', 
'I': 'Tarapacá', 
'II': 'Antofagasta', 
'III': 'Atacama', 
'IV': 'Coquimbo',
'V': 'Valparaíso',
'VI': 'Libertador General Bernardo O\'Higgins', 
'VII': 'Maule',
'VIII': 'Biobío',
'IX': 'La Araucanía',
'X': 'Los Lagos',
'XI': 'Aysén del General Carlos Ibáñez del Campo',
'XII': 'Magallanes y de la Antártica Chilena',
'XIV': 'Los Ríos',
'XV': 'Arica y Parinacota   ' 
}

partidos = {
'PH': 'Partido Humanista', 
'PS': 'Partido Socialista', 
'EVOP': 'Evopoli', 
'PC': 'Partido Comunista', 
'IND': 'Independiente', 
'PR': 'Partido Radical', 
'FRVS': 'Federación Regionalista Verde Social', 
'UDI': 'Unión Demócrata Independiente', 
'RN': 'Renovación Nacional', 
'LIBERAL': 'Partido Liberal', 
'PPD': 'Partido por la Democracia', 
'DC': 'Democracia Cristiana', 
'RD': 'Revolución Democratica', 
'PEV': 'Partido Ecologista Verde', 
'PODER': 'Partido Poder Ciudadano'
}

diputados = soup.find_all('li', 'alturaDiputado')

output = []
indice = {}
for diputado in diputados:

    dip_id = int(p.match(diputado.find_all('a')[1].attrs['href']).group(1))
    nombre = diputado.find('img').attrs['alt']
    mail = diputado.find('a').find('img').attrs['alt']
    region = diputado.find('ul','links').find_all('li')[0].text.split()[1]
    distrito = diputado.find('ul','links').find_all('li')[1].text.split()[1].replace('N°','')
    partido = diputado.find('ul','links').find_all('li')[2].text.split()[1]
    output.append({
        'dip_id': dip_id,
        'nombre': nombre,
        'mail': mail,
        'region': regiones[region],
        'distrito': distrito,
        'partido': partidos[partido]
        })
    if distrito not in indice:
        indice[distrito] = []
    indice[distrito].append({
        'dip_id': dip_id,
        'nombre': nombre,
        'mail': mail,
        'region': regiones[region],
        'partido': partidos[partido]
        })

with open('output/diputados.json', 'w') as json_file:
    json.dump(output, json_file)

with open('output/diputados_index.json', 'w') as json_file:
    json.dump(indice, json_file)

