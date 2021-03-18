import gspread
from oauth2client.service_account import ServiceAccountCredentials

# From Google API quickstart
#from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Code from https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/


# def fetchVocabSheetData():
#     # define the scope
#     scope = ['https://spreadsheets.google.com/feeds',
#              'https://www.googleapis.com/auth/drive']

#     # add credentials to the account
#     creds = ServiceAccountCredentials.from_json_keyfile_name(
#         'GREVocabTester-1279d77e0b83.json', scope)

#     # authorize the clientsheet
#     client = gspread.authorize(creds)

#     # get the instance of the Spreadsheet
#     sheet = client.open('GRE_Vocab_List')

#     # get the first sheet of the Spreadsheet
#     sheet_instance = sheet.get_worksheet(0)

#     # get all the records of the data
#     records_data = sheet_instance.get_all_records()

#     return records_data

# # Code from Google Sheet API QuickStart Page


def fetchVocabSheetData():
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'Google_Sheet_API/GREVocabTester-1279d77e0b83.json', SCOPES)

    service = build('sheets', 'v4', credentials=creds)

    # The ID of the spreadsheet to retrieve data from.
    # TODO: Update placeholder value.
    spreadsheet_id = '1hGw6e1lVBJa0axT4fm3qZzmvVIzW7Xcl4FLN43YcDEs'

    # Sheet1 A to E collumn
    range_ = '工作表1!A:F'

    # How values should be represented in the output.
    # The default render option is ValueRenderOption.FORMATTED_VALUE.
    value_render_option = 'FORMATTED_VALUE'

    # How dates, times, and durations should be represented in the output.
    # This is ignored if value_render_option is
    # FORMATTED_VALUE.
    # The default dateTime render option is [DateTimeRenderOption.SERIAL_NUMBER].
    date_time_render_option = ''

    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_, valueRenderOption=value_render_option)
    response = request.execute()

    # spreadsheets.values
    # {
    #   "range": string,
    #   "majorDimension": enum (Dimension),
    #   "values": [
    #     array
    #   ]
    # }
    values = response.get("values")

    return values
