import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="library"
)

cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    available INT DEFAULT 1
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS borrowers (
    borrower_id INT PRIMARY KEY,
    name VARCHAR(100)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS issues (
    issue_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT,
    borrower_id INT,
    issue_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (borrower_id) REFERENCES borrowers(borrower_id)
)
""")

con.commit()
