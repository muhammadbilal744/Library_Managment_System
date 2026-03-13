"""
cli.py - Command Line Interface for Library Management System
Works perfectly with the encapsulated Library class in src/library.py
"""

import os
from datetime import date
from src.library import Library
from src.models import SimpleFinePolicy, FinePolicy

# ===== CUSTOM POLICIES FOR THE MENU =====
class ProgressiveFinePolicy(FinePolicy):
    """Charges $5/day for first 5 days, then $10/day after that."""
    def calculate(self, days_late: int) -> float:
        if days_late <= 0: return 0.0
        if days_late <= 5: return float(days_late * 5.0)
        return float((5 * 5.0) + ((days_late - 5) * 10.0))

class NoFinePolicy(FinePolicy):
    """Never charges a fine."""
    def calculate(self, days_late: int) -> float:
        return 0.0

# ===== CLI HELPERS =====
def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 50)
    print(f" {title}")
    print("=" * 50)

def main():
    """Main CLI function"""
    
    # ===== SETUP =====
    clear_screen()
    print_header("LIBRARY MANAGEMENT SYSTEM SETUP")
    
    print("\nChoose Fine Policy:")
    print("1. Simple Fine ($5 per day)")
    print("2. Progressive Fine ($5 initially, then $10)")
    print("3. No Fine")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "2":
        library = Library(ProgressiveFinePolicy())
        print("Progressive Fine Policy selected")
    elif choice == "3":
        library = Library(NoFinePolicy())
        print("No Fine Policy selected")
    else:
        library = Library(SimpleFinePolicy())
        print("Simple Fine Policy selected")
    
    input("\nPress Enter to continue...")
    
    # ===== MAIN LOOP =====
    current_member = None
    
    while True:
        clear_screen()
        print_header("LIBRARY MANAGEMENT SYSTEM")
        
        # Safe encapsulated access to the current member
        if current_member:
            try:
                member = library.get_member(current_member)
                print(f"\n Logged in: {member.name} ({current_member})")
                print(f" Books borrowed: {len(member.borrowed_books)}/3")
            except KeyError:
                current_member = None
        else:
            print("\nNot logged in")
        
        print("\n=== MAIN MENU ===")
        print("1. Book Operations")
        print("2. Member Operations")
        print("3. Borrow/Return")
        print("4. Login/Logout")
        print("0. Exit")
        
        cmd = input("\nChoice: ").strip()
        
        # ===== BOOK OPERATIONS =====
        if cmd == "1":
            while True:
                clear_screen()
                print_header("BOOK OPERATIONS")
                print("1. Add Book")
                print("2. List All Books")
                print("3. List Available Books")
                print("4. Search Book")
                print("0. Back")
                
                sub = input("\nChoice: ").strip()
                
                if sub == "1":  # Add Book
                    book_id = input("Book ID: ")
                    title = input("Title: ")
                    author = input("Author: ")
                    try:
                        library.add_book(book_id, title, author)
                        print(f"Book '{title}' added")
                    except ValueError as e:
                        print(f" {e}")
                
                elif sub == "2":  # List All Books
                    print("\n--- ALL BOOKS ---")
                    # Use public method list_all_books() instead of private dictionary
                    for book in library.list_all_books():
                        # is_available is a property, no () needed
                        status = " Available" if book.is_available else "✗ Borrowed"
                        print(f"{book.book_id}: {book.title} by {book.author} [{status}]")
                
                elif sub == "3":  # List Available Books
                    print("\n--- AVAILABLE BOOKS ---")
                    available = library.list_available_books()
                    if available:
                        for book in available:
                            print(f"{book.book_id}: {book.title} by {book.author}")
                    else:
                        print("No books available")
                
                elif sub == "4":  # Search Book
                    book_id = input("Enter Book ID: ")
                    try:
                        book = library.get_book(book_id)
                        print(f"\nTitle: {book.title}")
                        print(f"Author: {book.author}")
                        print(f"Status: {'Available' if book.is_available else 'Borrowed'}")
                    except KeyError:
                        print(" Book not found")
                
                elif sub == "0":
                    break
                
                input("\nPress Enter...")
        
        # ===== MEMBER OPERATIONS =====
        elif cmd == "2":
            while True:
                clear_screen()
                print_header("MEMBER OPERATIONS")
                print("1. Add Member")
                print("2. List All Members")
                print("3. Search Member")
                print("0. Back")
                
                sub = input("\nChoice: ").strip()
                
                if sub == "1":  # Add Member
                    member_id = input("Member ID: ")
                    name = input("Name: ")
                    try:
                        library.add_member(member_id, name)
                        print(f" Member '{name}' added")
                    except ValueError as e:
                        print(f" {e}")
                
                elif sub == "2":  # List All Members
                    print("\n--- ALL MEMBERS ---")
                    for member in library.list_all_members():
                        print(f"{member.member_id}: {member.name} [{len(member.borrowed_books)}/3 books]")
                
                elif sub == "3":  # Search Member
                    member_id = input("Enter Member ID: ")
                    try:
                        member = library.get_member(member_id)
                        print(f"\nName: {member.name}")
                        print(f"Books borrowed: {len(member.borrowed_books)}/3")
                        if member.borrowed_books:
                            print("\nCurrently reading:")
                            for bid in member.borrowed_books:
                                try:
                                    book = library.get_book(bid)
                                    print(f"  • {book.title}")
                                except KeyError:
                                    pass
                    except KeyError:
                        print(" Member not found")
                
                elif sub == "0":
                    break
                
                input("\nPress Enter...")
        
        # ===== BORROW/RETURN =====
        elif cmd == "3":
            if not current_member:
                print("Please login first!")
                input("\nPress Enter...")
                continue
            
            while True:
                clear_screen()
                print_header("BORROW/RETURN")
                print("1. Borrow Book")
                print("2. Return Book")
                print("3. My Borrowed Books")
                print("0. Back")
                
                sub = input("\nChoice: ").strip()
                
                if sub == "1":  # Borrow
                    available = library.list_available_books()
                    if available:
                        print("\nAvailable books:")
                        for book in available:
                            print(f"  {book.book_id}: {book.title}")
                    
                    book_id = input("\nBook ID to borrow: ")
                    try:
                        library.borrow_book(current_member, book_id, date.today())
                        print("Book borrowed successfully!")
                    except (KeyError, ValueError) as e:
                        print(f"{e}")
                
                elif sub == "2":  # Return
                    member = library.get_member(current_member)
                    if member.borrowed_books:
                        print("\nYour books:")
                        for bid in member.borrowed_books:
                            try:
                                book = library.get_book(bid)
                                print(f"  {bid}: {book.title}")
                            except KeyError:
                                pass
                    
                    book_id = input("\nBook ID to return: ")
                    try:
                        fine = library.return_book(current_member, book_id, date.today())
                        if fine > 0:
                            print(f" Book returned. Fine: ₹{fine:.2f}")
                        else:
                            print(" Book returned on time!")
                    except (KeyError, ValueError) as e:
                        print(f"{e}")
                
                elif sub == "3":  # My Books
                    member = library.get_member(current_member)
                    if member.borrowed_books:
                        print("\nBooks you're reading:")
                        for bid in member.borrowed_books:
                            try:
                                book = library.get_book(bid)
                                print(f"  • {book.title} by {book.author}")
                            except KeyError:
                                pass
                    else:
                        print("You haven't borrowed any books")
                
                elif sub == "0":
                    break
                
                input("\nPress Enter...")
        
        # ===== LOGIN/LOGOUT =====
        elif cmd == "4":
            if current_member:
                print(f"Logged out from {current_member}")
                current_member = None
            else:
                member_id = input("Enter Member ID: ")
                try:
                    member = library.get_member(member_id)
                    current_member = member_id
                    print(f"Logged in as {member.name}")
                except KeyError:
                    print("Member not found")
            input("\nPress Enter...")
        
        # ===== EXIT =====
        elif cmd == "0":
            print("\nThanks for using the Library System!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")