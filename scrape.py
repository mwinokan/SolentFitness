#!/usr/bin/env python3

offline = False

active_gw = 1

lookup = {
	1: {
		"name": "UTS Week 1 (Responses)",
		"datacol": "What was your total time?",
		"datatype": "time",
		"datalabel": "Time",
		"reversed": False,
		"namefix": {
			0: 'Manch',
			1: 'James Cushen'
		},
		"complete": {
			3: False,
			7: False,
		}
	}
}

import mout
import mcol

import json

from web import html_page

def get_sheet_records(name,gw):

	import gspread
	import pandas as pd
	from oauth2client.service_account import ServiceAccountCredentials

	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json',scope)
	client = gspread.authorize(creds)

	name = lookup[gw]['name']
	datacol = lookup[gw]['datacol']

	sheet = client.open(name)

	sheet_instance = sheet.get_worksheet(0)
	records_data = sheet_instance.get_all_records(expected_headers=None)
	records_df = pd.DataFrame.from_dict(records_data)

	print(records_df.columns)

	note = records_df.columns[-1]

	entries = []
	# for i,(name,data) in enumerate(zip(records_df['Name'],records_df[datacol])):

	for i,row in records_df.iterrows():

		name = row['Name']
		data = row[datacol]

		if "namefix" in lookup[gw]:
			if i in lookup[gw]["namefix"]:
				name = lookup[gw]["namefix"][i]

		complete = True
		if i in lookup[gw]['complete']:
			complete = lookup[gw]['complete'][i]

		# if row[note]:
		# 	print(name,row[note])

		entries.append(dict(name=name,data=data,index=i,note=row[note],complete=complete))

	mout.out(f'Writing {mcol.file}week{gw}.json{mcol.clear}...')
	json.dump(entries, open(f'week{gw}.json','wt'))

	return entries

def result_table(gw,data):

	html_buffer = ''

	html_buffer += '<table class="w3-table-all">\n'
	
	# header
	html_buffer += '<tr>\n'

	html_buffer += '<th>\n'
	html_buffer += 'Rank\n'
	html_buffer += '</th>\n'

	html_buffer += '<th>\n'
	html_buffer += 'Name\n'
	html_buffer += '</th>\n'

	html_buffer += '<th>\n'
	html_buffer += f'{lookup[gw]["datalabel"]}\n'
	html_buffer += '</th>\n'

	html_buffer += '<th>\n'
	html_buffer += 'Note\n'
	html_buffer += '</th>\n'

	html_buffer += '</tr>\n'

	# complete
	completed = [d for d in data if d['complete']]
	for i,d in enumerate(sorted(completed,key=lambda x: x['data'],reverse=lookup[gw]['reversed'])):

		html_buffer += '<tr>\n'

		html_buffer += '<td>\n'
		html_buffer += f'{i+1}\n'
		html_buffer += '</td>\n'

		html_buffer += '<td>\n'
		html_buffer += f"{d['name']}\n"
		html_buffer += '</td>\n'

		html_buffer += '<td>\n'
		html_buffer += f"{d['data']}\n"
		html_buffer += '</td>\n'

		html_buffer += '<td>\n'
		html_buffer += f"{d['note']}\n"
		html_buffer += '</td>\n'

		html_buffer += '</tr>\n'

	# partial
	partial = [d for d in data if not d['complete']]
	for j,d in enumerate(sorted(partial,key=lambda x: x['data'],reverse=lookup[gw]['reversed'])):

		html_buffer += '<tr>\n'

		html_buffer += '<td>\n'
		html_buffer += f'{i+1+j+1}\n'
		html_buffer += '</td>\n'

		html_buffer += '<td>\n'
		html_buffer += f"{d['name']}\n"
		html_buffer += '</td>\n'

		html_buffer += '<td>\n'
		html_buffer += f"{d['data']}\n"
		html_buffer += '</td>\n'

		html_buffer += '<td>\n'
		html_buffer += f"{d['note']}\n"
		html_buffer += '</td>\n'

		html_buffer += '</tr>\n'

	html_buffer += '</table>\n'

	return html_buffer

def push_changes():

	import os
	os.system("git add *py")
	os.system("git add *html")
	os.system("git commit -m 'auto-push'")
	os.system("git push")

def main():

	html_buffer = ''
	
	html_buffer += f'<h1 class="w3-center">Fitness Challenge Results</h1>\n'

	for gw in range(active_gw,0,-1):

		mout.headerOut(f'Gameweek {gw}')
		html_buffer += f'<h2>Week {gw}</h2>\n'

		# get the data
		if not offline and gw == active_gw:
			data = get_sheet_records(lookup[gw]['name'],gw)
		else:
			mout.out(f'Reading {mcol.file}week{gw}.json{mcol.clear}...')
			data = json.load(open(f'week{gw}.json','rt'))

		for d in sorted(data,key=lambda x: x['data'],reverse=lookup[gw]['reversed']):
			print(d['name'],d['data'],d['index'],d['note'])

		html_buffer += result_table(gw, data)

	html_page('Solent Fitness','index.html', html_buffer, active_gw)

	push_changes()

if __name__ == '__main__':
	main()
