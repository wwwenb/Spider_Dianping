import os
import csv


class SaveFile:

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def save_message(self, file_name, message, mode="w", encoding="utf-8"):
        with open(file_name, mode=mode, encoding=encoding) as f:
            f.write(message)

    def write_csv_row(self, file_name, message, mode="a", encoding="utf-8"):
        # 使用newline来解决每写入一行多出空行的问题
        with open(file_name, mode=mode, encoding=encoding, newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(message)

    def write_csv_rows(self, file_name, message, mode="a", encoding="utf-8"):
        with open(file_name, mode=mode, encoding=encoding, newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(message)


save_file = SaveFile()