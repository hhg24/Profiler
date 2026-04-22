#import xlsxwriter
import pandas as pd

def write_to_excel(data, file_name, sheet_names=None):
    """
    Write a DataFrame or a list of DataFrames to an Excel file with optional sheet names.

    Parameters:
    data (pd.DataFrame or list of pd.DataFrame): The DataFrame(s) to write to the Excel file.
    file_path (str): The path to save the Excel file.
    sheet_names (str or list of str, optional): The name(s) of the sheet(s). If not provided, default names will be used.

    Returns:
    None
    """
    # Define the file path
    file_path = f"./results/{file_name}"
    # Create an Excel writer object
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        if isinstance(data, pd.DataFrame):
            # Handle a single DataFrame
            sheet_name = sheet_names if isinstance(sheet_names, str) else 'Sheet1'
            data.to_excel(writer, sheet_name=sheet_name, index=False)
        elif isinstance(data, list):
            # Handle a list of DataFrames
            if sheet_names is None:
                # Default sheet names if none are provided
                sheet_names = [f"Sheet{i + 1}" for i in range(len(data))]
            elif not isinstance(sheet_names, list) or len(sheet_names) != len(data):
                raise ValueError("sheet_names must be a list with the same length as the data list.")
            
            for df, sheet_name in zip(data, sheet_names):
                if not isinstance(df, pd.DataFrame):
                    raise ValueError(f"All elements in the data list must be DataFrames.")
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            raise ValueError("Input data must be a DataFrame or a list of DataFrames.")