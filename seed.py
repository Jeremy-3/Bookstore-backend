from app import app
from models import db, Author, Book, Bookstore, BookstoreBook,User
from datetime import date
from werkzeug.security import generate_password_hash


def seed_data():
    # Clear existing data
    db.session.query(BookstoreBook).delete()
    db.session.query(Book).delete()
    db.session.query(Author).delete()
    db.session.query(Bookstore).delete()
    db.session.query(User).delete()
    

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
        Book(title="Whisper of the Wind", genre="Fantasy", publication_date=date(2020, 5, 10), description="An epic journey of discovery.", author=authors[1],book_img="https://images.unsplash.com/photo-1516410529446-2c777cb7366d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGhvcnJvcnxlbnwwfHwwfHx8MA%3D%3D"),
        Book(title="Shadows in the Night", genre="Mystery", publication_date=date(2018, 11, 3), description="A detective uncovers hidden secrets.", author=authors[5],book_img="https://images.unsplash.com/photo-1586165877141-3dbcfc059283?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmlnaHQlMjBjaXR5fGVufDB8fDB8fHww"),
        Book(title="Beneath the Sky", genre="Drama", publication_date=date(2015, 3, 14), description="A family torn apart by tragedy.", author=authors[2],book_img="https://images.unsplash.com/photo-1526547462705-121430d02c2c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGhvcnJvcnxlbnwwfHwwfHx8MA%3D%3D"),
        Book(title="Into the Cosmos", genre="Sci-Fi", publication_date=date(2022, 6, 30), description="An astronaut ventures into the unknown.", author=authors[3],book_img="https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Y29zbW9zfGVufDB8fDB8fHww"),
        Book(title="Hearts Afire", genre="Romance", publication_date=date(2021, 2, 14), description="A tale of love and destiny.", author=authors[4],book_img="https://plus.unsplash.com/premium_photo-1664529914557-ee01920185e2?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8cm9tYW5jZXxlbnwwfHwwfHx8MA%3D%3D"),
        Book(title="Echoes of the Past", genre="Non-Fiction", publication_date=date(2019, 8, 25), description="A historical recount of pivotal events.", author=authors[5],book_img="https://images.unsplash.com/photo-1743348230487-d548a13228f6?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTAzfHxoaXN0b3JpY2FsfGVufDB8fDB8fHww"),
        Book(title="Reflections of the Mind", genre="Non-Fiction", publication_date=date(2023, 1, 5), description="An exploration of human thought.", author=authors[6],book_img="https://images.unsplash.com/photo-1461800919507-79b16743b257?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8aHVtYW58ZW58MHx8MHx8fDA%3D"),
        Book(title="The Quantum Enigma", genre="Sci-Fi", publication_date=date(2022, 7, 15), description="A deep dive into the mysteries of quantum mechanics.",author=authors[1],book_img="https://plus.unsplash.com/premium_photo-1681426558755-71090cebadff?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8cGh5c2ljc3xlbnwwfHwwfHx8MA%3D%3D"),
        Book(title="Lost,Found then Gone", genre="Romance", publication_date=date(2021, 3, 22), description="A haunting tale of love and loss set in a small coastal town.",author=authors[1],book_img="https://plus.unsplash.com/premium_photo-1670187526577-2c44454ee900?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHBhc3Npb258ZW58MHx8MHx8fDA%3D"),
        Book(title="The Art of Stillness", genre="Non-Fiction", publication_date=date(2020, 11, 10), description="Finding peace and purpose in a chaotic world.",author=authors[4],book_img="https://plus.unsplash.com/premium_photo-1670594369789-585a4fa262f8?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjF8fHN0aWxsJTIwd2F0ZXJzfGVufDB8fDB8fHww"),
        Book(title="Chronicles Of Ghee!", genre="Fiction", publication_date=date(2023, 4, 18), description="A journey through time and space in a distant future.",author=authors[2],book_img="https://images.unsplash.com/photo-1568952433726-3896e3881c65?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8ZnV0dXJlfGVufDB8fDB8fHww"),
        Book(title="Chronicles of Acadia", genre="Fantasy", publication_date=date(2019, 9, 30), description="A magical adventure in an enchanted woodland realm.",author=authors[1],book_img="https://images.unsplash.com/photo-1679943052723-59c756ff2fb0?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bWFnaWMlMjBmb3Jlc3QlMjBhbmltYXRpb258ZW58MHx8MHx8fDA%3D"),
        Book(title="The Silent Witness", genre="Drama", publication_date=date(2022, 2, 14), description="A gripping mystery unraveling hidden secrets and lies.",author=authors[6],book_img="https://plus.unsplash.com/premium_photo-1663100179015-f0ef9e4a8d51?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHNlY3JldHxlbnwwfHwwfHx8MA%3D%3D"),
        Book(title="Mindful Living", genre="Non-Fiction", publication_date=date(2021, 6, 8), description="Practical strategies for cultivating mindfulness in everyday life.",author=authors[6],book_img="https://images.unsplash.com/photo-1674969856334-3a2bf4a60cfb?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjZ8fG1pbmRmdWwlMjBsaXZpbmd8ZW58MHx8MHx8fDA%3D"),
        Book(title="The Forgotten Empire", genre="Action", publication_date=date(2020, 12, 25), description="A sweeping saga of power, betrayal, and redemption in ancient times.",author=authors[4],book_img="https://plus.unsplash.com/premium_photo-1690914948652-360b9b107397?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8Y2FzdGxlc3xlbnwwfHwwfHx8MA%3D%3D"),
        Book(title="Beyond the Horizon", genre="Mystery", publication_date=date(2023, 8, 2), description="An epic voyage across uncharted lands and seas.",author=authors[3],book_img="https://plus.unsplash.com/premium_photo-1664533227454-a228e8766994?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fGhvcml6b25zfGVufDB8fDB8fHww"),
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
               
    # User.query.filter_by(is_banned=None).update({User.is_banned: False})
    # db.session.commit()
    
    
    # Commit the session
    db.session.commit()
    print("Database seeded successfully!")

    user =[
        User(username="admin", email="admin@example.com", role="admin",password_hash=generate_password_hash('admin123')),
        User(username="author1", email="author1@example.com", role="user",password_hash=generate_password_hash('author123')),
        User(username="user1", email="user1@example.com", role="user",password_hash=generate_password_hash('user123')),
        User(username="walice", email="walice@gmail.com", role="user", password_hash=generate_password_hash('walice123'))
    ]


# Add the application context here
with app.app_context():
    seed_data()
