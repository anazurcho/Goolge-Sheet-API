file_id = '1bhDZkBRQG3F-BTxfBd9daHquo6jhfdbCoKgzd34PjLI'

FILE_TYPES = {'pdf': 'application/pdf',
              'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}

odoo_data = ['პირველი', 'მეორე', 'მესამე', 'მეოთხე', 'მე-5', 'მე-6', 'მე-7', 'მე-8']
odoo_data_1 = ['პირველის', 'პირველისა', 'პირველი']
values = {"userEnteredValue": {"stringValue": "anuki"}}
anabana = 'anabana'
string_value = lambda x: {"userEnteredValue": {"stringValue": str(x)}}
value = [string_value(row) for row in odoo_data]
value_2 = [string_value(row) for row in odoo_data_1]
value_3 = [{'values': [string_value(row) for row in odoo_data_1]}]

# data = {["Item", "Cost", "Stocked", "Ship Date"],
#         ["Wheel", "$20.50", "4", "3/1/2016"],
#         ["Door", "$15", "2", "3/15/2016"],
#         ["Engine", "$100", "1", "3/20/2016"],
#         ["Totals", "=SUM(B2:B4)", "=SUM(C2:C4)", "=MAX(D2:D4)"]}

spread_sheet_value = {
    'properties': {
        'title': 'Anzu Report'
    },
    'sheets': [
        {
            'properties': {
                'sheetId': 0,
                'title': 'პირველი შითი',
            },
            'data': [
                {
                    'startRow': 0,
                    'startColumn': 0,
                    'rowData': [
                        {
                            'values': value
                        }
                    ]
                },
                {
                    'startRow': 1,
                    'startColumn': 1,
                    'rowData': [
                        {
                            'values': value
                        }
                    ]
                },
            ],
        },
        {
            'properties': {
                'sheetId': 1,
                'title': 'მეორე შითი',
            },
            'data': [
                {
                    'startRow': 0,
                    'startColumn': 0,
                    'rowData': [
                        {
                            'values': value
                        }
                    ]
                },
                {
                    'startRow': 0,
                    'startColumn': 1,
                    'rowData': [
                        {
                            'values': value_2
                        }
                    ]
                },
            ],
        }
    ],

}


def list_spreadsheet_gspread(self):
    gs = gspread.authorize(self.credentials)
    sh = gs.open_by_key(file_id).sheet1
    student_data = ['Emily', 'Watson', 89]
    new_row_index = 6
    sh.insert_row(student_data, new_row_index)

    values_row = sh.row_values(new_row_index)
    print(values_row)