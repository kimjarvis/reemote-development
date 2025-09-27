import pandas as pd
import tabulate as tabulate
import json

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

# Create lists for the three dimensions
rows = []
for item in data:
    row = {
        'command': item['op']['command'],
        'host': item['host'],
        'guard': item['op']['guard'],
        'changed': item['changed'],
        'executed': item['executed'],
        'stdout': item['cp']['stdout'],
        'stderr': item['cp']['stderr'],
        'exit_status': item['cp']['exit_status'],
        'returncode': item['cp']['returncode']
    }
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Convert ALL values to strings to avoid tabulate issues
def safe_convert(value):
    """Convert any value to a safe string representation"""
    if value is None:
        return ''
    elif isinstance(value, bool):
        return 'True' if value else 'False'
    else:
        return str(value)

# Create a new DataFrame with all values converted to strings
df_display = df.copy()
for col in df_display.columns:
    df_display[col] = df_display[col].apply(safe_convert)

# Convert DataFrame to a format suitable for tabulate
table_data = df_display.values.tolist()
headers = df_display.columns.tolist()

# Use tabulate without maxcolwidths parameter to avoid compatibility issues
print(tabulate.tabulate(table_data, headers=headers, tablefmt='grid'))
