import csv

DELIMITER = "#"

class CsvReaderWriter:
    def __init__(self, filename):
        self.filename = filename

    # def open(self):
    #     self.file = open(file_out, encoding="utf-8")
    #
    # def close(self):
    #     self.file.close()

    def write_tags_and_text(self, tags, text):
        tags.append(text)
        with open(self.filename, encoding="utf-8", mode="a", newline='') as file:
            csv_writer = csv.writer(file, delimiter=DELIMITER)
            csv_writer.writerow(tags)

csvReaderWriter = CsvReaderWriter('testFile.csv')
csvReaderWriter.write_tags_and_text(['uczelnia', 'agh'], 'AGH to super uczelnia')
csvReaderWriter.write_tags_and_text(['wydziały', 'agh'], 'AGH ma kilka wydziałów')
