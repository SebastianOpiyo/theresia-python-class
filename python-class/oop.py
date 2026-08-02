"""
PROGRAMMING PARADIGMS
1. Functional Programming (Python, javascript) | Pure Functional Programming (Haskell, Golang/Go, Rust, )
2. Object Oriented Programming (OOP) -- C++, Python, Java, Javascript etc
"""

# Classes
class Vehicle:
     
     company_name = "TOYOTA" # An example of a class attribute

     def __init__(self, color:str,number_tires:int , engine:str):
          self.color = color
          self.num_tires = number_tires
          self.engine = engine
          self.fuel_type = None

     def drive(self):
          print(f"Driving")
    
     def fuel(self, fuel_type:str):
          self.fuel_type = fuel_type
          return self.fuel_type
          

# instantiate
Car = Vehicle("red",4,"2000cc")  # An instance of a vehicle in the name of a car
Lorry = Vehicle("white",8,"3500cc")


# DAY 2 ON CLASSES AND OBJECTS

class Car(Vehicle):

     location_of_manufacture = "Japan" # An example of a class attribute

     def __init__(self, color:str, year:int, make:str):
          self.color = color # An example of an instance attribute
          self.year = year
          self.make = make

     def define(self):
          # print(f"The car is a {self.color}, manufactured in the year {self.year} and its make is {self.make} and its fuel is {self.fuel("Diesel")}")
          print(f"The Company name is {self.company_name}\nAnd the location of manufacturing is {self.location_of_manufacture}")



toyota_car = Car("red", 2020, "Toyota")
suzuki_car = Car("blue", 2021, "Suzuki")

































if __name__ == "__main__":
    print(toyota_car.define()) 
#   print(suzuki_car.location_of_manufacture) 
    # This will raise an error because car_number is not defined in this scope


