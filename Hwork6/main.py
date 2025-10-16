#!/usr/bin/env python3
import sys
import os
import csv

def main():
    # Ensure correct usage
    if len(sys.argv) < 3:
        print("Usage: reader.py <src> <dst> <change1> <change2> ...")
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    changes = sys.argv[3:]

    # Check if source file exists
    if not os.path.isfile(src):
        print(f"Error: '{src}' does not exist or is not a file.")
        directory = os.path.dirname(src) or "."
        print("Files in the same directory:")
        try:
            for f in os.listdir(directory):
                print(f)
        except FileNotFoundError:
            print(f"Directory '{directory}' not found.")
        sys.exit(1)

    # Load CSV into memory
    try:
        with open(src, newline="", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            data = [row for row in reader]
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Apply changes
    for change in changes:
        try:
            col_str, row_str, value = change.split(",", 2)
            x = int(col_str)
            y = int(row_str)

            if y < 0 or y >= len(data):
                print(f"Warning: Row {y} out of range, skipping change '{change}'.")
                continue
            if x < 0 or x >= len(data[y]):
                print(f"Warning: Column {x} out of range, skipping change '{change}'.")
                continue

            data[y][x] = value
        except ValueError:
            print(f"Warning: Invalid change format '{change}', should be X,Y,value. Skipping.")
        except Exception as e:
            print(f"Warning: Error applying change '{change}': {e}")

    # Display modified CSV content
    print("\nModified CSV content:")
    for row in data:
        print(",".join(row))

    # Save modified CSV
    try:
        with open(dst, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerows(data)
        print(f"\nModified file saved to '{dst}'.")
    except Exception as e:
        print(f"Error writing to destination file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()