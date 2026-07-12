import time
# 1. Decorators
# define a decorator function
def my_decorator(fn):
    def wrapper():
        print("Before the call!")
        fn() # this represents the function that is being decorated
        print("After the fn call!")
    return wrapper

# Apply the decorator function to a function using the @ symbol
@my_decorator
def hello_wrapper():
    print("Hello Wrap!")


# 2. Map function 
numbers = [1, 2, 3, 4, 5]
squared_number = list(map(lambda x: x**2, numbers))
# squared_numbers = [x**2 for x in numbers]

# 3. Filter function 
# Filter even numbers from the list after squaring them
even_squared_numbers = list(filter(lambda x: x % 2 == 0, map(lambda x: x**2, numbers)))



# 4 Sorted function
list_of_names = ["John", "Alice", "Bob", "Eve"]
sorted_names = sorted(list_of_names, key=lambda name: name.lower())

# sort based on the length of the name
sorted_names_by_length = sorted(list_of_names, key=lambda name: len(name))


# Lambda function
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x**2, numbers))


# 5 Generator function

def my_number_generator(number):
    for i in range(number+1):
        yield i










# Range, Arrays, Iterators, Modules, Dates, Math, JSON, RegEx, PIP
if __name__ == "__main__":
    # hello_wrapper()
    # print(f"squared numbers {numbers}: {squared_number}")
    # print(squared_number)
    # print("sorted names:", sorted_names)
    # print("sorted names by length:", sorted_names_by_length)
    
    # generator function
    for i in my_number_generator(10):
        print(i)
        time.sleep(1)  # sleep for 1 second between each number