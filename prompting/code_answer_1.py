import os
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from sqlalchemy.engine.base import Engine


class Connection:
    def __init__(self, bl: str):
        """
        Initialize the BusinessLine object.

        Parameters:
        bl (str): The business line identifier (e.g., 'GKK', 'LIN').
        """
        self.bl = bl

    def get_connection_dict(self, role: str = 'basic', warehouse: str = 'data_science_wh') -> dict:
        """
        Construct the connection dictionary for a specific business line.

        Parameters:
        role (str): Role name, can take 'basic', 'campaign', or 'emarsys' as values. Default is 'basic'.
        warehouse (str): Name of the warehouse to be used. Default is 'data_science_wh'.

        Returns:
        dict: A dictionary containing connection parameters.
        """
        # Business line-specific connection variables
        bl_conn = {
            'LIN': {
                'conn_url': "https://er29506.west-europe.azure.snowflakecomputing.com/",
                'account': "er29506.west-europe.azure",
                'database': "CORE_PROD",
            },
            'GKK': {
                'conn_url': "https://jn71015.west-europe.azure.snowflakecomputing.com/",
                'account': "jn71015.west-europe.azure",
                'database': "DWHSIGNA_PROD",
            },
            'SPS': {
                'conn_url': "https://jn71015.west-europe.azure.snowflakecomputing.com/",
                'account': "jn71015.west-europe.azure",
                'database': "DWHSIGNA_PROD",
            },
            'HOL': {
                'conn_url': "",
                'account': "",
                'database': "",
            },
        }

        # Common connection variables
        try:
            common_conn = {
                'warehouse': warehouse,
                'user': os.environ["PYTHON_ANALYST_USERNAME"],
                'schema': f"DM_ANALYST_{self.bl.upper()}",
                'role': f"ANALYST_{role.upper()}_{self.bl.upper()}",
                'password': None,  # Can be updated to fetch from a secure source
                'authenticator': "externalbrowser",
            }
        except KeyError as e:
            raise KeyError(f"Missing required environment variable: {e}")

        # Combine common and business line-specific connection variables
        conn_dict = {**common_conn, **bl_conn.get(self.bl, {})}

        # Validate required keys
        required_keys = ['user', 'account', 'database', 'schema', 'warehouse', 'role', 'authenticator']
        for key in required_keys:
            if key not in conn_dict or not conn_dict[key]:
                raise ValueError(f"Missing or invalid value for required key: {key}")

        return conn_dict

    def create_engine(self, role: str = 'basic', warehouse: str = 'data_science_wh') -> Engine:
        """
        Create a SQLAlchemy engine for the specified business line.

        Parameters:
        role (str): Role name, can take 'basic', 'campaign', or 'emarsys' as values. Default is 'basic'.
        warehouse (str): Name of the warehouse to be used. Default is 'data_science_wh'.

        Returns:
        Engine: A SQLAlchemy engine object.
        """
        # Get the connection dictionary
        conn_dict = self.get_connection_dict(role=role, warehouse=warehouse)

        # Create and return the SQLAlchemy engine
        return create_engine(URL(**conn_dict))