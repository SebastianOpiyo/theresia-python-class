'''
1. Ask the user for their name, age and country
2. Create a function that takes the name, age and country as parameters and prints them in a formatted string
'''

x = 20  # global variable


def check_scope():
    global y
    y = 24
    print(f"X is a global variable with value {x}")



def check_scope2():
    print(f"Y is a local variable with value {y}")


def collect_user_info():
    print("Please enter your information below.\n")
    name = input("Please enter your name: ")
    age = int(input("Please enter your age: "))
    country = input("Please enter your country: ")
    return name, age, country

def print_user_info():
    name, age, country = collect_user_info()
    print("\nUser Information")
    print(f"Hello {name}, you are {age} years old and you are from {country}.")


# What is nonloacal
# Python decorators & their use cases



# Scope

if __name__ == "__main__":
    # call the function
    # print_user_info()
    # check_scope()
    # check_scope2()
    check_scope()
    check_scope2()
    