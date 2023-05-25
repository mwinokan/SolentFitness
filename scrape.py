#!/usr/bin/env python3

offline = False
run_push_changes = True
force_pull = False

active_gw = 3

lookup = {
	1: {
		"name": "UTS Week 1 (Responses)",
		"label": "10x (10x press-ups, 10x squats, 10x lunges, 10x sit ups, 10x burpees)",
		"datacol": "What was your total time?",
		"datatype": "time",
		"datalabel": "Time",
		"reversed": False,
		"namefix": {
			0: 'Manch',
			1: 'James Cushen',
			3: 'Tom Allan',
		},
		"complete": {
			3: False,
			7: False,
		}
	},
	2: {
		"name": "UTS Week 2 (Responses)",
		"label": "5km run",
		"datacol": "What was your total time?",
		"datatype": "time",
		"datalabel": "Time",
		"reversed": False,
		"complete": {},
		"skip": [2]
	},
	3: {
		"name": "UTS Week 3 (Responses)",
		"label": "1 mile run, 50/50/50 squats/press-ups/sit-ups, 1 mile run",
		"datacol": "What was your total time?",
		"datatype": "time",
		"datalabel": "Time",
		"reversed": False,
		"complete": {},
		# "skip": [2]
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

	if not len(records_df):
		mout.error("empty dataframe")

	print(records_df.columns)

	note = records_df.columns[-1]

	entries = []
	# for i,(name,data) in enumerate(zip(records_df['Name'],records_df[datacol])):

	for i,row in records_df.iterrows():

		name = row['Name'].strip()
		data = row[datacol]

		if "namefix" in lookup[gw]:
			if i in lookup[gw]["namefix"]:
				name = lookup[gw]["namefix"][i]

		if "skip" in lookup[gw]:
			if i in lookup[gw]["skip"]:
				continue

		complete = True
		if i in lookup[gw]['complete']:
			complete = lookup[gw]['complete'][i]

		entries.append(dict(name=name,data=data,index=i,note=row[note],complete=complete))

	mout.out(f'Writing {mcol.file}week{gw}.json{mcol.clear}...')
	json.dump(entries, open(f'week{gw}.json','wt'))

	return entries

def calculate_gw_points(position,complete):

	points = 1

	if complete:
		points += 1

	if position < 11:
		points += 11 - position

	return points

def result_table(gw,data):

	html_buffer = f'<p><b>{lookup[gw]["label"]}</b></p>'

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
	html_buffer += 'Pts\n'
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

		if i == 0:
			html_buffer += '🏆\n'
		else:
			html_buffer += f'{i+1}\n'

		html_buffer += '</td>\n'

		html_buffer += '<td>\n'
		html_buffer += f"{d['name']}\n"
		html_buffer += '</td>\n'

		html_buffer += '<td>\n'
		html_buffer += f"{d['data']}\n"
		html_buffer += '</td>\n'

		d['points'] = calculate_gw_points(i+1, True)
		d['position'] = i+1

		html_buffer += '<td>\n'
		html_buffer += f"{d['points']}\n"
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

		d['points'] = calculate_gw_points(i+j+1+1, False)
		d['position'] = i+j+1

		html_buffer += '<td>\n'
		html_buffer += f"{d['points']}\n"
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

	import os

	# launchd_plist()
	# exit()

	try:

		result_buffer = ''
		

		all_data = {}

		for gw in range(active_gw,0,-1):

			mout.headerOut(f'Gameweek {gw}')
			result_buffer += f'<h3>Week {gw}</h2>\n'

			# get the data
			if force_pull or not offline and gw == active_gw:
				data = get_sheet_records(lookup[gw]['name'],gw)
			else:
				mout.out(f'Reading {mcol.file}week{gw}.json{mcol.clear}...')
				data = json.load(open(f'week{gw}.json','rt'))

			for d in sorted(data,key=lambda x: x['data'],reverse=lookup[gw]['reversed']):
				print(d['name'],d['data'],d['index'],d['note'])

			all_data[gw] = data

			result_buffer += result_table(gw, data)

		html_buffer = f'<h1 class="w3-center">Fitness Challenge</h1>\n'

		html_buffer += '<p>Points are awarded per week for:</p>\n'
		html_buffer += '<ul>\n'
		html_buffer += '<li><b>1 point</b> for participation</li>\n'
		html_buffer += '<li><b>1 point</b> for a completed challenge</li>\n'
		html_buffer += '<li><b>1-10 points</b> for the top 10 best entries</li>\n'
		html_buffer += '</ul>\n'
		
		html_buffer += f'<h2>Leaderboard</h2>\n'
		html_buffer += leaderboard(all_data)

		html_buffer += f'<h2>Weekly Entries</h2>\n'
		html_buffer += result_buffer

		html_page('Solent Fitness','index.html', html_buffer, active_gw)

		if run_push_changes:
			push_changes()
		
		os.system("terminal-notifier -title 'UTS' -message 'Completed page update'")

	except Exception as e:

		mout.error(e)
		os.system(f"terminal-notifier -title 'UTS' -message 'Failed page update ({e})'")

def get_unique_names(all_data):
	names = []
	for gw in all_data:
		for d in all_data[gw]:
			names.append(d['name'])
	return list(set(names))

def get_player_score(name,all_data):
	score = 0
	for gw in all_data:
		for d in all_data[gw]:

			if d['name'] == name:
				score += d['points']
				break
	return score

def leaderboard(all_data):

	mout.header('Leaderboard')

	# print(all_data[3][0]['name'])

	unique_names = get_unique_names(all_data)

	leader_data = []
	for name in unique_names:
		score = get_player_score(name, all_data)
		leader_data.append(dict(name=name,score=score))

	print(unique_names)

	html_buffer = '<table class="w3-table-all">\n'
	
	# header
	html_buffer += '<tr>\n'

	html_buffer += '<th class="w3-center">\n'
	html_buffer += 'Rank\n'
	html_buffer += '</th>\n'

	html_buffer += '<th class="w3-center">\n'
	html_buffer += 'Score\n'
	html_buffer += '</th>\n'

	html_buffer += '<th>\n'
	html_buffer += 'Name\n'
	html_buffer += '</th>\n'

	html_buffer += '</tr>\n'

	for i,d in enumerate(sorted(leader_data,key=lambda x: x['score'],reverse=True)):

		html_buffer += '<tr>\n'

		html_buffer += '<td class="w3-center">\n'

		if i == 0:
			html_buffer += '🥇\n'
		elif i == 1:
			html_buffer += '🥈\n'
		elif i == 2:
			html_buffer += '🥉\n'
		else:
			html_buffer += f'{i+1}\n'

		html_buffer += '</td>\n'

		html_buffer += '<td class="w3-center">\n'
		html_buffer += f"{d['score']}\n"
		html_buffer += '</td>\n'

		html_buffer += '<td>\n'
		html_buffer += f"{d['name']}\n"
		html_buffer += '</td>\n'

		html_buffer += '</tr>\n'

		print(d['name'],d['score'])
	
	html_buffer += '</table>\n'

	return html_buffer

def launchd_plist(interval=14400):

	f = open("/Users/mw00368/Library/LaunchAgents/com.mwinokan.uts.plist",'w')

	str_buffer = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
		<key>Label</key>
		<string>com.mwinokan.uts</string>
		<key>Program</key>
		<string>/Users/mw00368/Box Sync/Python/SolentFitness/scrape.py</string>
		<key>EnvironmentVariables</key>
		<dict>
			<key>PATH</key>
			<string>/Users/mw00368/miniconda3/bin:/Users/mw00368/miniconda3/condabin:/Library/TeX/texbin:/Users/mw00368/miniconda3/bin:/Users/mw00368/sh:/Users/mw00368/asap/x86_64:/Users/mw00368/Movies/autodownload:/Users/mw00368/Dropbox/MCal:/Users/mw00368/.local/bin:/Users/mw00368/usr/bin:/Users/mw00368/bin:/usr/local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/TeX/texbin:/usr/local/munki:/opt/X11/bin:/Library/Apple/usr/bin:/Library/Frameworks/Mono.framework/Versions/Current/Commands:/Users/mw00368/sh:/Users/mw00368/gromax:/Users/mw00368/AseMolPlot</string>
			<key>PYTHONPATH</key>
			<string>/Users/mw00368/tars_n_zips/PyRosetta4.Release.python39.mac.release-321:/Users/mw00368/pypackages/gpxpy-1.4.2:/Users/mw00368/pypackages/gpxpy-1.4.2:/Users/mw00368/asap/Python:/Users/mw00368/asap/x86_64:/Users/mw00368/.local/lib/python3.7/site-packages:/Users/mw00368/miniconda3/lib/python3.8/site-packages/::/Users/mw00368/py/:/Users/mw00368/AseMolPlot</string>
		</dict>
		<key>StandardInPath</key>
		<string>/Users/mw00368/Box Sync/Python/SolentFitness/daemon.stdin</string>
		<key>StandardOutPath</key>
		<string>/Users/mw00368/Box Sync/Python/SolentFitness/daemon.stdout</string>
		<key>StandardErrorPath</key>
		<string>/Users/mw00368/Box Sync/Python/SolentFitness/daemon.stderr</string>
		<key>WorkingDirectory</key>
		<string>/Users/mw00368/Box Sync/Python/SolentFitness</string>
		<key>StartInterval</key>"""
	str_buffer += f"        <integer>{interval}</integer>"
	str_buffer += """    </dict>
</plist>"""
		
	f.write(str_buffer)
	f.close()

	import os
	os.system("launchctl unload ~/Library/LaunchAgents/com.mwinokan.uts.plist")
	os.system("launchctl load ~/Library/LaunchAgents/com.mwinokan.uts.plist")

	print("/Users/mw00368/Library/LaunchAgents/com.mwinokan.uts.plist")
	print("start with:")
	print("launchctl start com.mwinokan.uts")
	print("see details with:")
	print("launchctl print gui/$UID/com.mwinokan.uts")

if __name__ == '__main__':
	main()
