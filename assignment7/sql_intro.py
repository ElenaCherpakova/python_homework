import sqlite3
from datetime import datetime, timedelta


def add_publisher(cursor, name):
    try:
        cursor.execute(
            "INSERT INTO Publishers (publisher_name) VALUES (?)", (name,))
        print(f"Publisher {name} added successfully.")
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database.")


def add_magazines(cursor, name, publisher):
    cursor.execute(
        "SELECT * FROM Publishers WHERE publisher_name = ?", (publisher,))
    results = cursor.fetchall()
    if len(results) > 0:
        publisher_id = results[0][0]
    else:
        print(f"There is no publisher named {publisher}.")
        return
    try:
        cursor.execute(
            "INSERT INTO Magazines (magazine_name, publisher_id) VALUES (?, ?)", (name, publisher_id))
        print(f"Magazine {name} added successfully.")

    except sqlite3.IntegrityError:
        print(f"Magazine {name} is already in database.")


def add_subscriber(cursor, name, address):
    cursor.execute(
        "SELECT * FROM Subscribers WHERE subscriber_name = ? AND address = ?", (name, address))
    results = cursor.fetchall()
    if len(results) > 0:
        print(
            f"There is already a subscriber named {name} with address {address}.")
        return
    try:
        cursor.execute(
            "INSERT INTO Subscribers (subscriber_name, address) VALUES (?, ?)", (name, address))
        print(f"Subscriber {name} and {address} added successfully.")
    except sqlite3.IntegrityError:
        print(f"Subscriber {name} is already in database.")


def add_subscription(cursor, subscriber, magazine):
    expiration_date = (datetime.now() + timedelta(days=30)).isoformat()
    cursor.execute(
        "SELECT * FROM Subscribers WHERE subscriber_name = ?", (subscriber,))
    results = cursor.fetchall()
    if len(results) > 0:
        subscriber_id = results[0][0]
    else:
        print(f"There is no subscriber named {subscriber}.")
        return
    cursor.execute(
        "SELECT * FROM Magazines WHERE magazine_name = ?", (magazine,))
    results = cursor.fetchall()
    if len(results) > 0:
        magazine_id = results[0][0]
    else:
        print(f"There is no magazine named {magazine}.")
        return
    try:
        cursor.execute("INSERT INTO Subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)",
                       (subscriber_id, magazine_id, expiration_date))
        print(
            f"Subscription for {subscriber} to {magazine} added successfully.")
    except sqlite3.IntegrityError:
        print(
            f"Subscription for {subscriber} to {magazine} is already in database.")


try:
    with sqlite3.connect('../db/magazines.db') as conn:
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = 1")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Publishers (
            publisher_id INTEGER PRIMARY KEY,
            publisher_name TEXT NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Magazines (
            magazine_id INTEGER PRIMARY KEY,
            magazine_name TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subscribers (
            subscriber_id INTEGER PRIMARY KEY,
            subscriber_name TEXT NOT NULL,
            address TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES Subscribers(subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES Magazines(magazine_id)
            UNIQUE (subscriber_id, magazine_id)
        )
        """)
        print('Tables created successfully.')

        add_publisher(cursor, 'Elena')
        add_publisher(cursor, 'Bob')
        add_publisher(cursor, 'Daniel')
        add_publisher(cursor, 'Mike')

        add_magazines(cursor, 'Time', 'Elena')
        add_magazines(cursor, 'National Geographic', 'Bob')
        add_magazines(cursor, 'Vogue', 'Daniel')
        add_magazines(cursor, 'Forbes', 'Elena')
        add_magazines(cursor, 'Time', 'Mike')

        add_subscriber(cursor, 'Elena', '123 Main St')
        add_subscriber(cursor, 'Elena', '456 Elm St')
        add_subscriber(cursor, 'Bob', '456 Elm St')
        add_subscriber(cursor, 'Daniel', '789 Oak St')
        add_subscriber(cursor, 'Mike', '123 Street St')

        add_subscription(cursor, 'Elena', 'Time')
        add_subscription(cursor, 'Bob', 'National Geographic')
        add_subscription(cursor, 'Daniel', 'Vogue')
        add_subscription(cursor, 'Elena', 'Forbes')
        add_subscription(cursor, 'Mike', 'Time')

        conn.commit()
        print("Sample data inserted successfully.")

        # Task 4
        cursor.execute("SELECT * FROM Subscribers")
        results = cursor.fetchall()
        for row in results:
            print(row)
        cursor.execute("SELECT * FROM Magazines ORDER BY magazine_name")
        results = cursor.fetchall()
        for row in results:
            print(row)
        cursor.execute("SELECT publisher_name, magazine_name FROM Publishers AS p JOIN Magazines AS m ON p.publisher_id = m.publisher_id")
        results = cursor.fetchall()
        for row in results:
            print(row)
except sqlite3.Error as e:
    print(f"SQL Error: {e}")
