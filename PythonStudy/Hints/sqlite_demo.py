#! Python3

import sqlite3
def main():
    conn = sqlite3.connect('users.db')   # creates the file if doesn't exists, or connect if exists

    # set up a cursor to execute SQL commands
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE IF NOT EXISTS users (
        userID integer,
        username text 
                )""")

        c.execute("INSERT INTO users VALUES (1, 'JawkeRz')")

        # c.execute("SELECT * FROM users")
        # print(c.fetchall())

        # c.execute("INSERT INTO users VALUES (:argument_a, :argument_b)", {'argument_a': 'User1', 'argument_b': 1234})

        # conn.commit()  # commit the changes to the DB

        # to avoid the need to conn.commit() after every c.execute() we can use "with" statement:
        with conn:
            c.execute("SELECT * FROM users")
        print(c.fetchall())
    except sqlite3.OperationalError as e:
        print(e)

    conn.close()    # close the connection to the DB
if __name__ == '__main__':
    main()