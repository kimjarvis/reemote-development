def convert_to_df(data, columns=None):
    """Convert JSON data to DataFrame with specified columns"""
    # Define all available columns with their extraction logic
    all_columns = {
        'command': lambda item: item['op']['command'],
        'host': lambda item: item['host'],
        'guard': lambda item: item['op']['guard'],
        'changed': lambda item: item['changed'],
        'executed': lambda item: item['executed'],
        'stdout': lambda item: item['cp']['stdout'],
        'stderr': lambda item: item['cp']['stderr'],
        'exit_status': lambda item: item['cp']['exit_status'],
        'returncode': lambda item: item['cp']['returncode'],
        'env': lambda item: item.get('env', ''),
        'subsystem': lambda item: item.get('subsystem', ''),
        'exit_signal': lambda item: item.get('exit_signal', '')
    }

    # If no columns specified, use all columns
    if columns is None:
        columns = list(all_columns.keys())

    # Validate that all requested columns exist
    for col in columns:
        if col not in all_columns:
            raise ValueError(f"Column '{col}' is not available. Available columns: {list(all_columns.keys())}")

    rows = []
    for item in data:
        row = {}
        for col in columns:
            row[col] = all_columns[col](item)
        rows.append(row)

    # Create DataFrame with only the specified columns
    return pd.DataFrame(rows, columns=columns)
