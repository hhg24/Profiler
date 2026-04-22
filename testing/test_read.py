def main():
    from src.read import execute_sql
    from src.connection_manager import ConnectionManager

    #setup connection
    manager = ConnectionManager('GKK')
    conn = manager.get_connection()

    sql = """
        SELECT
            CUSTOMERID,
            FIRSTNAME
        FROM 
            CORE_PROD.DATAMART_GKK.CUSTOMER_DIM_STD_GKK
        LIMIT 10
    """

    # Read the Excel file
    execute_sql(conn, sql)

    manager.close()

if __name__ == "__main__":
    main()