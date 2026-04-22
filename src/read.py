import os
from typing import Union, Dict
from pandas import DataFrame, read_sql
from sqlalchemy.engine import Connection
from sqlalchemy.sql import text

def execute_sql(
    sql_input: Union[str, os.PathLike],
    conn: Connection,
    print_sql: bool = False,
    identifiers: Dict[str, str] = None,
    values: Dict[str, Union[str, int]] = None
) -> None:
    """
    Executes an SQL statement provided as a string or from a file, with support for variable substitution.

    Parameters:
    conn: The database connection object.
    sql_input (str or os.PathLike): The SQL statement as a string or the file path to an SQL file.
    identifiers (dict): Variables to substitute for placeholders written as {var} in the SQL.
    values (dict): Variables to substitute for placeholders written as :var in the SQL.

    Returns:
    None
    """
    try:
        # Check if the input is a file path
        if os.path.isfile(sql_input):
            # Read the SQL statement from the file
            with open(sql_input, 'r', encoding='utf-8') as file:
                sql_statement = file.read()
        else:
            # Treat the input as a raw SQL statement
            sql_statement = sql_input

        # Substitute curly bracket variables
        if identifiers:
            sql_statement = sql_statement.format(**identifiers)

        if print_sql:
            # Substitute parameterized variables for debugging
            if values:
                debug_sql = sql_statement
                for key, value in values.items():
                    placeholder = f":{key}"
                    debug_sql = debug_sql.replace(placeholder, repr(value))  # Replace :var with its value
            else:
                debug_sql = sql_statement
            # Print the SQL statement for debugging
            print(f"SQL statement:\n{debug_sql}")

        # Execute the SQL statement with parameterized variables
        result = conn.execute(text(sql_statement), values or {})
        print("SQL query executed successfully.")
        #print(f"Result: {result}")

    except Exception as e:
        # Handle any exceptions and return a failure message
        print(f"SQL query failed: {e}")

def read_sql_to_df(
    sql_input: Union[str, os.PathLike],
    conn: Connection,
    print_sql: bool = False,
    identifiers: Dict[str, str] = None,
    values: Dict[str, Union[str, int]] = None
) -> DataFrame:
    """
    Executes an SQL statement provided as a string or from a file, with support for variable substitution,
    and returns the result as a Pandas DataFrame.

    Parameters:
    conn: The database connection object.
    sql_input (str or os.PathLike): The SQL statement as a string or the file path to an SQL file.
    identifiers (dict): Variables to substitute for placeholders written as {var} in the SQL.
    values (dict): Variables to substitute for placeholders written as :var in the SQL.

    Returns:
    pd.DataFrame: The result of the SQL query as a Pandas DataFrame.
    """
    try:
        # Check if the input is a file path
        if os.path.isfile(sql_input):
            # Read the SQL statement from the file
            with open(sql_input, 'r', encoding='utf-8') as file:
                sql_statement = file.read()
        else:
            # Treat the input as a raw SQL statement
            sql_statement = sql_input

        # Substitute curly bracket variables
        if identifiers:
            sql_statement = sql_statement.format(**identifiers)

        # Substitute parameterized variables for debugging
        if values:
            for key, value in values.items():
                placeholder = f":{key}"
                sql_statement = sql_statement.replace(placeholder, repr(value))  # Replace :var with its value

            
        if print_sql:
            # Print the SQL statement for debugging
            print(f"SQL statement:\n{sql_statement}")

        # Execute the SQL statement with parameterized variables and return the result as a DataFrame
        result = read_sql(sql_statement, conn)
        print("SQL query executed successfully.")
        return result  # Return the DataFrame if successful

    except Exception as e:
        # Handle any exceptions and return a failure message
        print(f"SQL query failed: {e}")
        return DataFrame()  # Return an empty DataFrame on failure