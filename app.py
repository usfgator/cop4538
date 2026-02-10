from flask import Flask, render_template, request, redirect, url_for
import os
import time

app = Flask(__name__)

app.config['FLASK_TITLE'] = ""
 
# Record the start time when the app starts
start_time = time.time()

# Implement undo/redo using two stacks
# undo_stack stores snapshots of the contact list before each operation
# redo_stack stores snapshots of the contact list that were undone  
# Each snapshot must be a python list of contacts (name, email)
undo_stack = []
redo_stack = []

# Create a hash table (dictionary) to store contacts for O(1) search by name
# The key will be the contact name (lowercased for case-insensitive search)
contact_dict = {}


# --- IN-MEMORY DATA STRUCTURES (Students will modify this area) ---
# Phase 1: A simple Python List to store contacts
#contacts = [
#    ['alice', 'alice@example.com'],
#    ['bob', 'bob@example.com']
#]


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
            if current.data[0].lower() == name.lower():
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

# Initialize linked list with sample contacts   
 
contacts = LinkedList()
contacts.append(['Alice', 'alice@example.com'])
contacts.append(['Bob', 'bob@example.com'])

# Build hash index from linked list for O(1) search
current = contacts.head 
while current:
    name = current.data[0].lower()
    contact_dict[name] = current.data
    current = current.next



# --- ROUTES ---

@app.route('/')
def index():
    """
    Displays the main page.
    Eventually, students will pass their Linked List or Tree data here.
    """
    # Change Flask HTMLtitle to my name
    app.config['FLASK_TITLE'] = "Harrison's Contact List"

    # Calculate elapsed time since app start
    elapsed_time = time.time() - start_time
    # Convert linked list to a list for rendering
    contact_list = []
    current = contacts.head
    while current:
        contact_list.append(current.data)
        current = current.next
    

    return render_template('index.html', 
                         contacts=contact_list, 
                         title=app.config['FLASK_TITLE'],
                         elapsed_time=elapsed_time,
                         search_result=None,
                         search_query=None
                         )

@app.route('/add', methods=['POST'])
def add_contact():
    """
    Endpoint to add a new contact.
    Students will update this to insert into their Data Structure.
    """
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    # TODO: Before modifying the linked list, push current state to undo_stack and clear redo_stack
    undo_stack.append(contacts.to_list())
    redo_stack.clear()
    
    # Phase 1 Logic: Append to list
    #contacts.append([name, email])
    # Phase 2 Logic: Append to linked list and update hash index
    new_contact = [name, email]
    contacts.append(new_contact)
    contact_dict[name.lower()] = new_contact
    
    
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
# Create a flask route for deleting a contact that:
# 1. Gets the name of the contact to delete from the form
# 2. Find the full contact using hash table
# 3. Save current state to undo_stack and clear redo_stack
# 4. Deletes the contact from the linked list and hash table
def delete_contact():
    name = request.form.get('name', '').strip()
    contact = contact_dict.get(name.lower())
    if contact:
        undo_stack.append(contacts.to_list())
        redo_stack.clear()
        contacts.delete(contact)
        contact_dict.pop(name.lower(), None)
    return redirect(url_for('index'))


@app.route('/search')
def search_contact():
    query = request.args.get('query', '').strip()
    result = None
        
    # Phase 2 Logic: Search in linked list
    if query:
        result = contact_dict.get(query.lower())
    
    # Convert linked list to a list for rendering
    contact_list = []
    current = contacts.head
    while current:
        contact_list.append(current.data)
        current = current.next
    return render_template('index.html', 
                         contacts=contact_list, 
                         title=app.config['FLASK_TITLE'],
                         elapsed_time=time.time() - start_time,
                         search_result=result,
                         search_query=query
                        )

    
    # Phase 1 Logic: Search in list
    #def find(query):
    #    for contact in contacts:
    #        if contact[0].lower() == query.lower():
    #            return contact
    #    return None
    #result = find(query)

    
    #return render_template('index.html', 
    #                     contacts=contacts, 
    #                     title=app.config['FLASK_TITLE'],
    #                     elapsed_time=time.time() - start_time,
    #                     search_result=result)



# Create a flask route for undo operation that:
# Restores the most recent state from undo_stack
# Saves the current sate to redo_stack
# Redirects back to index page
@app.route('/undo', methods=['POST'])
def undo():
    if undo_stack:
        # Save current state to redo stack
        redo_stack.append(contacts.to_list())
        # Restore last state from undo stack
        last_state = undo_stack.pop()
        contacts.from_list(last_state)
        # Rebuild hash index after undo
        contact_dict.clear()
        current = contacts.head
        while current:
            name = current.data[0].lower()
            contact_dict[name] = current.data
            current = current.next
    return redirect(url_for('index'))

# Create a flask route for redo operation that:
# Restores the most recent state from redo_stack
# Saves the current sate to undo_stack
# Redirects back to index page
@app.route('/redo', methods=['POST'])
def redo():
    if redo_stack:
        # Save current state to undo stack
        undo_stack.append(contacts.to_list())
        # Restore last state from redo stack
        last_state = redo_stack.pop()
        contacts.from_list(last_state)
        # Rebuild hash index after redo
        contact_dict.clear()
        current = contacts.head
        while current:
            name = current.data[0].lower()
            contact_dict[name] = current.data
            current = current.next
    return redirect(url_for('index'))


# --- DATABASE CONNECTIVITY (For later phases) ---
# Placeholders for students to fill in during Sessions 5 and 27
def get_postgres_connection():
    pass

def get_mssql_connection():
    pass

if __name__ == '__main__':
    # Run the Flask app on port 5000, accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)
