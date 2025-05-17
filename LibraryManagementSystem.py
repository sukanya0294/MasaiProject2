# -*- coding: utf-8 -*-
"""
Created on Sat May 17 21:09:31 2025

@author: HP
"""

from dataclasses import dataclass

@dataclass
class Book:
       ISBN: str
       Title: str
       Author: str
       CopiesTotal: int
       CopiesAvailable: int
@dataclass
class Member:
       MemberID: str
       Name: str
       PasswordHash: str
       Email: str
       JoinDate: str
@dataclass
class Loan:
       LoanID: str
       MemberID: str
       ISBN: str
       IssueDate: str
       DueDate: str
       ReturnDate: str

import csv
from models import Book, Member, Loan

def load_books():
      with open('books.csv', newline='') as f:
           return[Book(**row) for row in csv.DictReader(f)]

def save_books(books):
      with open('books.csv', 'w', newline='') as f:
           writer = csv.Dictwriter(f, fieldnames=books[0].__dict__.keys())
           writer.writerheader()
           for book in books:
                writer.writerow(book.dict)
def load_members():
      with open('members.csv', newline='') as f:
         return [Member(**row) for row in csv.DictReader(f)]
def save_members(members):
      with open('members.csv', 'w', newline='') as f:
       writer = csv.DictWriter(f, fieldnames=members[0].dict.keys())
       writer.writeheader()
       for member in members:
          writer.writerow(member.dict)
def load_loans():
      with open('loans.csv', newline='') as f:
        return [Loan(**row) for row in csv.DictReader(f)]
def save_loans(loans):
      with open('loans.csv', 'w', newline='') as f:
       writer = csv.DictWriter(f, fieldnames=loans[0].dict.keys())
       writer.writeheader()
       for loan in loans:
          writer.writerow(loan.dict)

import bcrypt
import datetime
from models import Member
from storage import save_members

def hash_password(password):
     return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
     return bcrypt.checkpw(password.encode(), hashed.encode())

def login(members):
     email = input("Email: ")
     password = input("Password: ")
     for member in members:
         if member.Email == email and check_password(password, member.PasswordHash):
             print("Login successful!")
             return member
     print("Login failed.")
     return None

def register_member(members):
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    member_id = str(len(members) + 1)
    hashed = hash_password(password)
    join_date = str(datetime.date.today())
    member = Member(member_id, name, hashed, email, join_date)
    members.append(member)
    save_members(members)
    print("Registration successful!")

from storage import load_books, save_books, load_loans, save_loans, load_members
from models import Loan
import datetime

def librarian_menu(user):
    while True:
         print("\n=== Librarian Dashboard ===")
         print("1. Add Book\n2. Delete Book\n3. Issue Book\n4. Return Book\n5. View Overdue\n6. Logout")
         choice = input("Choose an option: ")
         if choice == '1':
            add_book()
         elif choice == '2':
             delete_book()
         elif choice == '3':
             issue_book()
         elif choice == '4':
             return_book()
         elif choice == '5':
             view_overdue()
         elif choice == '6':
             break
         else:
             print("Invalid choice")

def add_book():
      books = load_books()
      isbn = input("ISBN: ")
      title = input("Title: ")
      author = input("Author: ")
      total = int(input("Total Copies: "))
      book = Book(isbn, title, author, total, total)
      books.append(book)
      save_books(books)
      print("Book added.")

def delete_book():
      books = load_books()
      isbn = input("ISBN to delete: ")
      books = [b for b in books if b.ISBN != isbn]
      save_books(books)
      print("Book deleted.")

def issue_book():
      loans = load_loans()
      books = load_books()
      members = load_members()
      member_id = input("Member ID: ")
      isbn = input("Book ISBN: ")
      book = next((b for b in books if b.ISBN == isbn), None)
      if book and book.CopiesAvailable > 0:
          loan_id = str(len(loans) + 1)
          issue_date = str(datetime.date.today())
          due_date = str(datetime.date.today() + datetime.timedelta(days=14))
          loan = Loan(loan_id, member_id, isbn, issue_date, due_date, '')
          book.CopiesAvailable -= 1
          loans.append(loan)
          save_loans(loans)
          save_books(books)
          print("Book issued.")
      else:
          print("Book not available.")

def return_book():
        loans = load_loans()
        books = load_books()
        loan_id = input("Loan ID: ")
        for loan in loans:
           if loan.LoanID == loan_id and not loan.ReturnDate:
                loan.ReturnDate = str(datetime.date.today())
                book = next((b for b in books if b.ISBN == loan.ISBN), None)
                if book:
                   book.CopiesAvailable += 1
                break
        save_loans(loans)
        save_books(books)
        print("Book returned.")

def view_overdue():
        loans = load_loans()
        today = datetime.date.today()
        for loan in loans:
             if not loan.ReturnDate and datetime.date.fromisoformat(loan.DueDate) < today:
                print(loan)

from storage import load_books, load_loans, save_loans, save_books
from models import Loan
import datetime

def member_menu(user):
     while True:
        print("\n=== Member Dashboard ===")
        print("1. Search Books\n2. Borrow Book\n3. My Loans\n4. Logout")
        choice = input("Choose an option: ")
        if choice == '1':
           search_books()
        elif choice == '2':
           borrow_book(user)
        elif choice == '3':
           my_loans(user)
        elif choice == '4':
           break
        else:
           print("Invalid choice")

def search_books():
        books = load_books()
        keyword = input("Enter title or author keyword: ").lower()
        for book in books:
           if keyword in book.Title.lower() or keyword in book.Author.lower():
                 print(book)

def borrow_book(user):
        books = load_books()
        loans = load_loans()
        isbn = input("Book ISBN: ")
        book = next((b for b in books if b.ISBN == isbn), None)
        if book and book.CopiesAvailable > 0:
             loan_id = str(len(loans) + 1)
             issue_date = str(datetime.date.today())
             due_date = str(datetime.date.today() + datetime.timedelta(days=14))
             loan = Loan(loan_id, user.MemberID, isbn, issue_date, due_date, '')
             book.CopiesAvailable -= 1
             loans.append(loan)
             save_loans(loans)
             save_books(books)
             print("Book borrowed.")
        else:
             print("Book not available.")

def my_loans(user):
        loans = load_loans()
        for loan in loans:
            if loan.MemberID == user.MemberID:
                 print(loan)
