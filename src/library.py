"""
library.py - Main Library class that coordinates everything
OOP Concepts: Composition, Dependency Injection, Encapsulation
"""
from typing import Dict, List, Optional
from datetime import date
from .models import Book, Member, BorrowRecord, FinePolicy

class Library:
    """
    Main Library class that manages books, members, and borrowing.
    
    OOP Concepts Used:
    1. COMPOSITION: Library HAS-A collection of Books, Members, Records
    2. DEPENDENCY INJECTION: FinePolicy is injected (given to Library)
    3. ENCAPSULATION: All data is private, accessed through methods
    """
    
    def __init__(self, fine_policy: FinePolicy):
        """
        Initialize an empty library with a fine policy.
        
        Args:
            fine_policy: A FinePolicy object (Dependency Injection!)
                         Library doesn't create its own policy - it's given one.
        """
        self.fine_policy = fine_policy
        self._books: Dict[str, Book] = {}      # Private! Use methods to access
        self._members: Dict[str, Member] = {}  # Private! Use methods to access
        self._records: List[BorrowRecord] = [] # Private! Use methods to access
    
    # ========== BOOK MANAGEMENT ==========
    
    def add_book(self, book_id: str, title: str, author: str) -> None:
        """Adds a new book to the library."""
        if book_id in self._books:
            raise ValueError(f"Book with ID {book_id} already exists!")
        
        book = Book(book_id=book_id, title=title, author=author)
        self._books[book_id] = book
    
    def get_book(self, book_id: str) -> Book:
        """Gets a book by ID."""
        if book_id not in self._books:
            raise KeyError(f"Book with ID {book_id} not found!")
        return self._books[book_id]
    
    def list_all_books(self) -> List[Book]:
        """Return list of all books."""
        return list(self._books.values())
    
    def list_available_books(self) -> List[Book]:
        """Return list of currently available books."""
        return [book for book in self._books.values() if book.is_available]
    
    # ========== MEMBER MANAGEMENT ==========
    
    def add_member(self, member_id: str, name: str) -> None:
        """Adds a new member to the library."""
        if member_id in self._members:
            raise ValueError(f"Member with ID {member_id} already exists!")
        
        member = Member(member_id=member_id, name=name)
        self._members[member_id] = member
    
    def get_member(self, member_id: str) -> Member:
        """Gets a member by ID."""
        if member_id not in self._members:
            raise KeyError(f"Member with ID {member_id} not found!")
        return self._members[member_id]
    
    def list_all_members(self) -> List[Member]:
        """Return list of all members."""
        return list(self._members.values())
    
    # ========== BORROWING OPERATIONS ==========
    
    def borrow_book(self, member_id: str, book_id: str, borrow_date: date) -> None:
        """Process a book borrowing."""
        # Step 1: Validate IDs exist
        if member_id not in self._members:
            raise KeyError(f"Member {member_id} not found!")
        if book_id not in self._books:
            raise KeyError(f"Book {book_id} not found!")
        
        member = self._members[member_id]
        book = self._books[book_id]
        
        # Step 2: Ask book to borrow itself (encapsulation)
        book.borrow()
        
        # Step 3: Ask member to add to their list
        try:
            member.borrow_book(book_id)
        except ValueError as e:
            # Rollback if the member cannot borrow the book
            book.return_book() 
            raise e 
        
        # Step 4: Create record
        record = BorrowRecord(
            member_id=member_id,
            book_id=book_id,
            borrow_date=borrow_date
        )
        self._records.append(record)
    
    def return_book(self, member_id: str, book_id: str, return_date: date) -> float:
        """Process a book return and calculate fine."""
        # Step 1: Validate IDs exist
        if member_id not in self._members:
            raise KeyError(f"Member {member_id} not found!")
        if book_id not in self._books:
            raise KeyError(f"Book {book_id} not found!")
        
        member = self._members[member_id]
        book = self._books[book_id]
        
        # Step 2 & 3: Return the book
        member.return_book(book_id)
        book.return_book()
        
        # Step 4: Find and update the borrowing record
        record = self._find_active_record(member_id, book_id)
        if not record:
            raise ValueError(f"No active borrowing record found for {member_id} - {book_id}")
        
        record.return_date = return_date
        
        # Step 5: Calculate fine (Assuming a 7-day grace period)
        days_borrowed = (return_date - record.borrow_date).days
        days_late = days_borrowed - 7
        
        fine = self.fine_policy.calculate(days_late)
        return fine
    
    def _find_active_record(self, member_id: str, book_id: str) -> Optional[BorrowRecord]:
        """PRIVATE METHOD: Find an active borrowing record (no return date)."""
        # Searching backwards ensures we find the most recent borrow record
        for record in reversed(self._records):
            if (record.member_id == member_id and 
                record.book_id == book_id and 
                record.return_date is None):
                return record
        return None
    
    # ========== UTILITY METHODS ==========
    
    def get_member_borrowed_books(self, member_id: str) -> List[Book]:
        """Get all books currently borrowed by a member."""
        member = self.get_member(member_id)
        borrowed_ids = member.borrowed_books 
        
        books = []
        for book_id in borrowed_ids:
            if book_id in self._books:
                books.append(self._books[book_id])
        return books
    
    def get_all_records(self) -> List[BorrowRecord]:
        """Get all borrowing records (returns a copy)."""
        return self._records.copy()
    
    def get_borrowing_history(self, member_id: str) -> List[BorrowRecord]:
        """Get all records for a specific member."""
        return [r for r in self._records if r.member_id == member_id]