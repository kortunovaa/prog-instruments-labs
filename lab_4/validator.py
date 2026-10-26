import csv
import re
from checksum import calculate_checksum, serialize_result

class CSVValidator:
    """Класс для валидации CSV-файлов с помощью регулярных выражений."""
    
    def __init__(self, file_path: str, encoding: str = 'utf-16', delimiter: str = ';'):
        self.file_path = file_path
        self.encoding = encoding
        self.delimiter = delimiter
        self.patterns = {
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "height": r"^[0-2]\.\d{2}$",
            "snils": r"^\d{11}$",
            "passport": r"^\d{2} \d{2} \d{6}$",
            "occupation": r"^[A-Za-zА-Яа-яЁё\s-]+$",
            "longitude": r"^-?(?:180(?:\.0+)?|(?:1[0-7]\d|[1-9]?\d)\.\d+)$",
            "hex_color": r"^#[0-9a-fA-F]{6}$",
            "issn": r"^\d{4}-\d{4}$",
            "locale_code": r"^[a-z]{2}(-[a-z]{2})?$",
            "time": r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d\.\d{6}$"
        }

    def _is_row_valid(self, row: dict) -> bool:
        """Проверяет одну строку. Возвращает True, если строка валидна."""
        for field, value in row.items():
            if field in self.patterns:
                if not re.match(self.patterns[field], value):
                    return False
        return True

    def find_invalid_rows(self) -> list:
        """Читает файл и возвращает список индексов невалидных строк."""
        invalid_rows = []
        with open(self.file_path, "r", encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            for idx, row in enumerate(reader):
                if not self._is_row_valid(row):
                    invalid_rows.append(idx)
        return invalid_rows


def main():
    validator = CSVValidator(file_path="11.csv")
    invalid_rows = validator.find_invalid_rows()
    
    checksum = calculate_checksum(invalid_rows)
    print(f"Найдено невалидных строк: {len(invalid_rows)}")
    print(f"Контрольная сумма: {checksum}")
    
    serialize_result(variant=11, checksum=checksum)

if __name__ == "__main__":
    main()