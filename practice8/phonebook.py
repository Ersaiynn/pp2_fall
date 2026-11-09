from connect import connect


# Task 1: Search contacts
def search_contacts():
    pattern = input("Enter name or phone: ")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM search_contacts(%s)",
                (pattern,)
            )
            rows = cur.fetchall()

            for row in rows:
                print(row)


# Task 2: Insert or update contact
def upsert_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL upsert_contact(%s, %s)",
                (name, phone)
            )

    print("Contact inserted or updated!")


# Task 3: Insert many contacts
def insert_many_contacts():
    names = []
    phones = []

    n = int(input("How many contacts? "))

    for i in range(n):
        name = input("Enter name: ")
        phone = input("Enter phone: ")

        names.append(name)
        phones.append(phone)

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL insert_many_contacts(%s::text[], %s::text[], %s::text[])",
                (names, phones, [])
            )
            invalid = cur.fetchone()[0]

    print("Invalid contacts:", invalid)


# Task 4: Pagination
def get_contacts_page():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s)",
                (limit, offset)
            )
            rows = cur.fetchall()

            for row in rows:
                print(row)


# Task 5: Delete contact
def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")

    choice = input("Choose: ")

    if choice == "1":
        delete_type = "name"
    elif choice == "2":
        delete_type = "phone"
    else:
        print("Invalid choice")
        return

    value = input("Enter value: ")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL delete_contact(%s, %s)",
                (value, delete_type)
            )

    print("Delete completed!")


# Main menu
def main():
    while True:
        print("\nPHONEBOOK")
        print("1. Search contacts")
        print("2. Insert or update contact")
        print("3. Insert many contacts")
        print("4. Pagination")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        try:
            if choice == "1":
                search_contacts()
            elif choice == "2":
                upsert_contact()
            elif choice == "3":
                insert_many_contacts()
            elif choice == "4":
                get_contacts_page()
            elif choice == "5":
                delete_contact()
            elif choice == "0":
                break
            else:
                print("Invalid choice")
        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()