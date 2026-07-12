# Loops
# Types of Loops
'''
1. If ...elif,else
2. While
3. For Loop
4. Match/Case
'''

# Boolean --> a==b, a!=b, a<b, a<= b, a>b

'''
age = 15
name = "Bob"

if age > 18: # Execute to True
    print(f"Entry allowed")
elif age < 18 and age > 15:
    print(f"You still a teenager")
elif age < 15 or name == "Bob":
    print("You are the only allowed teenager!")
else:
    pass

# if age < 18:print("You are young")
# else:print("You are allowed")

# Short hand method # List compression operation
# print(f"A") if a > b else print(f"B") 

'''

# For Loop

example_string = "Hello World"
list_example = [1,2,3,4,5,6,7,8,9]

'''
for l in example_string: # iterates through anything that is iterable
    print(l) 
    for i in list_example:
        print(i)

'''

# While Loop
'''
count = 0

while count < 10:
    print(f'the count is {count}')
    count += 1 # count = count + 1
'''



# Match Expression
day=int(input(f"Please enter the day of the week: "))

# match day:
#     case 1:print("Monday")
#     case 2:print("Tuesday")
#     case 3:print("Wednesday")
#     case 4:print("Thursday")
#     case 5:print("Friday")
#     case 6:print("Saturday")
#     case 7:print("Sunday")


def day_checker(day:int) -> None:
    match day:
        case 1:print("Monday")
        case 2:print("Tuesday")
        case 3:print("Wednesday")
        case 4:print("Thursday")
        case 5:print("Friday")
        case 6:print("Saturday")
        case 7:print("Sunday")
    


# Calling the function

# day_checker(day)

def print_name(school:str, year:int, name="Sebastian"):
    print(f"My name is {name}, I was born in the year {year} and I study at {school}")

# print_name("Nyerere", 2024)

def positional_only_parameters(name, /, age, city="Dar es Salaam"):
    print(f"My name is {name} and I am {age} years old my city is {city}")

# positional_only_parameters("Sebastian", 20, "Dodoma")

def keyword_only_parameters(*, name:str):
    print(f"My name is {name}")

# keyword_only_parameters(name="Sebastian")

def pass_many_parameters(*args, **kwargs):
    print(f"Positional arguments: {args}")
    print(f"Keyword arguments: {kwargs}")

pass_many_parameters(1,2,3,4,5, name="Sebastian", age=20, city="Dar es Salaam")

# Differentiate between a parameter and an argument
