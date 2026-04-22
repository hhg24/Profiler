import os
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from sqlalchemy.engine.base import Engine

class BusinessLine:
    def __init__(self, bl):
        self.bl = bl

    def get_connection_dict(self, role:str = 'basic', warehouse:str = 'data_science_wh') -> dict:
        """
        Function to get the connection dictionary for a specific business line.
        
        Parameters:
        role (str): Role name, can take 'basic', 'campaign' or 'emarsys' as values. Default is 'basic'.
        warehouse (str): Name of the warehouse to be used. Default is 'data_science_wh'.
        """
        # Add business line specific connection variables
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
                'account': ""
                }
            # Add more BL configurations as needed
            }
        
        # Add common connection variables
        common_conn = {
            'warehouse': warehouse,
            'user': os.environ["PYTHON_ANALYST_USERNAME"],
            'schema': f"DM_ANALYST_{self.bl.upper()}",
            'role' : f"ANALYST_{role.upper()}_{self.bl.upper()}",
            'password': None,
            'authenticator': "externalbrowser"
            }

        # Combine the common and BL specific connection variables
        conn_dict = {**common_conn, **bl_conn.get(self.bl, {})}

        return conn_dict
    
    def create_engine(self, role:str = 'basic', warehouse:str = 'data_science_wh') -> Engine:
        """"
        Function to get the connection dictionary for a specific business line.
        
        Parameters:
        role (str): Role name, can take 'basic', 'campaign' or 'emarsys' as values. Default is 'basic'.
        warehouse (str): Name of the warehouse to be used. Default is 'data_science_wh'.
        """

        raw_dict = self.get_connection_dict(role=role, warehouse=warehouse)

        # select only required keys for the connection string
        required_keys = ['user', 'account', 'database', 'schema', 'warehouse', 'role', 'authenticator']
        conn_dict = {key: raw_dict[key] for key in required_keys if key in raw_dict}


        engine = create_engine(URL(**conn_dict))

        return engine