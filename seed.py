from app import app
from models import db, Author, Book, Bookstore, BookstoreBook
from datetime import date

def seed_data():
    # Clear existing data
    db.session.query(BookstoreBook).delete()
    db.session.query(Book).delete()
    db.session.query(Author).delete()
    db.session.query(Bookstore).delete()

    # Create Authors
    authors = [
        Author(
            first_name="Alice",
            second_name="Wonder",
            email="alice.wonder@example.com",
            nationality="American",
            bio="Writes captivating fantasy novels."
        ),
        Author(
            first_name="Bob",
            second_name="Rivers",
            email="bob.rivers@example.com",
            nationality="Canadian",
            bio="Famous for his thrilling mystery books."
        ),
        Author(
            first_name="Clara",
            second_name="Smith",
            email="clara.smith@example.com",
            nationality="British",
            bio="Known for her inspiring dramas."
        ),
        Author(
            first_name="David",
            second_name="Green",
            email="david.green@example.com",
            nationality="Australian",
            bio="Writes action-packed sci-fi stories."
        ),
        Author(
            first_name="Emma",
            second_name="Stone",
            email="emma.stone@example.com",
            nationality="Irish",
            bio="Creates heartwarming romantic tales."
        ),
        Author(
            first_name="Felix",
            second_name="Woods",
            email="felix.woods@example.com",
            nationality="German",
            bio="Specializes in non-fiction and historical works."
        ),
        Author(
            first_name="Grace",
            second_name="Blue",
            email="grace.blue@example.com",
            nationality="French",
            bio="Writes intriguing philosophical essays."
        )
    ]
    db.session.add_all(authors)

    # Create Books
    books = [
        Book(title="Whisper of the Wind", genre="Fantasy", publication_date=date(2020, 5, 10), description="An epic journey of discovery.", author=authors[1],book_img="public/wind.jpg"),
        Book(title="Shadows in the Night", genre="Mystery", publication_date=date(2018, 11, 3), description="A detective uncovers hidden secrets.", author=authors[0],book_img="public/nightsky.jpg"),
        Book(title="Beneath the Sky", genre="Drama", publication_date=date(2015, 3, 14), description="A family torn apart by tragedy.", author=authors[2],book_img="public/beneath.jpg"),
        Book(title="Into the Cosmos", genre="Sci-Fi", publication_date=date(2022, 6, 30), description="An astronaut ventures into the unknown.", author=authors[3],book_img="public/cosmos.jpg"),
        Book(title="Hearts Afire", genre="Romance", publication_date=date(2021, 2, 14), description="A tale of love and destiny.", author=authors[4],book_img="public/hearts.jpg"),
        Book(title="Echoes of the Past", genre="Non-Fiction", publication_date=date(2019, 8, 25), description="A historical recount of pivotal events.", author=authors[5],book_img="public/echoes.jpg"),
        Book(title="Reflections of the Mind", genre="Non-Fiction", publication_date=date(2023, 1, 5), description="An exploration of human thought.", author=authors[6],book_img="public/mind.jpg"),
    ]
    db.session.add_all(books)

    # Create Bookstores
    bookstores = [
        Bookstore(name="City Lights", location="New York, USA", established_date=date(1990, 1, 1)),
        Bookstore(name="Mystery Corner", location="Toronto, Canada", established_date=date(2005, 6, 15)),
        Bookstore(name="Dreamscape Books", location="London, UK", established_date=date(1980, 3, 30)),
        Bookstore(name="Galaxy Reads", location="Sydney, Australia", established_date=date(2010, 12, 25))
    ]
    db.session.add_all(bookstores)
    
    # creating bookstorebooks 
    associations = [
                    BookstoreBook(book=books[0], bookstore=bookstores[0], stock=8, price=12.99),
                    BookstoreBook(book=books[1], bookstore=bookstores[1], stock=5, price=10.99),
                    # Add more associations
                ]
                
    db.session.add_all(associations)
               
    
    
    
    # Commit the session
    db.session.commit()
    print("Database seeded successfully!")


# Add the application context here
with app.app_context():
    seed_data()
