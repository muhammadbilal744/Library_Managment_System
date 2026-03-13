# OOP Library Management System


##  Short Description
This project is a robust, terminal-based Library Management System built entirely in Python. It simulates a real-world library where administrators can manage a catalog of books, register members, process borrowing and returning workflows, and calculate late fines. 

The primary goal of this project is to demonstrate a deep understanding of core **Object-Oriented Programming (OOP)** principles and clean code practices. The business logic is strictly decoupled from the Command Line Interface (CLI), ensuring the system is modular, highly testable, and easy to maintain.

---

## Features
* **Interactive CLI:** A user-friendly, clear-screen terminal interface with nested menus.
* **Authentication Simulation:** A simple login system to track which member is currently performing borrowing/returning actions.
* **Book Management:** Add new books, search for specific titles, and view lists of all books or only currently available books.
* **Member Management:** Register new members, enforce borrowing limits (max 3 books), and track individual borrowing histories.
* **Dynamic Fine Calculation:** Choose from multiple fine policies at startup (Simple, Progressive, or No Fine) to dynamically calculate late fees upon book returns.

---

##  Project Structure
The repository is strictly organized to separate concerns, keeping models, business rules, tests, and user interfaces in their dedicated domains:

```text
oop-library-system/
│
├── src/
│   ├── __init__.py
│   ├── models.py         # Data classes: Book, Member, BorrowRecord, FinePolicy
│   └── library.py        # Core business logic and orchestration
│
├── tests/
│   ├── __init__.py
│   └── test_library.py   # 14 automated unit tests
│
├── cli.py                # Command Line Interface (I/O only)
├── README.md             # Project documentation
└── .gitignore            # Git ignore rules for Python
