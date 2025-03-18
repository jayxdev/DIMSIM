from typing import Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Custom Exceptions
class BookAlreadyExistsError(Exception):
    """
    Exception raised when attempting to add a book that already exists in the library.
    """
    def __init__(self, message: Optional[str] = None):
        default_message = "The book already exists in the library."
        super().__init__(message or default_message)


class BookNotFoundError(Exception):
    """
    Exception raised when a book is not found in the library.
    """
    def __init__(self, message: Optional[str] = None):
        default_message = "The requested book was not found in the library."
        super().__init__(message or default_message)


class BookAlreadyCheckedOutError(Exception):
    """
    Exception raised when attempting to check out a book that is already checked out.
    """
    def __init__(self, message: Optional[str] = None):
        default_message = "The book is already checked out."
        super().__init__(message or default_message)


class BookNotCheckedOutError(Exception):
    """
    Exception raised when attempting to return a book that is not checked out.
    """
    def __init__(self, message: Optional[str] = None):
        default_message = "The book was not checked out."
        super().__init__(message or default_message)


# Book Class
class Book:
    """
    Represents a book in the library.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        is_checked_out (bool): Availability status of the book.
    """

    def __init__(self, title: str, author: str):
        """
        Initializes a new Book instance.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
        """
        self.title = title
        self.author = author
        self.is_checked_out = False

    def checkout(self) -> None:
        """
        Marks the book as checked out.

        Raises:
            BookAlreadyCheckedOutError: If the book is already checked out.
        """
        if self.is_checked_out:
            logger.error(f"Attempt to checkout already checked out book: '{self.title}'.")
            raise BookAlreadyCheckedOutError(f"'{self.title}' is already checked out.")
        self.is_checked_out = True
        logger.info(f"Book checked out: '{self.title}'.")

    def return_book(self) -> None:
        """
        Marks the book as returned.

        Raises:
            BookNotCheckedOutError: If the book was not checked out.
        """
        if not self.is_checked_out:
            logger.error(f"Attempt to return a book that was not checked out: '{self.title}'.")
            raise BookNotCheckedOutError(f"'{self.title}' was not checked out.")
        self.is_checked_out = False
        logger.info(f"Book returned: '{self.title}'.")


# Library Class
class Library:
    """
    Manages a collection of books in the library.

    Attributes:
        books (Dict[str, Book]): A dictionary mapping book titles to Book instances.
    """

    def __init__(self):
        """Initializes a new Library instance with an empty collection of books."""
        self.books: Dict[str, Book] = {}
        logger.info("Initialized new Library.")

    def add_book(self, title: str, author: str) -> None:
        """
        Adds a new book to the library.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.

        Raises:
            BookAlreadyExistsError: If the book already exists in the library.
        """
        if title in self.books:
            logger.error(f"Attempt to add duplicate book: '{title}'.")
            raise BookAlreadyExistsError(f"The book '{title}' already exists in the library.")
        self.books[title] = Book(title, author)
        logger.info(f"Added book: '{title}' by {author}.")

    def checkout_book(self, title: str) -> None:
        """
        Checks out a book from the library.

        Args:
            title (str): The title of the book to check out.

        Raises:
            BookNotFoundError: If the book is not found in the library.
            BookAlreadyCheckedOutError: If the book is already checked out.
        """
        book = self._get_book(title)
        book.checkout()

    def return_book(self, title: str) -> None:
        """
        Returns a book to the library.

        Args:
            title (str): The title of the book to return.

        Raises:
            BookNotFoundError: If the book is not found in the library.
            BookNotCheckedOutError: If the book was not checked out.
        """
        book = self._get_book(title)
        book.return_book()

    def is_book_available(self, title: str) -> bool:
        """
        Checks if a book is available for checkout.

        Args:
            title (str): The title of the book.

        Returns:
            bool: True if the book is available, False otherwise.

        Raises:
            BookNotFoundError: If the book is not found in the library.
        """
        book = self._get_book(title)
        availability = not book.is_checked_out
        logger.info(f"Book availability for '{title}': {'Available' if availability else 'Checked out'}.")
        return availability

    def list_available_books(self) -> Dict[str, str]:
        """
        Lists all available books in the library.

        Returns:
            Dict[str, str]: A dictionary of available books with titles as keys and authors as values.
        """
        available_books = {title: book.author for title, book in self.books.items() if not book.is_checked_out}
        logger.info(f"Listing available books: {len(available_books)} found.")
        return available_books

    def list_all_books(self) -> Dict[str, Dict[str, any]]:
        """
        Lists all books in the library along with their availability status.

        Returns:
            Dict[str, Dict[str, any]]: A dictionary of all books with their details.
        """
        all_books = {
            title: {
                'author': book.author,
                'is_checked_out': book.is_checked_out
            } for title, book in self.books.items()
        }
        logger.info(f"Listing all books: {len(all_books)} found.")
        return all_books

    def _get_book(self, title: str) -> Book:
        """
        Retrieves a book from the library.

        Args:
            title (str): The title of the book.

        Returns:
            Book: The Book instance.

        Raises:
            BookNotFoundError: If the book is not found in the library.
        """
        if title not in self.books:
            logger.error(f"Book not found: '{title}'.")
            raise BookNotFoundError(f"The book '{title}' does not exist in the library.")
        return self.books[title]


# Example Usage
if __name__ == "__main__":
    # Initialize the library
    library = Library()

    # Add books to the library
    try:
        library.add_book("1984", "George Orwell")
        library.add_book("To Kill a Mockingbird", "Harper Lee")
        library.add_book("The Great Gatsby", "F. Scott Fitzgerald")
    except BookAlreadyExistsError as e:
        logger.warning(e)

    # List all books
    print("\nAll Books in Library:")
    for title, details in library.list_all_books().items():
        status = "Checked Out" if details['is_checked_out'] else "Available"
        print(f"'{title}' by {details['author']} - {status}")

    # Checkout a book
    try:
        library.checkout_book("1984")
    except (BookNotFoundError, BookAlreadyCheckedOutError) as e:
        logger.warning(e)

    # Check availability
    try:
        availability = library.is_book_available("1984")
        print(f"\nIs '1984' available? {'Yes' if availability else 'No'}")
    except BookNotFoundError as e:
        logger.warning(e)

    # Return a book
    try:
        library.return_book("1984")
    except (BookNotFoundError, BookNotCheckedOutError) as e:
        logger.warning(e)

    # List available books
    print("\nAvailable Books in Library:")
    for title, author in library.list_available_books().items():
        print(f"'{title}' by {author}")
