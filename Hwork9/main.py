import os
import sys
import csv
import json
import pickle

class BaseReader:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.data = []

    def load(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def apply_changes(self, changes):
        for change in changes:
            try:
                col, row, value = change.split(",")
                col, row = int(col.strip()), int(row.strip())
                while len(self.data) <= row:
                    self.data.append([])
                while len(self.data[row]) <= col:
                    self.data[row].append("")
                self.data[row][col] = value.strip()
            except Exception as e:
                print(f"Invalid change format '{change}': {e}")

    def display(self):
        for row in self.data:
            print(", ".join(row))


class CSVReader(BaseReader):
    def load(self):
        with open(self.src, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            self.data = [list(row) for row in reader]

    def save(self):
        with open(self.dst, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(self.data)


class JSONReader(BaseReader):
    def load(self):
        with open(self.src, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def save(self):
        with open(self.dst, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)


class PickleReader(BaseReader):
    def load(self):
        with open(self.src, "rb") as f:
            self.data = pickle.load(f)

    def save(self):
        with open(self.dst, "wb") as f:
            pickle.dump(self.data, f)


def get_reader(src, dst):
    ext = os.path.splitext(src)[1].lower()
    if ext == ".csv":
        return CSVReader(src, dst)
    elif ext == ".json":
        return JSONReader(src, dst)
    elif ext == ".pickle":
        return PickleReader(src, dst)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python reader.py source_file destination_file [changes...]")
        sys.exit(1)

    src, dst, *changes = sys.argv[1:]

    if not os.path.isfile(src):
        print(f"Error: {src} does not exist or is not a file.")
        directory = os.path.dirname(src) or "."
        print("Files in directory:", os.listdir(directory))
        sys.exit(1)

    try:
        reader = get_reader(src, dst)
    except ValueError as e:
        print(e)
        sys.exit(1)

    reader.load()
    reader.apply_changes(changes)
    reader.display()
    reader.save()
    print(f"Saved modified file to {dst}")


if __name__ == "__main__":
    main()
