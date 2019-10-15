#http://vcs.api.datainterfaces.org/vcs.json?min_date=2016-06&max_date=2017-06

import json
import csv
import pandas as pd

from bs4 import BeautifulSoup
import requests


start_date = "2016-07"
end_date = "2017-06"

def job(infr, tipoinfr):
	print(infr, tipoinfr)
	with open('location_metadata.csv') as loc_file:
		csv_file = csv.reader(loc_file, delimiter=",")
		lines = list(csv_file)
		to_writes = []
		to_writes.append(['loc_id', 'full_address', 'lat', 'lng', tipoinfr])

		page_link = 'http://vcs.api.datainterfaces.org/vcs.json?infr_list=' + infr + '&min_date=' + start_date + '&max_date=' + end_date
		page_response = requests.get(page_link, timeout=5)
		try:
			data = page_response.json()
		except ValueError:
			print('EMPTY')
		if data:
			for res in data['loc_id']:
				index = int(res) + 1
				to_writes.append([lines[index][0], data['loc_id'][res]])

def job2(infr):
	print('Analizzo infrazione numero ',infr)
	with open('output_file.csv') as loc_file:
		csv_file = csv.reader(loc_file, delimiter=",")
		lines = list(csv_file)

		to_writes = []
		for line in lines:
			to_writes.append(line)

		page_link = 'http://vcs.api.datainterfaces.org/vcs.json?infr_list=' + infr + '&min_date=' + start_date + '&max_date=' + end_date
		page_response = requests.get(page_link, timeout=5)
		try:
			data = page_response.json()
		except ValueError:
			print('EMPTY')
		if data:
			for res in data['loc_id']:
				for write in to_writes:
					if write[0] == res:
						index = int(infr) + 4
						write[index] = data['loc_id'][res]

	with open('output_file.csv', 'w') as csvout:
		writefile = csv.writer(csvout, delimiter=',', lineterminator='\n')
		for write in to_writes:
			writefile.writerow(write)

def create_file():
	with open("location_infr.csv") as csvin:
		readfile = csv.reader(csvin, delimiter=',')
		lines = list(readfile)
		with open('output_file.csv', 'w') as csvout:
			writefile = csv.writer(csvout, delimiter=',', lineterminator='\n')
			index = 0
			for row in lines:
				if index > 0:
					# row.extend(["0" + ' ' + "0"])
					new = []
					for r in row:
						if not r:
							new.append(0)
						else:
							new.append(r)
					writefile.writerow(new)
				else:
					writefile.writerow(row)
				index+=1
	print("-----		LOCATION CREATED		-----")

	with open('infr_metadata.csv') as loc_file:
		csv_file = csv.reader(loc_file, delimiter=",")
		lines = list(csv_file)
		lines.pop(0)
		for line in lines:
			job2(line[0])

create_file()