from database import get_connection
import random

titles = ["Python", "Java", "FastAPI", "AI", "Data", "Linux", "Docker", "React", "SQL", "Code"]
authors = ["Author A", "Author B", "Author C", "Author D"]
publishers = ["Publisher X", "Publisher Y", "Publisher Z"]

con = get_connection()
cur = con.cursor()

for i in range(50000):
    title = f"{random.choice(titles)} Book {i}"
    author = random.choice(authors)
    publisher = random.choice(publishers)
    image_url = "https://example.com/image.jpg"
    cur.execute("""
        INSERT INTO books (title, author, publisher, image_url)
        VALUES (%s, %s, %s, %s);
    """, (title, author, publisher, image_url))

print("books added")

con.commit()
cur.close()
con.close()