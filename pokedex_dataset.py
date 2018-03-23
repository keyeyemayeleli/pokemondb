import requests
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup
import re
import json

r = requests.get('https://pokemondb.net/pokedex/national')
soup = BeautifulSoup(r.text,'lxml')
links = []
dex = []

links = [ 'https://pokemondb.net' + a['href'] for a in soup.find_all('a', {'class' : 'ent-name'})]

	
def parseHtml(s):
		dexdata = s.find('h2', text='Pokédex data').findNext('table')
		poke_name = s.find('h1').text
		nat_id = dexdata.find('th', text='National №').findNext('td').text
		types = dexdata.find('th', text='Type').findNext('td').text.strip()
		species = dexdata.find('th', text='Species').findNext('td').text
		height = dexdata.find('th', text='Height').findNext('td').text
		weight = dexdata.find('th', text='Weight').findNext('td').text
		ability = dexdata.find('th', text='Abilities').findNext('a').text
		hability = dexdata.find('th', text='Abilities').findNext('a').findNext('a').text
		#japname = dexdata.find('th', text='Japanese').findNext('td').text 
		training = s.find('h2', text='Training').findNext('table')
		evyield = training.find('th', text='EV yield').findNext('td').text.strip()
		catchrate = training.find('th', text='Catch rate').findNext('td').text
		base_hap = training.find('th', text='Base Happiness').findNext('td').text.strip()
		base_exp = training.find('th', text='Base EXP').findNext('td').text
		growth_rate = training.find('th', text='Growth Rate').findNext('td').text
		breeding = s.find('h2', text='Breeding').findNext('table')
		egg_groups = breeding.find('th', text='Egg Groups').findNext('td').text.strip()
		male_ratio = breeding.find('span', {'class': 'gender-male'}).text
		female_ratio = breeding.find('span', {'class': 'gender-female'}).text
		egg_cycles = breeding.find('th', text='Egg cycles').findNext('td').text.strip()
		stats = s.find('h2', text='Base stats').findNext('table')
		hp = stats.find('th', text='HP')
		hp_base = hp.findNext('td', {'class':'num'}).text # 
		hp_min = hp.findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).text
		hp_max = hp.findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).text
		atk = stats.find('th', text='Attack')
		atk_base = atk.findNext('td', {'class':'num'}).text
		atk_min = atk.findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).text
		atk_max = atk.findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).text
		defense = stats.find('th', text='Defense')
		defense_base = defense.findNext('td', {'class':'num'}).text
		defense_min = defense.findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).text
		defense_max = defense.findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).text
		spdefense = stats.find('th', text='Sp. Def')
		spdefense_base = spdefense.findNext('td', {'class':'num'}).text
		spdefense_min = spdefense.findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).text
		spdefense_max = spdefense.findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).text
		speed = stats.find('th', text='Speed')
		speed_base = speed.findNext('td', {'class':'num'}).text
		speed_min = speed.findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).text
		speed_max = speed.findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).findNext('td', {'class':'num'}).text
		e = s.find('h2', text='Pokédex entries').findNext('table')
		entries = {i.text:i.findNext('td').text for i in e.find_all('span')}
		evo = s.find('div', class_='infocard-evo-list')
		a = []
		b = []
		evolutions = []
		for i in evo.find_all('a', class_='ent-name'):
		    a.append(i.text)
		    b.append(re.sub('[^0-9]','', i.findNext('span').text))
		for count, a in enumerate(a[1:]):
		    k = {}
		    k.update({'evolves_to':a, 'level':b[count]})
		    evolutions.append(k)
		m = s.find('h3', text='Moves learnt by level up').findNext('table')
		headers = [h.text for h in m.find_all('th')]
		moves_lvl = [{headers[c]:x.text for c, x in enumerate(r.find_all('td'))} for r in m.find_all('tr')[1:]]
		m = s.find('h3', text='Egg moves').findNext('table')
		headers = [h.text for h in m.find_all('th')]
		moves_egg = [{headers[c]:x.text for c, x in enumerate(r.find_all('td'))} for r in m.find_all('tr')[1:]]
		m = s.find('h3', text='Move Tutor moves').findNext('table')
		headers = [h.text for h in m.find_all('th')]
		moves_tutor = [{headers[c]:x.text for c, x in enumerate(r.find_all('td'))} for r in m.find_all('tr')[1:]]
		m = s.find('h3', text='Moves learnt by TM').findNext('table')
		headers = [h.text for h in m.find_all('th')]
		moves_tm = [{headers[c]:x.text for c, x in enumerate(r.find_all('td'))} for r in m.find_all('tr')[1:]]
		loc = s.find('h2', text=('Where to find ' + poke_name)).findNext('table')

		locations = {i.text:i.findNext('td').text for i in loc.find_all('span', class_='igame')}

		x = {'name': poke_name,
		 	 'nat_id':nat_id,
		     'types':types,
		     'species':species,
		     'height':height,
		     'weight':weight,
		     'ability':ability,
		     'hability':hability,
		     #'japname':japname,
		     'evyield':evyield,
		     'catchrate':catchrate,
		     'base_hap':base_hap,
		     'base_exp':base_exp,
		     'growth_rate':growth_rate,
		     'egg_groups':egg_groups,
		     'male_ratio':male_ratio,
		     'female_ratio':female_ratio,
		     'egg_cycles':egg_cycles,
		     'hp_base':hp_base,
		     'hp_min':hp_min,
		     'hp_max':hp_max,
		     'atk_base':atk_base,
		     'atk_min':atk_min,
		     'atk_max':atk_max,
		     'defense_base':defense_base,
		     'defense_min':defense_min,
		     'defense_max':defense_max,
		     'spdefense_base':spdefense_base,
		     'spdefense_min':spdefense_min,
		     'spdefense_max':spdefense_max,
		     'speed_base':speed_base,
		     'speed_min':speed_min,
		     'speed_max':speed_max,
		     'entries':entries, 
		     'evolutions': evolutions, 
		     'moves_lvl': moves_lvl, 
		     'moves_egg':moves_egg, 
		     'moves_tutor': moves_tutor, 
		     'locations':locations}
		dex.append(x)

for l in links:
	r = requests.get(l)
	soup = BeautifulSoup(r.text, 'lxml')
	parseHtml(soup)
	print(l)

with open('pokedex.json', 'w') as outfile:
    json.dump(dex, outfile)