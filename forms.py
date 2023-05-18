#!/usr/bin/env python3

from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/forms.body.readonly",'https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json',scope)

# client = gspread.authorize(creds)

# SCOPES = "https://www.googleapis.com/auth/forms.body.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

# Prints the title of the sample form:
form_id = 'UTS Week 2'
result = service.forms().get(formId=form_id).execute()
print(result)

