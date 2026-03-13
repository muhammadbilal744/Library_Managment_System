"""
test_library.py - Unit tests for Library Management System
Requirements: At least 8 tests focusing on business logic
"""

import unittest
from datetime import date
import sys
import os

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.library import Library
from src.models import Book, Member, SimpleFinePolicy, FinePolicy

# A custom policy just for Test 10 to prove Polymorphism works!
class NoFinePolicy(FinePolicy):
    def calculate(self, days_late: int) -> float:
        return 0.0

class TestLibrarySystem(unittest.TestCase):
    """Test cases for Library Management System"""
    
    def setUp(self):
        """Create fresh library before each test"""
        self.lib = Library(SimpleFinePolicy(per_day=5.0))
        
        # Add test data
        self.lib.add_book("B001", "Python Basics", "John Doe")
        self.lib.add_book("B002", "Data Science", "Jane Smith")
        self.lib.add_member("M001", "Alice")
        self.lib.add_member("M002", "Bob")
    
    # ===== TEST 1: Add Book =====
    def test_add_book(self):
        """Test that books can be added successfully"""
        self.lib.add_book("B003", "New Book", "New Author")
        book = self.lib.get_book("B003")
        self.assertEqual(book.title, "New Book")
    
    # ===== TEST 2: Add Duplicate Book (Failure Test) =====
    def test_add_duplicate_book(self):
        """Test that adding duplicate book ID raises error"""
        with self.assertRaises(ValueError):
            self.lib.add_book("B001", "Duplicate", "Author")
    
    # ===== TEST 3: Add Member =====
    def test_add_member(self):
        """Test that members can be added successfully"""
        self.lib.add_member("M003", "Charlie")
        member = self.lib.get_member("M003")
        self.assertEqual(member.name, "Charlie")
    
    # ===== TEST 4: Borrow Book =====
    def test_borrow_book(self):
        """Test borrowing a book"""
        self.lib.borrow_book("M001", "B001", date(2024, 1, 1))
        
        # Book should be unavailable (is_available is a property now)
        self.assertFalse(self.lib.get_book("B001").is_available)
        
        # Member should have the book
        self.assertIn("B001", self.lib.get_member("M001").borrowed_books)
    
    # ===== TEST 5: Borrow Unavailable Book (Failure Test) =====
    def test_borrow_unavailable_book(self):
        """Test that borrowing already borrowed book raises error"""
        # First borrow
        self.lib.borrow_book("M001", "B001", date(2024, 1, 1))
        
        # Try to borrow again
        with self.assertRaises(ValueError):
            self.lib.borrow_book("M002", "B001", date(2024, 1, 1))
    
    # ===== TEST 6: Borrow Limit Reached (Failure Test) =====
    def test_borrow_limit_reached(self):
        """Test that member cannot borrow more than 3 books"""
        # Add more books
        self.lib.add_book("B003", "Book 3", "Author")
        self.lib.add_book("B004", "Book 4", "Author")
        
        # Borrow 3 books
        self.lib.borrow_book("M001", "B001", date(2024, 1, 1))
        self.lib.borrow_book("M001", "B002", date(2024, 1, 1))
        self.lib.borrow_book("M001", "B003", date(2024, 1, 1))
        
        # Try to borrow 4th book
        with self.assertRaises(ValueError):
            self.lib.borrow_book("M001", "B004", date(2024, 1, 1))
    
    # ===== TEST 7: Return Book =====
    def test_return_book(self):
        """Test returning a book"""
        # Borrow first
        self.lib.borrow_book("M001", "B001", date(2024, 1, 1))
        
        # Return within 7-day grace period
        fine = self.lib.return_book("M001", "B001", date(2024, 1, 5))
        
        # Book should be available
        self.assertTrue(self.lib.get_book("B001").is_available)
        
        # Member should not have the book
        self.assertNotIn("B001", self.lib.get_member("M001").borrowed_books)
        
        # Fine should be 0 (returned early)
        self.assertEqual(fine, 0.0)
    
    # ===== TEST 8: Return Book Not Borrowed (Failure Test) =====
    def test_return_not_borrowed(self):
        """Test that returning book not borrowed raises error"""
        with self.assertRaises(ValueError):
            # Attempt to return a book that hasn't been borrowed
            self.lib.return_book("M001", "B002", date(2024, 1, 10))
    
    # ===== TEST 9: Calculate Fine =====
    def test_calculate_fine(self):
        """Test fine calculation for late return"""
        # Borrow Jan 1
        self.lib.borrow_book("M001", "B001", date(2024, 1, 1))
        
        # Return late (Jan 20 -> 19 days total)
        # 19 days - 7 day grace period = 12 days late
        # 12 days * 5.0 = 60.0
        fine = self.lib.return_book("M001", "B001", date(2024, 1, 20))
        self.assertEqual(fine, 60.0)
    
    # ===== TEST 10: Different Fine Policy =====
    def test_different_fine_policy(self):
        """Test that different policy gives different fine"""
        # Create library with no fine policy
        lib2 = Library(NoFinePolicy())
        lib2.add_book("B001", "Python", "Author")
        lib2.add_member("M001", "Ali")
        
        # Borrow and return very late
        lib2.borrow_book("M001", "B001", date(2024, 1, 1))
        fine = lib2.return_book("M001", "B001", date(2024, 1, 20))
        
        # No fine should be charged
        self.assertEqual(fine, 0.0)
    
    # ===== TEST 11: Invalid Member ID (Failure Test) =====
    def test_invalid_member_id(self):
        """Test that using invalid member ID raises error"""
        with self.assertRaises(KeyError):
            self.lib.borrow_book("INVALID", "B001", date.today())
    
    # ===== TEST 12: Invalid Book ID (Failure Test) =====
    def test_invalid_book_id(self):
        """Test that using invalid book ID raises error"""
        with self.assertRaises(KeyError):
            self.lib.borrow_book("M001", "INVALID", date.today())
    
    # ===== TEST 13: Book Availability After Return =====
    def test_book_available_after_return(self):
        """Test that book becomes available after return"""
        self.lib.borrow_book("M001", "B001", date(2024, 1, 1))
        self.assertFalse(self.lib.get_book("B001").is_available)
        
        self.lib.return_book("M001", "B001", date(2024, 1, 5))
        self.assertTrue(self.lib.get_book("B001").is_available)
    
    # ===== TEST 14: Member Borrowed Books List =====
    def test_member_borrowed_list(self):
        """Test that member's borrowed books list is correct"""
        self.lib.borrow_book("M001", "B001", date(2024, 1, 1))
        self.lib.borrow_book("M001", "B002", date(2024, 1, 1))
        
        member = self.lib.get_member("M001")
        self.assertEqual(len(member.borrowed_books), 2)
        self.assertIn("B001", member.borrowed_books)
        self.assertIn("B002", member.borrowed_books)

if __name__ == "__main__":
    unittest.main()