import functions_class as fc # import of a module example
import numpy as np

# fc.print_user_info()



# decorator function

def my_decorator_func(func):
    def wrapper():
        print("Before the function is called.")
        func()
        print("After the function is called.")
    return wrapper

@my_decorator_func
def my_function():
    print("Inside the function.")


my_function()