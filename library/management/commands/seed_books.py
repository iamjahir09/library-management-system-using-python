
from django.core.management.base import BaseCommand
from library.models import Book


class Command(BaseCommand):
    help = "Create sample books for the library catalogue"

    def handle(self, *args, **options):
        books = [
            ("The Alchemist", "Paulo Coelho", "9780061122415", "Fiction", "A journey about dreams, courage, and discovering one's purpose.", 5),
            ("Atomic Habits", "James Clear", "9780735211292", "Self Development", "A practical guide to building good habits and breaking bad ones.", 4),
            ("Clean Code", "Robert C. Martin", "9780132350884", "Programming", "Principles and practices for writing readable, maintainable software.", 3),
            ("Python Crash Course", "Eric Matthes", "9781718502703", "Programming", "A hands-on introduction to Python programming.", 4),
            ("Deep Learning", "Ian Goodfellow, Yoshua Bengio, Aaron Courville", "9780262035613", "Artificial Intelligence", "Foundational concepts and methods in deep learning.", 2),
            ("Introduction to Algorithms", "Thomas H. Cormen et al.", "9780262046305", "Computer Science", "A comprehensive reference to algorithms and data structures.", 3),
            ("Database System Concepts", "Abraham Silberschatz et al.", "9780078022159", "Computer Science", "Core concepts of database design, SQL, and transaction processing.", 3),
            ("Operating System Concepts", "Abraham Silberschatz et al.", "9781119800361", "Computer Science", "Principles of operating systems and resource management.", 2),
            ("Computer Networking: A Top-Down Approach", "James Kurose and Keith Ross", "9780136681557", "Computer Science", "Networking concepts explained from the application layer downward.", 2),
            ("The Pragmatic Programmer", "David Thomas and Andrew Hunt", "9780135957059", "Programming", "Practical advice for professional software development.", 3),
            ("Think and Grow Rich", "Napoleon Hill", "9781585424337", "Self Development", "Classic ideas about goal setting and personal achievement.", 3),
            ("Wings of Fire", "A. P. J. Abdul Kalam and Arun Tiwari", "9788173711466", "Biography", "The autobiography of Indian aerospace scientist A. P. J. Abdul Kalam.", 4),
            ("Rich Dad Poor Dad", "Robert T. Kiyosaki", "9781612680194", "Finance", "Personal finance lessons about assets, liabilities, and financial literacy.", 3),
            ("Sapiens", "Yuval Noah Harari", "9780062316097", "History", "An overview of the history and development of humankind.", 2),
            ("The Psychology of Money", "Morgan Housel", "9780857197689", "Finance", "Stories about how people think about money and financial decisions.", 3),
            ("Artificial Intelligence: A Modern Approach", "Stuart Russell and Peter Norvig", "9780134610993", "Artificial Intelligence", "A broad introduction to artificial intelligence concepts and methods.", 2),
            ("Head First Java", "Kathy Sierra and Bert Bates", "9780596009205", "Programming", "A visual and example-driven introduction to Java.", 3),
            ("Designing Data-Intensive Applications", "Martin Kleppmann", "9781449373320", "Software Engineering", "Architectural principles for reliable, scalable data systems.", 2),
            ("The Hobbit", "J. R. R. Tolkien", "9780547928227", "Fiction", "A fantasy adventure about a hobbit's unexpected journey.", 3),
            ("To Kill a Mockingbird", "Harper Lee", "9780061120084", "Fiction", "A novel exploring justice, morality, and community.", 2),

            ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "Fiction", "A classic novel exploring ambition, wealth, and the American Dream.", 4),
            ("1984", "George Orwell", "9780451524935", "Fiction", "A dystopian novel about surveillance, power, and freedom.", 3),
            ("Pride and Prejudice", "Jane Austen", "9780141439518", "Fiction", "A classic novel about relationships, social expectations, and personal growth.", 3),
            ("Harry Potter and the Philosopher's Stone", "J. K. Rowling", "9780747532699", "Fantasy", "A young wizard discovers a magical world and his place within it.", 5),
            ("The Lord of the Rings", "J. R. R. Tolkien", "9780618640157", "Fantasy", "An epic fantasy journey to destroy a powerful ring.", 3),
            ("The Lean Startup", "Eric Ries", "9780307887894", "Business", "A practical approach to building and testing new business ideas.", 3),
            ("Zero to One", "Peter Thiel", "9780804139298", "Business", "Ideas about innovation, startups, and building new technologies.", 3),
            ("The Intelligent Investor", "Benjamin Graham", "9780060555665", "Finance", "Principles of value investing and long-term financial decision-making.", 2),
            ("The Power of Habit", "Charles Duhigg", "9780812981605", "Self Development", "An exploration of how habits work and how they can be changed.", 4),
            ("Can't Hurt Me", "David Goggins", "9781544512280", "Biography", "A memoir about discipline, resilience, and overcoming personal challenges.", 3),
            ("Ikigai", "Hector Garcia and Francesc Miralles", "9780143130727", "Self Development", "An exploration of purpose, daily habits, and a meaningful life.", 4),
            ("The Theory of Everything", "Stephen Hawking", "9780553380163", "Science", "An introduction to major ideas about the universe and cosmology.", 2),
            ("A Brief History of Time", "Stephen Hawking", "9780553380163", "Science", "An introduction to space, time, black holes, and cosmology.", 3),
            ("The Selfish Gene", "Richard Dawkins", "9780198788607", "Science", "An introduction to evolution and gene-centred explanations of natural selection.", 2),
            ("Hands-On Machine Learning", "Aurélien Géron", "9781098125974", "Artificial Intelligence", "Practical techniques for machine learning using modern Python tools.", 3),
            ("Machine Learning Yearning", "Andrew Ng", "9781999579500", "Artificial Intelligence", "Practical guidance on structuring and improving machine learning projects.", 2),
            ("Fluent Python", "Luciano Ramalho", "9781492056355", "Programming", "Advanced Python techniques and effective use of the language.", 3),
            ("Effective Java", "Joshua Bloch", "9780134685991", "Programming", "Best practices for writing robust and maintainable Java applications.", 3),
            ("Cracking the Coding Interview", "Gayle Laakmann McDowell", "9780984782857", "Computer Science", "Programming interview preparation with algorithms and data structures.", 4),
            ("System Design Interview", "Alex Xu", "9781736049112", "Software Engineering", "An introduction to designing scalable software systems.", 3),
            ("The Design of Everyday Things", "Don Norman", "9780465050659", "Design", "Principles of usability and human-centred product design.", 2),
        ]

        created = 0

        for title, author, isbn, category, description, copies in books:
            _, was_created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "title": title,
                    "author": author,
                    "category": category,
                    "description": description,
                    "total_copies": copies,
                    "available_copies": copies,
                },
            )
            created += int(was_created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Sample catalogue ready. {created} books added; {len(books)} books checked."
            )
        )
