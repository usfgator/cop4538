# Create a benchmarking module that compares Linear Search and Binary Search
# performance when searching for contacts in a list.
#
# This module will be used by a Flask web application, so the benchmark must
# return results instead of printing them.
#
# The module should:
# 1. Generate a list of contacts with random names and emails.
# 2. Implement a linear search that scans the list sequentially.
# 3. Sort the contacts using the existing quick_sort() algorithm.
# 4. Implement binary search to locate a target contact in the sorted list.
# 5. Measure the execution time for both search methods using time.perf_counter().
# 6. Test multiple dataset sizes (ex: 1000, 10000, 50000 contacts).
# 7. Repeat searches multiple times to produce reliable timing results.
# 8. Return the results as a list of dictionaries formatted like:
#
#    [
#        {"size": 1000, "linear": 0.0021, "binary": 0.0003},
#        {"size": 10000, "linear": 0.0213, "binary": 0.0004},
#        {"size": 50000, "linear": 0.1090, "binary": 0.0005}
#    ]
#
# The results will be displayed in the Flask GUI as a benchmark table.
#
# This benchmark demonstrates the algorithmic difference between:
# Linear Search  -> O(n)
# Binary Search  -> O(log n)
#
# The module must expose a function called run_benchmark()
# that returns the benchmark results.
import random
import string
import time


def quick_sort(contacts):

    if len(contacts) <= 1:
        return contacts

    pivot = contacts[len(contacts)//2][0].lower()

    left = [x for x in contacts if x[0].lower() < pivot]
    middle = [x for x in contacts if x[0].lower() == pivot]
    right = [x for x in contacts if x[0].lower() > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def generate_random_contacts(n):

    contacts = []

    for _ in range(n):

        name = ''.join(random.choices(string.ascii_letters, k=8))
        email = name.lower() + "@example.com"

        contacts.append([name, email])

    return contacts


def linear_search(contacts, target_name):

    for contact in contacts:

        if contact[0] == target_name:
            return contact

    return None


def binary_search(contacts, target_name):

    low = 0
    high = len(contacts) - 1

    while low <= high:

        mid = (low + high)//2
        mid_name = contacts[mid][0]

        if mid_name == target_name:
            return contacts[mid]

        elif mid_name < target_name:
            low = mid + 1

        else:
            high = mid - 1

    return None

def run_benchmark():

    results = []

    dataset_sizes = [1000, 10000, 50000]
    trials = 1000

    for size in dataset_sizes:

        contacts = generate_random_contacts(size)

        target = random.choice(contacts)[0]

        sorted_contacts = quick_sort(contacts)

        # -------- Linear Search Benchmark --------

        start = time.perf_counter()

        for _ in range(trials):
            linear_search(contacts, target)

        linear_time = (time.perf_counter() - start) / trials


        # -------- Binary Search Benchmark --------

        start = time.perf_counter()

        for _ in range(trials):
            binary_search(sorted_contacts, target)

        binary_time = (time.perf_counter() - start) / trials


        results.append({
            "size": size,
            "linear": linear_time,
            "binary": binary_time
        })

    return results


    