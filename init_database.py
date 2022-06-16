import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main(database):
    sql_create_blocks_table = """CREATE TABLE IF NOT EXISTS Blocks (
                                        id integer PRIMARY KEY,
                                        transactions text NOT NULL,
                                        timestamp integer NOT NULL,
                                        previousHash text NOT NULL,
                                        hash text NOT NULL,
                                        reward integer NOT NULL,
                                        nonce integer NOT NULL,
                                        difficulty integer NOT NULL
                                    ); """

    sql_create_transactions_table = """CREATE TABLE IF NOT EXISTS Transactions (
                                    id integer PRIMARY KEY,
                                    type integer NOT NULL,
                                    inputs text NOT NULL,
                                    outputs text NOT NULL,
                                    timestamp text NOT NULL,
                                    transactionId text NOT NULL,
                                    fees integer NOT NULL
                                );"""

    sql_create_unconfirmed_transactions_table = """CREATE TABLE IF NOT EXISTS Unconfirmed_Transactions (
                                    id integer PRIMARY KEY,
                                    type integer NOT NULL,
                                    inputs text NOT NULL,
                                    outputs text NOT NULL,
                                    timestamp text NOT NULL,
                                    transactionId text NOT NULL,
                                    fees integer NOT NULL
                                );"""

    sql_create_UTXO_table = """CREATE TABLE IF NOT EXISTS UTXO (
                                    id integer PRIMARY KEY,
                                    value integer NOT NULL,
                                    address text NOT NULL,
                                    transactionId text NOT NULL,
                                    lockingScript text NOT NULL
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tablesS
    if conn is not None:
        # create Blocks, Nodes, Transactions and Unconfirmed_Transactions tables
        create_table(conn, sql_create_blocks_table)
        create_table(conn, sql_create_transactions_table)
        create_table(conn, sql_create_unconfirmed_transactions_table)
        create_table(conn, sql_create_UTXO_table)
    else:
        print("Error! cannot create the database connection.")


main("database.db")
