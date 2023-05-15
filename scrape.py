#!/usr/bin/env python3

import mout
import mcol

import gspread
import pandas as pd

import json

from oauth2client.service_account import ServiceAccountCredentials

recalculate = False

if recalculate:

	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json',scope)
	client = gspread.authorize(creds)

	sheet = client.open("UTS Week 1 (Responses)")

	sheet_instance = sheet.get_worksheet(0)
	records_data = sheet_instance.get_all_records(expected_headers=None)
	records_df = pd.DataFrame.from_dict(records_data)

	entries = []
	for i,(name,time) in enumerate(zip(records_df['Name'],records_df['What was your total time?'])):
		if i == 0: name = 'Manch'
		elif i == 1: name = 'James Cushen'
		entries.append(dict(name=name,time=time))

	json.dump(entries, open('week1.json','wt'))
	
else:

	entries = json.load(open('week1.json','rt'))

for d in sorted(entries,key=lambda x: x['time'],reverse=False):

	print(d['name'],d['time'])

