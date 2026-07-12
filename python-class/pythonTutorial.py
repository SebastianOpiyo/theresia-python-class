# Python comment

"""
This is a multi-line comment
Or a block of comment"""

# print("Hello, World!")

# Operations
x = 20
y = 10
# sum = x + y 

# I want to test to use of key word sum
# We dont use keywords as variable names
# print(sum)
# z = sum(x, y) # we have used an inbuilt function "sum"

# print(f"The sum of {x} and {y} is {z}")


# Arithmetic Operators
# Strings, Comments
# Variables, int, float
# Inbuilt methods, functions e.g sum, print

# bool, lists, tuples, sets, dictionaries
# Functions
# Indentation
# loops

# BOOLEANS
# Use of of isinstance() function

# Check if a number is an int
num = "10"
num2 = int(num)

# dict1 = dict()
dict1 = {"kenya":"nairobi", "Tanzania":"Dodoma", "Uganda":"Kampala"}
age = {"Alex":20, "Josh:":20, "Maggie":30}
fruits= set()

# fruits = {"banana", "banana", "orange"}

# Lists
vegetables = ["cabbages", "spinach", "kales", "cabbages"]
# print(len(vegetables))
# print(type(vegetables))

# print(isinstance(dict1, dict))Loops
# print(len(dict1))


# 

# name = "Alex"

# for l in name:
#     print(l)


# for key in dict1:
#     print(f'{key} --> {dict1[key]}')


# Factorial using for loop
'''
number = int(input("Enter a number: "))
factorial = 1

for i in range(1, number + 1):
    factorial *= i  # factorial = factorial * i

print("Factorial of", number, "is", factorial)
'''

def is_prime(num):
    is_prime = True
    if num < 2:
        is_prime = False
    else:
        if num % 2 == 0:
            is_prime = False
    return is_prime




# formalize list

def formalize_list(some_list):
    formalized_list = []

    # max value in given some_list

    # use the max value to divide each elem in the lst

    # append the outcome of the division to the formalized_list

    # return the formalized list



if __name__ == "__main__":
    while True:
        num= int(input("Enter a number to check if its prime: "))
        if is_prime(num):
            print(f"{num} is a prime number")
        else:
            print(f"{num} is not a prime number\n")