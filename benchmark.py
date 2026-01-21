# import time and create a start timer
import time
start_time = time.time()
n = 1000000
for index in range(n):
    pass
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Look of {n} iterations took {elapsed_time} seconds")
