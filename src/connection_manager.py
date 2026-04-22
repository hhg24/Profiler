import os
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from sqlalchemy.engine.base import Connection


class ConnectionManager:
    """
    A class to manage database connections for different business lines. 
    It uses SQLAlchemy to create and manage connections to the corresponding Snowflake database.

    Example usage of the Connection class with pandas following SQLAlchemy best practices:
        >>> from src.connection_manager import ConnectionManager
        >>> import pandas as pd
        >>> try:
        >>>     # Initialize the Connection object for the 'GKK' business line
        >>>     manager = ConnectionManager('GKK')
        >>>     conn = manager.get_connection() 
        >>>     # Define the SQL query
        >>>     sql = "SELECT CUSTOMERID FROM CORE_PROD.DATAMART_GKK.CUSTOMER_DIM_STD_GKK LIMIT 10"
        >>>     # Execute the query and load the result into a Pandas DataFrame
        >>>     df = pd.read_sql(sql, conn)
        >>>     # Print the DataFrame
        >>>     print(df)
        >>> except Exception as e:
        >>>     # Handle any exceptions that occur
        >>>     print(f"An error occurred: {e}")
        >>> finally:
        >>>     # Ensure the connection is closed
        >>>     manager.close()

    Alternatively, you can use the connection to execute raw SQL commands using the text wrapper:
        >>> from src.connection_manager import ConnectionManager
        >>> from sqlalchemy import text
        >>> try:
        >>>     # Initialize the Connection object for the 'GKK' business line
        >>>     conn = ConnectionManager('GKK').get_connection()
        >>>     # Define the SQL query
        >>>     sql = "SELECT CUSTOMERID FROM CORE_PROD.DATAMART_GKK.CUSTOMER_DIM_STD_GKK LIMIT 10"
        >>>     # Execute the query using the execute method of the connection object
        >>>     result = conn.execute(text("SELECT CURRENT_TIMESTAMP()"))
        >>>     print(result.fetchone())
        >>> except Exception as e:
        >>>     # Handle any exceptions that occur
        >>>     print(f"An error occurred: {e}")
        >>> finally:
        >>>     # Ensure the connection is closed
        >>>     manager.close()
    """

    def __init__(self, bl: str, platform: str = 'local', role: str = 'basic', warehouse: str = 'compute_wh'):
        """
        Initialize the Connection object.

        Parameters:
        bl (str): The business line identifier (e.g., 'GKK', 'LIN').
        platform (str): The platform type. Default is 'local'.
        role (str): Role name, can take 'basic', 'campaign', or 'emarsys' as values. Default is 'basic'.
            - 'basic': will use the role "ANALYST_BASIC_<BL>"
            - 'campaign' will use the role "ANALYST_CAMPAIGN_<BL>"
            - 'emarsys' will use the role "ANALYST_EMARSYS_<BL>"
        warehouse (str): Name of the warehouse to be used. Default is 'compute_wh'.
            - 'compute_wh': will use "compute_wh" X-small warehouse.
            - 'mdm_wh': will use "mdm_wh" X-small warehouse.
            - 'data_science_wh': will use "data_science_wh" Small warehouse.
            - 'campaign_wh': will use "campaign_wh" Medium warehouse.
        """
        self.bl = bl
        self.platform = platform
        self.role = role
        self.warehouse = warehouse
        self.engine = None
        self.connection = None

    def get_database_username(self) -> str:
        """
        Retrieve the username for the connection. If the environment variable
        PYTHON_ANALYST_USERNAME is not set, prompt the user to provide their username.

        Returns:
        str: The username to use for the connection.
        """
        try:
            # Check if the environment variable exists
            username = os.environ["PYTHON_ANALYST_USERNAME"]
        except KeyError:
            print(f"Environment variable 'PYTHON_ANALYST_USERNAME' not found.")
            # Ask the user to provide their username
            username = input("Please enter your HOC username [name@house-of-communication.com]: ").strip()
        return username

    def get_connection_dict(self) -> dict:
        """
        Construct the connection dictionary for a specific business line.

        Parameters:
        platform (str): The platform type, can be 'local' or 'cloud'. Default is 'local'.
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
                'role': f"LINDT_ANALYST_{self.role.upper()}_ALL"
            },
            'GKK': {
                'conn_url': "https://jn71015.west-europe.azure.snowflakecomputing.com/",
                'account': "jn71015.west-europe.azure",
                'database': "DWHSIGNA_PROD",
                'role': f"ANALYST_{self.role.upper()}_{self.bl.upper()}"
            },
            'SPS': {
                'conn_url': "https://jn71015.west-europe.azure.snowflakecomputing.com/",
                'account': "jn71015.west-europe.azure",
                'database': "DWHSIGNA_PROD",
                'role': f"ANALYST_{self.role.upper()}_{self.bl.upper()}"
            },
            'HOL': {
                'conn_url': "",
                'account': "",
                'database': "",
                'role': ""
            },
        }

        # Common connection variables
        try:
            common_conn = {
                'warehouse': self.warehouse,
                'user': self.get_database_username(),
                'schema': f"DM_ANALYST_{self.bl.upper()}",
                'password': None,  # Can be updated to fetch from a secure source
                'authenticator': "externalbrowser",
            }
        except KeyError as e:
            raise KeyError(f"Missing required environment variable: {e}")

        # Combine common and business line-specific connection variables
        conn_dict = {**common_conn, **bl_conn.get(self.bl, {})}

        # Validate required keys
        local_keys = ['user', 'account', 'database', 'schema', 'warehouse', 'role', 'authenticator']
        for key in local_keys:
            if key not in conn_dict or not conn_dict[key]:
                raise ValueError(f"Missing or invalid value for required key: {key}")
            
        if self.platform == 'local':
            return {key: conn_dict[key] for key in local_keys if key in conn_dict}
        else:
            return conn_dict

    def get_connection(self) -> Connection:
        """
        Open a database connection.

        Returns:
        Connection: An open database SQLAlchemy connection object.
        """
        print(self.get_connection_dict())

        if self.engine is None:
            # Create the SQLAlchemy engine
            conn_dict = self.get_connection_dict()
            self.engine = create_engine(URL(**conn_dict))

        # Open a connection
        self.connection = self.engine.connect()
        return self.connection

    def close(self):
        """
        Close the database connection and dispose of the engine.
        """
        if self.connection is not None:
            self.connection.close()
            self.connection = None

        if self.engine is not None:
            self.engine.dispose()
            self.engine = None

    # Define __enter__ and __exit__ methods for context manager support
    def __enter__(self):
        """
        Enter the runtime context related to this object.

        Returns:
        Connection: The current instance of the Connection class.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context related to this object.

        Parameters:
        exc_type: The exception type.
        exc_value: The exception value.
        traceback: The traceback object.
        """
        self.close()