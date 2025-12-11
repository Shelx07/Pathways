import csv
import os 
#one record is [user id , passwd, number of books taken,[list of books taken]]
FILE = "Report.csv"

def ensure_file_exists():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            pass

def load_data():
    """
    Returns list of lists: [[user, pass, count, [books]]
    """
    ensure_file_exists()
    data = []
    with open(FILE, "r", newline="") as f:
        reader = csv.reader(f)   #reader object
        for row in reader:     #iterating thru the data
            if not row:      # if it is not empty
                continue

            # Ensure row has 4 columns
            
            user = row[0]
            passwd = row[1]
            # row[2] is count (ignored, we calculate it from list)
            book_str = row[3]

            # Convert string "b1|b2" -> list ["b1", "b2"]
            books = []
            if book_str:
                parts = book_str.split("|")   #book1 | book 2 | book 3   ---> [book1,book2,book3]
                for b in parts:
                    if b:
                        books.append(b)
            
            data.append([user, passwd, len(books), books])
    return data

def save_data(data):
    """Saves list of lists back to CSV"""
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        for row in data:
            # row is [user, pass, count, [book_list]]
            user = row[0]
            passwd = row[1]
            book_list = row[3]
            
            # Join list back to string "book1|book2"
            book_str = "|".join(book_list)   # as ":".join([1,2,3]) ---->1:2:3
            
            writer.writerow([user, passwd, len(book_list), book_str])

# --- Operations ---

def create_account(user, passwd):
    if not user or not passwd:
        return False, "User ID and password required."

    data = load_data()
    
    # Check if user exists
    user_exists = False
    for row in data:#[1st record]
        if row[0] == user:
            user_exists = True
            break
            
    if user_exists:
        return False, "User ID already exists."
    
    # Append new user: [user, pass, 0, empty_list]
    data.append([user, passwd, 0, []])
    save_data(data)
    return True, f"Account '{user}' created."

def add_books(user, passwd, new_books): # new_books is a list
    if not new_books:  # checks if new_books is empty or not
        return False, "No books provided."

    data = load_data()
    for row in data:
        if row[0] == user and row[1] == passwd:
            # Add new books one by one 
            current_books = row[3]
            for b in new_books:
                if b:
                    current_books.append(b)
            
            save_data(data)
            return True, f"Added {len(new_books)} books."
            
    return False, "User ID or password incorrect."

def return_books(user, passwd, remove_list):
    if not remove_list:
        return None, "No books provided."

    data = load_data()
    for row in data:
        if row[0] == user and row[1] == passwd:
            current_books = row[3]
            before_count = len(current_books)
            
            # Create a new list keeping only books NOT in remove_list
            updated_books = []
            for b in current_books:
                if b not in remove_list:
                    updated_books.append(b)
            
            row[3] = updated_books
            save_data(data)
            
            returned_count = before_count - len(updated_books)
            return returned_count, f"Returned {returned_count} books."
            
    return None, "User ID or password incorrect."

def get_user(user, passwd):
    """
    Finds the user list
    """
    data = load_data()
    for row in data:
        if row[0] == user and row[1] == passwd:
            return {'user': row[0], 'pass': row[1], 'books': row[3]}
    return None