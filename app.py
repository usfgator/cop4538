from collections import deque
from benchmark import run_benchmark
from flask import Flask, render_template, request, redirect, url_for
import time
import heapq

app = Flask(__name__)
app.config['FLASK_TITLE'] = ""

start_time = time.time()

# Initial data structures for undo/redo
undo_stack = []
redo_queue = deque()

# Hash table for O(1) lookups
contact_dict = {}
next_contact_id = 3

# Copilot Prompt:
# Create a Node class for a singly linked list to store contacts.
# Each node should store contact data (id, name, email, category)
# and a reference to the next node in the list.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
# Copilot Prompt:
# Implement a singly linked list to store contacts.
# Each contact should be stored as [id, name, email, category].
# Include methods for append, delete by ID, traversal, and conversion to/from a Python list.
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
        prev = None
        while temp:
            if temp.data[0] == key[0]:
                if prev:
                    prev.next = temp.next
                else:
                    self.head = temp.next
                return
            prev = temp
            temp = temp.next

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


contacts = LinkedList()
contacts.append([1, 'Alice', 'alice@example.com', 'Personal'])
contacts.append([2, 'Bob', 'bob@example.com', 'Work'])

# Copilot Prompt:
# Use a Python dictionary as a hash table to map contact IDs to contact records.
# This enables O(1) lookup when retrieving or deleting contacts.
current = contacts.head
while current:
    contact_dict[current.data[0]] = current.data
    current = current.next


# Copilot Prompt:
# Implement QuickSort to sort contacts by ID.
# Use a divide-and-conquer approach with a pivot,
# and recursively sort left and right partitions.
def quick_sort(data):
    if len(data) <= 1:
        return data
    pivot = data[len(data)//2][0]
    left = [x for x in data if x[0] < pivot]
    mid = [x for x in data if x[0] == pivot]
    right = [x for x in data if x[0] > pivot]
    return quick_sort(left) + mid + quick_sort(right)

# Copilot Prompt:
# Implement binary search to efficiently find a contact by ID
# in a sorted list of contacts.
# The function should return the matching contact or None.
def binary_search(data, target):
    low, high = 0, len(data)-1
    while low <= high:
        mid = (low + high)//2
        if data[mid][0] == target:
            return data[mid]
        elif data[mid][0] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

def find_contact_by_id(data, target):
    return binary_search(data, target)

# Copilot Prompt:
# Create a TreeNode class to represent hierarchical categories.
# Each node should store a category name, a list of contacts,
# and references to child categories.
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.contacts = []

    def add_child(self, node):
        self.children.append(node)

    def add_contact(self, contact):
        if not any(c[0] == contact[0] for c in self.contacts):
            self.contacts.append(contact)

    def remove_contact(self, contact):
        self.contacts = [c for c in self.contacts if c[0] != contact[0]]

    def clear_contacts_recursive(self):
        self.contacts = []
        for child in self.children:
            child.clear_contacts_recursive()

    def find(self, value):
        if self.value.lower() == value.lower():
            return self
        for child in self.children:
            result = child.find(value)
            if result:
                return result
        return None

# Copilot Prompt:
# Implement a CategoryTree class with a root node called "Contacts".
# Provide methods to find categories recursively and add new categories
# under a given parent node.
class CategoryTree:
    def __init__(self):
        self.root = TreeNode("Contacts")

    def get_category(self, name):
        return self.root.find(name)

    def add_category(self, parent, name):
        parent_node = self.get_category(parent)
        if not parent_node:
            return None
        node = TreeNode(name)
        parent_node.add_child(node)
        return node


# Copilot Prompt:
# Create a BSTNode class to store category names as keys
# and references to TreeNode objects as values.
# Each node should support left and right children.
class BSTNode:
    def __init__(self, key, value):
        self.key = key.lower()
        self.value = value
        self.left = None
        self.right = None

    def insert(self, key, value):
        key = key.lower()
        if key < self.key:
            if self.left:
                self.left.insert(key, value)
            else:
                self.left = BSTNode(key, value)
        elif key > self.key:
            if self.right:
                self.right.insert(key, value)
            else:
                self.right = BSTNode(key, value)

    def search(self, key):
        key = key.lower()
        if key == self.key:
            return self.value
        elif key < self.key and self.left:
            return self.left.search(key)
        elif key > self.key and self.right:
            return self.right.search(key)
        return None

# Copilot Prompt:
# Implement a Binary Search Tree (BST) for category lookup.
# Include insert and search operations to achieve O(log n) access time.
class CategoryBST:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if not self.root:
            self.root = BSTNode(key, value)
        else:
            self.root.insert(key, value)

    def search(self, key):
        if not self.root:
            return None
        return self.root.search(key)


# Copilot Prompt:
# Implement a priority queue using Python's heapq module.
# Store VIP contacts with priority values so that higher priority
# contacts are retrieved first (use negative values for max-heap behavior).
class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, contact_id, priority):
        heapq.heappush(self.heap, (-priority, contact_id))

    def remove(self, contact_id):
        self.heap = [item for item in self.heap if item[1] != contact_id]
        heapq.heapify(self.heap)

    def clear(self):
        self.heap = []

    def get_all_ids(self):
        return [cid for _, cid in self.heap]


# Initialize data structures
category_tree = CategoryTree()
category_bst = CategoryBST()
vip_heap = MaxHeap()

for cat in ["Work", "Personal"]:
    node = category_tree.add_category("Contacts", cat)
    category_bst.insert(cat, node)




# Helper function to rebuild all derived data structures (hash table, tree, heap)
# from the linked list to ensure consistency after updates, undo, and redo operations.

vip_priority_map = {}

def rebuild_hash_table():
    contact_dict.clear()
    current = contacts.head
    while current:
        contact_dict[current.data[0]] = current.data
        current = current.next

# Copilot Prompt:
# Rebuild all derived data structures (hash table, tree, heap)
# from the linked list to ensure consistency after updates,
# undo, and redo operations.
def rebuild_all_structures():
    rebuild_hash_table()

    # Clear tree
    category_tree.root.clear_contacts_recursive()

    # Rebuild tree
    current = contacts.head
    while current:
        c = current.data
        node = category_tree.get_category(c[3])
        if node:
            node.add_contact(c)
        current = current.next

    # Rebuild heap
    vip_heap.clear()
    for cid, p in vip_priority_map.items():
        vip_heap.insert(cid, p)


def snapshot_state():
    return {
        "contacts": contacts.to_list(),
        "next_id": next_contact_id,
        "vip": dict(vip_priority_map)
    }


def restore_state(state):
    global next_contact_id, vip_priority_map
    contacts.from_list(state["contacts"])
    next_contact_id = state["next_id"]
    vip_priority_map = dict(state["vip"])
    rebuild_all_structures()



# ROUTES

# Copilot Prompt:
# Display all contacts by converting the linked list into a sorted list using QuickSort.
# Extract VIP contacts using a heap-based priority queue.
# Render both full contact list and VIP subset in the UI.
@app.route('/')
def index():
    contact_list = quick_sort(contacts.to_list())
    vip_ids = set(vip_heap.get_all_ids())
    vip_contacts = [c for c in contact_list if c[0] in vip_ids]

    return render_template(
        'index.html',
        contacts=contact_list,
        vip_contacts=vip_contacts,
        elapsed_time=time.time() - start_time
    )

# Copilot Prompt:
# Add a new contact to the linked list and update the hash table.
# Ensure the category exists using a BST for fast lookup.
# If a priority is assigned, insert the contact into a heap-based VIP structure.
# Rebuild all derived data structures after insertion to maintain consistency.
@app.route('/add', methods=['POST'])
def add_contact():
    global next_contact_id

    name = request.form.get('name', '')
    email = request.form.get('email', '')
    category = request.form.get('category', 'Work').title()

    priority = int(request.form.get('priority') or 0)

    undo_stack.append(snapshot_state())
    redo_queue.clear()

    new_contact = [next_contact_id, name, email, category]
    contacts.append(new_contact)
    contact_dict[new_contact[0]] = new_contact

    # Ensure category exists in BST
    node = category_bst.search(category)
    if not node:
        node = category_tree.add_category("Contacts", category)
        category_bst.insert(category, node)

    if priority > 0:
        vip_priority_map[new_contact[0]] = priority
        vip_heap.insert(new_contact[0], priority)

    next_contact_id += 1

    rebuild_all_structures()

    return redirect(url_for('index'))


# Copilot Prompt:
# Delete a contact from the linked list and hash table using its ID.
# Remove the contact from the VIP heap if applicable.
# Rebuild all data structures to maintain consistency after deletion.
@app.route('/delete', methods=['POST'])
def delete_contact():
    contact_id = int(request.form.get('id', 0))
    contact = contact_dict.get(contact_id)

    if contact:
        undo_stack.append(snapshot_state())
        redo_queue.clear()

        contacts.delete(contact)
        contact_dict.pop(contact_id, None)

        vip_priority_map.pop(contact_id, None)
        vip_heap.remove(contact_id)

        # 🔥 FIX
        rebuild_all_structures()

    return redirect(url_for('index'))

# Copilot Prompt:
# Implement undo functionality using a stack.
# Restore the previous application state and push the current state to the redo queue.
@app.route('/undo', methods=['POST'])
def undo():
    if undo_stack:
        redo_queue.append(snapshot_state())
        restore_state(undo_stack.pop())
    return redirect(url_for('index'))

# Copilot Prompt:
# Implement redo functionality using a queue (FIFO).
# Restore the next available state and push the current state back to the undo stack.
@app.route('/redo', methods=['POST'])
def redo():
    if redo_queue:
        undo_stack.append(snapshot_state())
        restore_state(redo_queue.popleft())
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)