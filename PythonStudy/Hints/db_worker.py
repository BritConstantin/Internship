import sqlite3


class DbWorker:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(f'{db_name}.db')
        self.db_name = db_name
    # done
    def create_table(self, table_name, cols):
        c = self.conn.cursor()
        cols_str = ""
        try:

            for col_name in cols.keys():
                cols_str += col_name + " " + cols[col_name]
            c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                        {col_name}
                        )""")

            c.execute("INSERT INTO users VALUES (1, 'JawkeRz')")

            # c.execute("SELECT * FROM users")
            # print(c.fetchall())

            # c.execute("INSERT INTO users VALUES (:argument_a, :argument_b)", {'argument_a': 'User1', 'argument_b': 1234})

            # conn.commit()  # commit the changes to the DB

            # to avoid the need to conn.commit() after every c.execute() we can use "with" statement:
            # with self.conn:
            #     c.execute("SELECT * FROM users")
            # print(c.fetchall())
        except sqlite3.OperationalError as e:
            print(self.create_table.__name__ + e)

    def print_table(self,table_name):
        c = self.conn.cursor()
        try:

            with self.conn:
                c.execute(f"SELECT * FROM {table_name}")
            print(c.fetchall())
        except sqlite3.OperationalError as e:
            print(self.create_table.__name__ + e)
    # fixme:
    def insert_row(self, table_name, row):
        c = self.conn.cursor()
        try:

            c.execute("INSERT INTO users VALUES (1, 'JawkeRz')")

            # c.execute("SELECT * FROM users")
            # print(c.fetchall())

            # c.execute("INSERT INTO users VALUES (:argument_a, :argument_b)", {'argument_a': 'User1', 'argument_b': 1234})

            # conn.commit()  # commit the changes to the DB

            # to avoid the need to conn.commit() after every c.execute() we can use "with" statement:
            # with conn:
            #     c.execute("SELECT * FROM users")
            # print(c.fetchall())
        except sqlite3.OperationalError as e:
            print(self.create_table.__name__ + e)

    def close_connection(self):
        self.conn.close()  # close the connection to the DB


if __name__ == '__main__':
    db_name = "users2"
    table_name = 'users'
    users_hat = {
        'message_id': 'integer',
        'user_id': 'integer',
        'message': 'string'
    }
    my_db = DbWorker(table_name)
    my_db.create_table(table_name,users_hat)
    my_db.print_table(table_name)
    # my_db.insert_row(table_name, )
    my_db.close_connection()
