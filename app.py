from collections import deque
from benchmark import run_benchmark
from flask import Flask, render_template, request, redirect, url_for
import os
import time

app = Flask(__name__)

app.config['FLASK_TITLE'] = ""
 
# Record the start time when the app starts
start_time = time.time()

# Implement undo/redo using a stack for undo and a queue for redo (FIFO).
# Each operation (add/delete) will push the current state of the contact list onto the undo stack
# before modifying it. When undoing, we pop from the undo stack and enqueue the current state onto
# the redo queue. When redoing, we dequeue from the redo queue and push the current state back onto
# the undo stack.
# undo_stack stores snapshots of the contact list before each operation
# redo_queue stores snapshots of the contact list that were undone
# Each snapshot must be a python list of contacts (ID, name, email)
undo_stack = []
redo_queue = deque()

# Create a hash table (dictionary) to store contacts for O(1) search by name
# The key will be the contact name (lowercased for case-insensitive search)
# We will maintain this hash table in sync with the linked list to allow for efficient lookups and deletions.
# We will use quick sort and binary search for searching contacts, but the hash table will still be useful for O(1) lookups during add/delete operations and for building the sorted list for display.

contact_dict = {}
next_contact_id = 3  # This will be used to assign unique IDs to contacts if needed in the future



# --- IN-MEMORY DATA STRUCTURES (Students will modify this area) ---

# Phase 2: Linked List implementation
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
    def delete(self, key):
        temp = self.head
        if temp is not None:
            if temp.data == key:
                self.head = temp.next
                temp = None
                return
        while temp is not None:
            if temp.data == key:
                break
            prev = temp
            temp = temp.next
        if temp is None:
            return
        prev.next = temp.next
        temp = None
    def find_by_name(self, name):
        current = self.head
        while current:
            if current.data[1].lower() == name.lower():
                return current.data
            current = current.next
        return None 
    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next
    #Add helper methods to:
    # 1. Convert the linked list to a Python list of contacts (to_list)
    # 2. Create a linked list from a Python list of contacts (from_list)
    # These methods will help with undo/redo functionality
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(list(current.data))
            current = current.next
        return result
    def from_list(self, data_list):
        self.head = None
        for data in data_list:
            self.append(data)

# Initialize linked list with sample contacts; add ID field to each contact for better tracking and searching 
 
contacts = LinkedList()
contacts.append([1, 'Alice', 'alice@example.com'])
contacts.append([2, 'Bob', 'bob@example.com'])

# Build hash index from linked list for O(1) search
current = contacts.head 
while current:
    name = current.data[1].lower()
    contact_dict[name] = current.data
    current = current.next

# Implement Quick Sort to sort contacts alphabetically by name.
# The input will be a Python list of contacts where each contact is
# stored as [ID, name, email].
# Quick Sort will:
# 1. Choose a pivot element
# 2. Partition contacts into three lists (less, equal, greater)
#    based on alphabetical comparison of the name field.
# 3. Recursively sort the left and right partitions.
# 4. Return the combined sorted list.
#
# This function will be used before performing binary search,
# since binary search requires the data to be sorted.
def quick_sort(contacts):
    if len(contacts) <= 1:
        return contacts
    pivot = contacts[len(contacts) // 2][0]
    left = [x for x in contacts if x[0] < pivot]
    middle = [x for x in contacts if x[0] == pivot]
    right = [x for x in contacts if x[0] > pivot]
    return quick_sort(left) + middle + quick_sort(right)
# Implement binary search to find a contact by name in a sorted list.
# The input will be a sorted list of contacts where each contact is
# stored as [ID, name, email].
#
# The algorithm should follow the lecture pattern:
# 1. Set low = 0
# 2. Set high = len(list) - 1
# 3. While low <= high:
#       mid = (low + high) // 2
#       compare the name at mid with the target name
# 4. If equal, return the contact
# 5. If target is smaller, search left half
# 6. If target is larger, search right half
# 7. If not found, return None
#
# This function will be used after quick_sort() to perform efficient searching.
def binary_search(contacts, target_id):
    low = 0
    high = len(contacts) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_id = contacts[mid][0]
        if mid_id == target_id:
            return contacts[mid]
        elif mid_id < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return None

def find_contact_by_id(contacts_list, target_id):
    return binary_search(contacts_list, target_id)


# --- ROUTES ---

@app.route('/')
def index():
    """
    Displays the main page.
    Eventually, students will pass their Linked List or Tree data here.
    """
    # Change Flask HTMLtitle to my name
    app.config['FLASK_TITLE'] = ""

    # Calculate elapsed time since app start
    elapsed_time = time.time() - start_time

    # Use QuickSort to display contacts alphabetically on the main page.
    # Convert the LinkedList into a Python list using contacts.to_list(),
    # then sort the list using quick_sort() before rendering the template.
    contact_list = contacts.to_list()    
    contact_list = quick_sort(contact_list)
    
    return render_template('index.html', 
                         contacts=contact_list, 
                         title=app.config['FLASK_TITLE'],
                         elapsed_time=elapsed_time,
                         search_result=None,
                         search_query=None
                         )

@app.route('/add', methods=['POST'])
# Any time the user performs a new operation (add/delete), clear the redo queue.
# This prevents redoing states that no longer make sense after new edits.
# Replace any redo_stack.clear() calls with redo_queue.clear().
def add_contact():
    """
    Endpoint to add a new contact.
    Students will update this to insert into their Data Structure.
    """
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    # TODO: Before modifying the linked list, push current state to undo_stack and clear redo_stack
    undo_stack.append(contacts.to_list())
    redo_queue.clear()
    
    # Phase 1 Logic: Append to list
    #contacts.append([name, email])
    # Phase 2 Logic: Append to linked list and update hash index
    global next_contact_id
    new_contact = [next_contact_id, name, email]
    contacts.append(new_contact)
    contact_dict[name.lower()] = new_contact
    next_contact_id += 1
    
    return redirect(url_for('index'))


# Create a flask route for deleting a contact that:
# 1. Gets the name of the contact to delete from the form
# 2. Find the full contact using hash table
# 3. Save current state to undo_stack and clear redo_stack
# 4. Deletes the contact from the linked list and hash table
# Any time the user performs a new operation (add/delete), clear the redo queue.
# This prevents redoing states that no longer make sense after new edits.
# Replace any redo_stack.clear() calls with redo_queue.clear().
@app.route('/delete', methods=['POST'])
def delete_contact():

    contact_id = int(request.form.get('id'))

    # find the contact with matching ID
    contact = None
    current = contacts.head

    while current:
        if current.data[0] == contact_id:
            contact = current.data
            break
        current = current.next

    if contact:
        undo_stack.append(contacts.to_list())
        redo_queue.clear()

        contacts.delete(contact)

        # remove from hash table using name
        contact_dict.pop(contact[1].lower(), None)

    return redirect(url_for('index'))

# Replace the current hash-table search with QuickSort + Binary Search.
# The search process should follow these steps:
# 1. Convert the LinkedList of contacts into a Python list using contacts.to_list().
# 2. Sort the list alphabetically using quick_sort().
# 3. Use binary_search() to locate the target contact.
# 4. Return the found contact (or None if not found).
# 5. Render the sorted list so the UI displays contacts in alphabetical order.
@app.route('/search')
def search_contact():
    query = request.args.get('query', '').strip()
    result = None

    # Step 1: Convert LinkedList to Python list
    contact_list = contacts.to_list()

    # Step 2: Sort using QuickSort
    sorted_contacts = quick_sort(contact_list)

    # Step 3: Binary search
    if query:
        result = find_contact_by_id(sorted_contacts, int(query))

    return render_template(
        'index.html',
        contacts=sorted_contacts,
        title=app.config['FLASK_TITLE'],
        elapsed_time=time.time() - start_time,
        search_result=result,
        search_query=query
    )   
 
# Create a flask route for undo operation that:
# Restores the most recent state from undo_stack
# Saves the current sate to redo_queue
# Redirects back to index page
# Update undo() to use redo_queue (FIFO):
# - If undo_stack is not empty, enqueue the current contacts snapshot onto redo_queue
# - Pop the last snapshot from undo_stack and restore it into the linked list
# - Rebuild the hash table index (contact_dict) after restoring
@app.route('/undo', methods=['POST'])
def undo():
    if undo_stack:
        # Save current state to redo queue (FIFO)
        redo_queue.append(contacts.to_list())

        # Restore last state from undo stack (LIFO)
        last_state = undo_stack.pop()
        contacts.from_list(last_state)

        # Rebuild hash index after undo
        contact_dict.clear()
        current = contacts.head
        while current:
            name = current.data[1].lower()
            contact_dict[name] = current.data
            current = current.next

    return redirect(url_for('index'))

# Create a flask route for redo operation that:
# Restores the most recent state from redo_queue
# Saves the current sate to undo_stack
# Redirects back to index page
# Update redo() to use redo_queue (FIFO):
# - If redo_queue is not empty, push the current contacts snapshot onto undo_stack
# - Dequeue (popleft) the oldest snapshot from redo_queue and restore it
# - Rebuild the hash table index (contact_dict) after restoring
@app.route('/redo', methods=['POST'])
def redo():
    if redo_queue:
        # Save current state to undo stack
        undo_stack.append(contacts.to_list())

        # Restore the oldest undone state (FIFO)
        next_state = redo_queue.popleft()
        contacts.from_list(next_state)

        # Rebuild hash index after redo
        contact_dict.clear()
        current = contacts.head
        while current:
            name = current.data[1].lower()
            contact_dict[name] = current.data
            current = current.next

    return redirect(url_for('index'))

# Create a Flask route that runs the search benchmark using the
# run_benchmark() function from benchmark.py. The results should
# be returned to the index template so they can be displayed in
# the GUI as a benchmark table.
@app.route('/benchmark', methods=['POST'])
def benchmark():

    results = run_benchmark()

    contact_list = contacts.to_list()
    contact_list = quick_sort(contact_list)

    return render_template(
        'index.html',
        contacts=contact_list,
        title=app.config['FLASK_TITLE'],
        elapsed_time=time.time() - start_time,
        search_result=None,
        search_query=None,
        benchmark_results=results
    )



# --- DATABASE CONNECTIVITY (For later phases) ---
# Placeholders for students to fill in during Sessions 5 and 27
def get_postgres_connection():
    pass

def get_mssql_connection():
    pass

if __name__ == '__main__':
    # Run the Flask app on port 5000, accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)
