import pandas as pd

from src.connection_manager import ConnectionManager
from src.read import read_sql_to_df
from src.write import write_to_excel

def main():
    print("Hello from template!")
    print("This is an example on how to use a context manager to automatically close the connection.")
    try:
        with ConnectionManager('GKK', role='campaign') as manager:
            # Accessing the ConnectionManager instance allows us to use all methods
            print(manager.get_connection_dict())

            # Create an SQLAlchemy connection to query the database
            conn = manager.get_connection()
             # Read first query into a dataframe
            df_1 = read_sql_to_df(
                sql_input = r'sqls\99_TEST.sql',
                conn = conn,
                print_sql = True,
                identifiers = {"segment": "c.RFM_DESC"},
                values = {"start_date": "2023-01-01", "end_date": "2023-12-31"}
            ) 
            # Read second query into a dataframe
            df_2 = read_sql_to_df(
                sql_input = r'sqls\99_TEST.sql',
                conn = conn,
                print_sql = True,
                identifiers = {"segment": "c.LIFECYCLE_DESC"},
                values = {"start_date": "2023-01-01", "end_date": "2023-12-31"}
            ) 
            # Read third query into a dataframe
            df_3 = read_sql_to_df(
                sql_input = r'sqls\99_TEST.sql',
                conn = conn,
                print_sql = True,
                identifiers = {"segment": "'ALL'"},
                values = {"start_date": "2023-01-01", "end_date": "2023-12-31"}
            )
        # The connection is automatically closed when exiting the context manager
        
        #Combine the dataframes into a single dataframe
        df_4 = pd.concat([df_1, df_2, df_3], ignore_index=True)
        # Create a list of dataframes and write each in a excel tab
        dfs = [df_1, df_2, df_3, df_4]
        # Write the DataFrames to an Excel file
        # write_to_excel(dfs, 'output.xlsx')
        # Optionally, you can specify sheet names for each DataFrame
        sheet_names = ['by RFM', 'by Lifecycle', 'total', 'combined']
        write_to_excel(dfs, 'output_context_manager.xlsx', sheet_names)

    except Exception as e:
        # Handle any exceptions that occur
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()





