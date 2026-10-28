import mysql.connector
from datetime import date

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="library"
)

cur = con.cursor()

while True:
    print("\n--- Library Circulation System ---")
    print("1. Add Book")
    print("2. Register Borrower")
    print("3. Issue Book")
    print("4. Return Book")
    print("5. View Books")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        book_id = int(input("Book ID: "))
        title = input("Book title: ")
        author = input("Author: ")

        cur.execute(
            "INSERT INTO books VALUES (%s, %s, %s, 1)",
            (book_id, title, author)
        )
        con.commit()
        print("Book added successfully.")

    elif choice == "2":
        borrower_id = int(input("Borrower ID: "))
        name = input("Borrower name: ")

        cur.execute(
            "INSERT INTO borrowers VALUES (%s, %s)",
            (borrower_id, name)
        )
        con.commit()
        print("Borrower registered successfully.")

    elif choice == "3":
        book_id = int(input("Book ID: "))
        borrower_id = int(input("Borrower ID: "))

        cur.execute(
            "SELECT available FROM books WHERE book_id = %s",
            (book_id,)
        )
        book = cur.fetchone()

        cur.execute(
            "SELECT borrower_id FROM borrowers WHERE borrower_id = %s",
            (borrower_id,)
        )
        borrower = cur.fetchone()

        if book and book[0] == 1 and borrower:
            cur.execute(
                "INSERT INTO issues (book_id, borrower_id, issue_date) "
                "VALUES (%s, %s, %s)",
                (book_id, borrower_id, date.today())
            )
            cur.execute(
                "UPDATE books SET available = 0 WHERE book_id = %s",
                (book_id,)
            )
            con.commit()
            print("Book issued successfully.")
        else:
            print("Book unavailable or borrower not found.")

    elif choice == "4":
        issue_id = int(input("Issue ID: "))

        cur.execute(
            "SELECT book_id, issue_date FROM issues "
            "WHERE issue_id = %s AND return_date IS NULL",
            (issue_id,)
        )
        record = cur.fetchone()

        if record:
            book_id, issue_date = record
            days = (date.today() - issue_date).days
            fine = max(0, days - 14) * 5

            cur.execute(
                "UPDATE issues SET return_date = %s WHERE issue_id = %s",
                (date.today(), issue_id)
            )
            cur.execute(
                "UPDATE books SET available = 1 WHERE book_id = %s",
                (book_id,)
            )
            con.commit()

            print("Book returned successfully.")
            print("Overdue fine: Rs.", fine)
        else:
            print("Invalid issue ID or book already returned.")

    elif choice == "5":
        cur.execute("SELECT * FROM books")
        for book in cur.fetchall():
            print(book)

    elif choice == "6":
        break

    else:
        print("Invalid choice.")

cur.close()
con.close()