
import csv
import psycopg2
from config import load_config
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = psycopg2.connect(**load_config())
    try:
        with conn:
            yield conn
    finally:
        conn.close()


# 1. Create table
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) UNIQUE NOT NULL
    )
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

    print("Contacts table is ready!")


# 2. Insert contacts from CSV
def insert_from_csv():
    filename = input("Enter CSV filename: ").strip()

    try:
        with open(filename, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            contacts = []

            for row in reader:
                if len(row) != 2:
                    print("Skipping invalid row:", row)
                    continue

                name, phone = row[0].strip(), row[1].strip()

                if name and phone:
                    contacts.append((name, phone))

        sql = """
        INSERT INTO contacts (first_name, phone)
        VALUES (%s, %s)
        ON CONFLICT (phone) DO NOTHING
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(sql, contacts)

        print("CSV import completed!")

    except FileNotFoundError:
        print("CSV file not found.")


# 3. Insert contact from console
def insert_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    if not name or not phone:
        print("Name and phone cannot be empty.")
        return

    sql = """
    INSERT INTO contacts (first_name, phone)
    VALUES (%s, %s)
    ON CONFLICT (phone) DO NOTHING
    RETURNING id
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name, phone))
            result = cur.fetchone()

            if result:
                print("Contact added! ID:", result[0])
            else:
                print("This phone number already exists.")


# 4. Update name or phone
def update_contact():
    old_name = input("Enter current name: ").strip()

    print("1. Update name")
    print("2. Update phone")
    choice = input("Choose: ")

    if choice == "1":
        new_name = input("Enter new name: ").strip()
        column = "first_name"
        value = new_name

    elif choice == "2":
        new_phone = input("Enter new phone: ").strip()
        column = "phone"
        value = new_phone

    else:
        print("Invalid choice.")
        return

    if not value:
        print("Value cannot be empty.")
        return

    sql = f"""
    UPDATE contacts
    SET {column} = %s
    WHERE first_name = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (value, old_name))
            print("Updated rows:", cur.rowcount)


# 5. Query contacts
def query_contacts():
    print("1. Show all")
    print("2. Search by name")
    print("3. Search by phone prefix")

    choice = input("Choose: ")

    if choice == "1":
        sql = "SELECT * FROM contacts ORDER BY id"
        params = ()

    elif choice == "2":
        name = input("Enter name: ")
        sql = """
        SELECT * FROM contacts
        WHERE first_name ILIKE %s
        ORDER BY id
        """
        params = (f"%{name}%",)

    elif choice == "3":
        prefix = input("Enter phone prefix: ")
        sql = """
        SELECT * FROM contacts
        WHERE phone LIKE %s
        ORDER BY id
        """
        params = (f"{prefix}%",)

    else:
        print("Invalid choice.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

            for row in rows:
                print(row)

            print("Found:", len(rows))


# 6. Delete by name or phone
def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Enter name: ")
        sql = "DELETE FROM contacts WHERE first_name = %s"
        value = name

    elif choice == "2":
        phone = input("Enter phone: ")
        sql = "DELETE FROM contacts WHERE phone = %s"
        value = phone

    else:
        print("Invalid choice.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (value,))
            print("Deleted rows:", cur.rowcount)


# Main menu
def main():
    create_table()

    while True:
        print("\n===== PHONEBOOK =====")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Choose an option: ")

        try:
            if choice == "1":
                insert_from_csv()
            elif choice == "2":
                insert_contact()
            elif choice == "3":
                update_contact()
            elif choice == "4":
                query_contacts()
            elif choice == "5":
                delete_contact()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")

        except psycopg2.Error as error:
            print("Database error:", error)


if __name__ == "__main__":
    main()
