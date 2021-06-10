#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import io
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload

import data


SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
CLIENT_SECRET_FILE = 'client_secret.json'
TOKEN_FILE = 'token.pickle'
file_id = '1zFJ_fy3biT_DVgjQ87Yo5mBn82QGcJjENEGWkahyqZU'


def create_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPE)
            creds = flow.run_local_server()
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds


class GoogleAPI:

    def __init__(self):
        self.credentials = create_credentials()
        self.sheet_service = build('sheets', 'v4', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def create_spreadsheet(self):
        spreadsheet = data.spread_sheet_value
        spreadsheet = self.sheet_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        print(spreadsheet.get('spreadsheetId'), spreadsheet.get('body'))
        return spreadsheet.get('spreadsheetId')

    def download_spreadsheet(self, mime_type):

        request = self.drive_service.files().export_media(fileId=file_id, mimeType=data.FILE_TYPES[mime_type])
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        file_name = 'ფაილი'
        done = False

        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)

        with open(os.path.join('./Downloads', f'{file_name}.{mime_type}'), 'wb') as f:
            f.write(fh.read())
            f.close()

    def get_values(self, spreadsheet_id, range_name):
        service = self.sheet_service
        # [START sheets_get_values]
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        print(rows)
        print('{0} rows retrieved.'.format(len(rows)))
        return result

    def get_sheets(self, spreadsheet_id):
        service = self.sheet_service
        # [START sheets_get_values]
        result = service.spreadsheets().get(
            spreadsheetId=spreadsheet_id).execute()
        sheets = result.get('sheets', [])
        print(sheets)
        return result


if __name__ == "__main__":
    obj = GoogleAPI()
    print(data.FILE_TYPES)
    print(data.FILE_TYPES['pdf'])
    i = int(input("Enter your choice: 1 - create File. 2 - download File. 3- get data. 4 - get sheets. 5 - list of spreadsheet\n"))
    if i == 1:
        obj.create_spreadsheet()
    if i == 2:
        o = int(input("Enter your choice: 1 - Download pdf. 2 - Download xlsx.\n"))
        if o == 1:
            obj.download_spreadsheet(mime_type='pdf')
        if o == 2:
            obj.download_spreadsheet(mime_type='xlsx')
    if i == 3:
        obj.get_values(spreadsheet_id=file_id, range_name='A:Z')
    if i == 4:
        obj.get_sheets(spreadsheet_id=file_id)
    if i == 5:
        obj.list_spreadsheet_gspread()
    else:
        exit()
