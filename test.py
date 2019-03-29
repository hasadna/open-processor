from parser_report import ExcelParser, FakeLogger

path = "C:\\Users\\roy.DM\\Projects\\open_processor\\assets\\513026484_gs.xlsx"

parser = ExcelParser(logger=FakeLogger)
parsed = parser.parse_file(file_path=path)

print(parsed)
