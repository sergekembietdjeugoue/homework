#!/usr/bin/env pythonProject2
import sys
import os
import csv

def print_usage():
    print("Usage: python reader.py <src> <dst> <change1> <change2> ...")
    print("Example: python reader.py in.csv out.csv 0,0,piano 3,1,mug 1,2,17 3,3,0")

def list_files_in_directory(path):
    directory = os.path.dirname(os.path.abspath(path)) or "."
    print(f"Files in directory '{directory}':")
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            print("  ", f)

def apply_changes(data, changes):
    for change in changes:
        try:
            x_str, y_str, value = change.split(",", 2)
            x, y = int(x_str), int(y_str)

            if y < 0 or y >= len(data):
                print(f"Warning: Row index {y} out of range. Skipping '{change}'.")
                continue
            if x < 0 or x >= len(data[y]):
                print(f"Warning: Column index {x} out of range in row {y}. Skipping '{change}'.")
                continue

            data[y][x] = value

        except ValueError:
            print(f"Warning: Invalid change format '{change}'. Expected format 'X,Y,value'. Skipping.")
        except Exception as e:
            print(f"Error applying change '{change}': {e}")

def display_csv(data):
    print("\nModified CSV content:")
    for row in data:
        print(",".join(row))
    print()

def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    changes = sys.argv[3:]

    # Check if source file exists
    if not os.path.exists(src) or not os.path.isfile(src):
        print(f"Error: Source file '{src}' does not exist or is not a file.")
        list_files_in_directory(src)
        sys.exit(1)

    # Read CSV file
    try:
        with open(src, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = [row for row in reader]
    except Exception as e:
        print(f"Error reading '{src}': {e}")
        sys.exit(1)

    # Apply changes
    if changes:
        apply_changes(data, changes)

    # Display and write the modified CSV
    display_csv(data)

    try:
        with open(dst, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"Modified file saved to '{dst}'.")
    except Exception as e:
        print(f"Error writing to '{dst}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
