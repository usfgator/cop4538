from flask import Flask, render_template, request, redirect, url_for
import os
import time

app = Flask(__name__)

app.config['FLASK_TITLE'] = ""
 
# Record the start time when the app starts
start_time = time.time()

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
# Initialize linked list with sample contacts   
 
contacts = LinkedList()
contacts.append(['Alice', 'alice@example.com'])
contacts.append(['Bob', 'bob@example.com'])



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
                         search_result=None
                         )

@app.route('/add', methods=['POST'])
def add_contact():
    """
    Endpoint to add a new contact.
    Students will update this to insert into their Data Structure.
    """
    name = request.form.get('name')
    email = request.form.get('email')
    
    # Phase 1 Logic: Append to list
    contacts.append([name, email])
    
    return redirect(url_for('index'))

@app.route('/search')
def search_contact():
    query = request.args.get('query', '').strip()
    result = None
        
    # Phase 2 Logic: Search in linked list
    if query:
        result = contacts.find_by_name(query)
    
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




# --- DATABASE CONNECTIVITY (For later phases) ---
# Placeholders for students to fill in during Sessions 5 and 27
def get_postgres_connection():
    pass

def get_mssql_connection():
    pass

if __name__ == '__main__':
    # Run the Flask app on port 5000, accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)
