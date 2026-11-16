import csv
import json
from datetime import date
from pathlib import Path
from connect import connect

BASE = Path(__file__).resolve().parent


def setup():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute((BASE / "schema.sql").read_text(encoding="utf-8"))
            cur.execute((BASE / "procedures.sql").read_text(encoding="utf-8"))
    print("TSIS1 database setup complete")


def show(rows):
    if not rows:
        print("No contacts found")
    for row in rows:
        print(row)


def filter_by_group():
    group = input("Group (Family/Work/Friend/Other): ").strip()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.first_name, c.surname, c.email, g.name
                FROM contacts c JOIN groups g ON c.group_id = g.id
                WHERE g.name ILIKE %s ORDER BY c.first_name, c.id
            """, (group,))
            show(cur.fetchall())


def search_by_email():
    email = input("Email contains: ").strip()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, first_name, surname, email FROM contacts
                WHERE email ILIKE %s ORDER BY id
            """, (f"%{email}%",))
            show(cur.fetchall())


def sort_contacts():
    print("1. Name   2. Birthday   3. Date added")
    choice = input("Choose: ").strip()
    columns = {
        "1": "first_name, id",
        "2": "birthday NULLS LAST, id",
        "3": "date_added DESC, id DESC"
    }
    if choice not in columns:
        print("Wrong choice")
        return
    sql = "SELECT id, first_name, surname, email, birthday, date_added FROM contacts ORDER BY " + columns[choice]
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            show(cur.fetchall())


def navigate_pages():
    size = 5
    page = 0
    while True:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (size, page * size))
                rows = cur.fetchall()
        print(f"\nPage {page + 1}")
        show(rows)
        command = input("next / prev / quit: ").strip().lower()
        if command == "quit":
            break
        if command == "next":
            if len(rows) == size:
                page += 1
            else:
                print("Last page")
        elif command == "prev":
            page = max(0, page - 1)
        else:
            print("Unknown command")


def search_all():
    query = input("Search name, surname, email or phone: ").strip()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            show(cur.fetchall())


def add_phone():
    name = input("Existing contact name: ").strip()
    phone = input("New phone: ").strip()
    kind = input("Type (home/work/mobile): ").strip()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, kind))
    print("Phone added")


def move_to_group():
    name = input("Existing contact name: ").strip()
    group = input("New group: ").strip()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (name, group))
    print("Group updated")


def export_json():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.first_name, c.surname, c.email, c.birthday, g.name
                FROM contacts c LEFT JOIN groups g ON c.group_id = g.id ORDER BY c.id
            """)
            contacts = cur.fetchall()
            output = []
            for ident, name, surname, email, birthday, group in contacts:
                cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id", (ident,))
                phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]
                output.append({"name": name, "surname": surname, "email": email,
                               "birthday": birthday.isoformat() if birthday else None,
                               "group": group, "phones": phones})
    path = BASE / "contacts.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported {len(output)} contacts to {path.name}")


def save_contact(item, overwrite=False):
    name = (item.get("name") or "").strip()
    if not name:
        raise ValueError("Name is empty")
    phones = item.get("phones") or []
    birthday = item.get("birthday") or None
    if birthday:
        birthday = date.fromisoformat(birthday)
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM contacts WHERE first_name = %s ORDER BY id LIMIT 1", (name,))
            row = cur.fetchone()
            first_phone = phones[0]["phone"] if phones else None
            if row:
                if not overwrite:
                    return
                ident = row[0]
                cur.execute("""
                    UPDATE contacts SET surname=%s, email=%s, birthday=%s, phone=%s
                    WHERE id=%s
                """, (item.get("surname") or "", item.get("email"), birthday, first_phone, ident))
                cur.execute("DELETE FROM phones WHERE contact_id = %s", (ident,))
            else:
                cur.execute("""
                    INSERT INTO contacts (first_name, surname, email, birthday, phone)
                    VALUES (%s,%s,%s,%s,%s) RETURNING id
                """, (name, item.get("surname") or "", item.get("email"), birthday, first_phone))
                ident = cur.fetchone()[0]
            group = (item.get("group") or "").strip()
            if group:
                cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT(name) DO NOTHING", (group,))
                cur.execute("UPDATE contacts SET group_id=(SELECT id FROM groups WHERE name=%s) WHERE id=%s", (group, ident))
            else:
                cur.execute("UPDATE contacts SET group_id=NULL WHERE id=%s", (ident,))
            for entry in phones:
                phone = entry["phone"]
                kind = entry.get("type", "mobile")
                if kind not in ("home", "work", "mobile"):
                    raise ValueError("Wrong phone type")
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)", (ident, phone, kind))


def import_json():
    path = BASE / input("JSON filename (contacts.json): ").strip()
    items = json.loads(path.read_text(encoding="utf-8"))
    for item in items:
        name = (item.get("name") or "").strip()
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM contacts WHERE first_name=%s LIMIT 1", (name,))
                exists = cur.fetchone() is not None
        overwrite = False
        if exists:
            choice = input(f"{name} exists: skip or overwrite? ").strip().lower()
            if choice != "overwrite":
                print("Skipped", name)
                continue
            overwrite = True
        try:
            save_contact(item, overwrite)
            print("Imported", name)
        except Exception as error:
            print("Could not import", name, ":", error)


def import_csv():
    path = BASE / input("CSV filename (contacts.csv): ").strip()
    with path.open(newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))
    for row in rows:
        item = {"name": row["first_name"], "surname": row.get("surname") or "",
                "email": row.get("email") or None, "birthday": row.get("birthday") or None,
                "group": row.get("group") or "",
                "phones": [{"phone": row["phone"], "type": row.get("type") or "mobile"}]}
        try:
            with connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM contacts WHERE first_name = %s LIMIT 1", (item["name"],))
                    exists = cur.fetchone() is not None
            # Extend old CSV import: new contacts are added; existing ones are skipped.
            if exists:
                print("Skipped existing", item["name"])
            else:
                save_contact(item)
                print("Imported", item["name"])
        except Exception as error:
            print("Could not import", item["name"], ":", error)


def main():
    actions = {
        "1": filter_by_group, "2": search_by_email, "3": sort_contacts,
        "4": navigate_pages, "5": export_json, "6": import_json,
        "7": import_csv, "8": add_phone, "9": move_to_group, "10": search_all,
        "11": setup
    }
    while True:
        print("\n=== TSIS1 PHONEBOOK ===")
        print("1 Group filter | 2 Email search | 3 Sort | 4 Pages")
        print("5 Export JSON | 6 Import JSON | 7 Import CSV")
        print("8 Add phone | 9 Move group | 10 Search all | 11 Setup DB | 0 Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        try:
            if choice in actions:
                actions[choice]()
            else:
                print("Wrong choice")
        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
