from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from os import path
import apiclient, httplib2, json


class Sheets:
    def __init__(self) -> None:
        self.len_of_row: int = 6
        self.service = None

    def read_sheet(self, whichDate: str | None = None, isNeed: bool = False) -> str | list[str]:
        if self.service == None:
            return "Fail: module wasn't started"
        # Пример чтения файла
        try:
            values = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range='A1:F200',
                majorDimension='ROWS'
            ).execute()
        except:
            if isNeed == True:
                return "Fail: cannot write"
            else:
                return "Fail: cannot read"
        response = values.get("values")
        sheet: list[str] = list()
        columns_title: list = list()
        for row in response:
            columns: list[str | None] = list()
            for index in range(0, self.len_of_row):
                try:
                    cell = row[index]
                except:
                    cell = None
                columns.append(cell)
            if response.index(row) != 0:
                day_data: str = str()
                for i in range(0, self.len_of_row):
                    day_data += str(f"[{columns_title[i]}]: {columns[i]}\n")
                sheet.append(day_data)
            else:
                for i in range(0, self.len_of_row):
                    columns_title.append(columns[i])
        if isNeed == True:
            return sheet
        else:
            if whichDate != None:
                if whichDate == 'today':
                    whichDate = self.get_current_date()
                for column in sheet:
                    if column.find(whichDate) != -1:
                        return str(column)
            else:
                date: str = self.get_current_date()
                required_data: str = str()
                for column in sheet:
                    if column.find(date) != -1:
                        index: int = sheet.index(column)
                        if index-2 > 0:
                            for i in range(index-2, index):
                                required_data += str(f'{sheet[i]}\n')
                        required_data += str(f'{column}\n')
                        if len(sheet)-2 > index:
                            for i in range(index+1, index+3):
                                required_data += str(f'{sheet[i]}\n')
                return required_data
                

    def write_sheet(self, data: list) -> None:
        if self.service == None:
            return "Fail: module wasn't started"
        while len(data) != 5:
            data.append(str())
        sheet: list[str] = self.read_sheet(isNeed= True)
        if type(sheet) == str:
            return sheet
        colum_number: int = int()
        for column in sheet:
            if column.find(data[0]) != -1:
                colum_number = sheet.index(column)+2
        data_to_send: dict = {"range": str(f'C{colum_number}:F{colum_number}'), "majorDimension": "ROWS",
                                "values": [[data[1], data[2], data[3], data[4]]]
                            }

#        print(f'data: {data}, position: {position}')
        # Пример записи в файл
        try:
            values = self.service.spreadsheets().values().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={
                            "valueInputOption": "USER_ENTERED",
                            "data": [data_to_send,]
                        }
                ).execute()
            return "Success"
        except:
            return "Fail: cannot write"

    def get_current_date(self) -> str:
        incorrect_date = str(datetime.now())
        incorrect_date = incorrect_date.split()
        incorrect_date = incorrect_date[0].split("-")
        year: str = incorrect_date[0].split('0')
        return str(f"{incorrect_date[2]}.{incorrect_date[1]}.{year[1]}")

    def start(self, spreadsheet_id: str | None = None) -> str:
        if (path.isfile("src/lib/lib_plugins/google/sheets/spreadsheetId.json") == True) & (spreadsheet_id == None): 
            with open("src/lib/lib_plugins/google/sheets/spreadsheetId.json", "r") as File:
                data: dict = json.load(File)
                self.spreadsheet_id: str = data.get("spreadsheet_id")
        elif ((path.isfile("src/lib/lib_plugins/google/sheets/spreadsheetId.json") == False) | (path.isfile("src/lib/lib_plugins/google/sheets/spreadsheetId.json") == True)) & (spreadsheet_id != None): 
            self.spreadsheet_id: str = spreadsheet_id
            with open("src/lib/lib_plugins/google/sheets/spreadsheetId.json", "w") as File:
                json.dump({"spreadsheet_id": self.spreadsheet_id},File)
        else:
            return "Fail: cannot find spreadsheet_id"
        if path.isfile('src/lib/lib_plugins/google/sheets/creds.json') != False:
            CREDENTIALS_FILE = 'src/lib/lib_plugins/google/sheets/creds.json'
            # ID Google Sheets документа (можно взять из его URL)
            # Авторизуемся и получаем service — экземпляр доступа к API
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                CREDENTIALS_FILE,
                ['https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'])
            httpAuth = credentials.authorize(httplib2.Http())
            self.service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
            return "Success"
        else:
            return "Fail: cannot find creds.json"
