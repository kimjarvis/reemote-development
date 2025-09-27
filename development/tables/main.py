import pandas as pd
import tabulate
import json

from development.tables.convert_to_aggrid import convert_to_aggrid
from development.tables.convert_to_df import convert_to_df
from development.tables.convert_to_tabulate import convert_to_tabulate


def main():
    """Main function to read file and process data"""
    try:
        with open('result.json', 'r') as file:
            content = file.read().strip()
            if not content:
                print("Error: result.json file is empty!")
                exit(1)
            data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print("Please check the format of your result.json file")
        exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        exit(1)

    # Convert JSON data to DataFrame with specified columns
    columns = ["command", "host", "stdout"]
    df = convert_to_df(data, columns)

    # Convert DataFrame to tabulated table
    table = convert_to_tabulate(df)

    # Print the tabulated table
    print(table)

    columns, rows= convert_to_aggrid(df)
    print(columns)
    print(rows)

if __name__ == "__main__":
    main()