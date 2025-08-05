def basic_summary(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": df.isnull().sum().sum(),
        "column_types": df.dtypes.astype(str).to_dict()
    }