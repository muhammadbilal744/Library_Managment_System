"""
models.py - Contains the data classes and policies for our Library System
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set, Optional
from datetime import date
from abc import ABC, abstractmethod

# ==========================================
# Policy (Abstraction & Polymorphism)
# ==========================================
class FinePolicy(ABC):
    """
    Abstract base class for fine calculation policies.
    OOP Concept: Abstraction - Defines an interface without implementing it.
    """
    @abstractmethod
    def calculate(self, days_late: int) -> float:
        pass


class SimpleFinePolicy(FinePolicy):
    """
    Calculates fines based on a flat daily rate.
    OOP Concept: Polymorphism/Inheritance - Implements the FinePolicy blueprint.
    """
    def __init__(self, per_day: float = 5.0):
        self.per_day = per_day

    def calculate(self, days_late: int) -> float:
        # Return fine for late days (no negative fines)
        if days_late <= 0:
            return 0.0
        return float(days_late * self.per_day)

# ==========================================
# Data Models (Encapsulation)
# ==========================================
@dataclass
class Book:
    """
    Represents a book in the library.
    
    OOP Concepts:
    - Encapsulation: _available is private
    - Methods: borrow() and return_book() control access
    """
    book_id: str
    title: str
    author: str
    _available: bool = field(default=True, repr=False)  # Private attribute
    
    def borrow(self) -> None:
        """
        Mark book as borrowed.
        This method ENCAPSULATES the logic of borrowing.
        """
        if not self._available:
            raise ValueError(f"Book '{self.title}' is currently unavailable.")
        self._available = False
    
    def return_book(self) -> None:
        """
        Mark book as available again.
        """
        self._available = True
    
    @property
    def is_available(self) -> bool:
        """
        Public property to check availability (read-only access)
        """
        return self._available


@dataclass
class Member:
    """
    Represents a library member.
    
    OOP Concepts:
    - Encapsulation: _borrowed_books is protected
    - @property: provides controlled access to private data
    """
    member_id: str
    name: str
    _borrowed_books: Set[str] = field(default_factory=set, repr=False)
    
    def borrow_book(self, book_id: str, limit: int = 3) -> None:
        """
        Add a book to member's borrowed list.
        
        Args:
            book_id: ID of book being borrowed
            limit: Maximum books a member can borrow
            
        Raises:
            ValueError: If member has reached borrow limit
        """
        if len(self._borrowed_books) >= limit:
            raise ValueError(f"Member '{self.name}' has reached the borrowing limit of {limit} books.")
        self._borrowed_books.add(book_id)
    
    def return_book(self, book_id: str) -> None:
        """
        Remove a book from member's borrowed list.
        
        Args:
            book_id: ID of book being returned
            
        Raises:
            ValueError: If member didn't borrow this book
        """
        if book_id not in self._borrowed_books:
            raise ValueError(f"Member '{self.name}' does not have book '{book_id}' borrowed.")
        self._borrowed_books.remove(book_id)
    
    @property
    def borrowed_books(self) -> Set[str]:
        """
        Property decorator - provides read-only access to borrowed_books.
        Returns a COPY to prevent direct modification.
        """
        return set(self._borrowed_books)


@dataclass
class BorrowRecord:
    """
    Records a single borrowing transaction.
    This is a simple data class - no methods needed.
    """
    member_id: str
    book_id: str
    borrow_date: date
    return_date: Optional[date] = None