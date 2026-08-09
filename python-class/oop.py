"""
PROGRAMMING PARADIGMS
1. Functional Programming (Python, javascript) | Pure Functional Programming (Haskell, Golang/Go, Rust, )
2. Object Oriented Programming (OOP) -- C++, Python, Java, Javascript etc
"""

# Encapsulation - 
# Polymorphism





# Classes
class Vehicle:
     
     company_name = "TOYOTA" # An example of a class attribute

     def __init__(self, color:str,number_tires:int , engine:str):
          self.color = color
          self.num_tires = number_tires
          self.__engine = engine # Private attribute
          self.fuel_type = None

     def driving(self):
          print(f"Driving")
    
     def fuel(self, fuel_type:str):
          self.fuel_type = fuel_type
          return self.fuel_type

     def __engine_type(self):
          """This is a private method that is only accessible inside this class
          It cannot be called outside or reused by another child class"""
          print(f"The engine type is:{self.__engine}")

     def get_engine_type(self):
          return self.__engine_type()

          

# instantiate
sample_car = Vehicle("red",4,"2000cc")  # An instance of a vehicle in the name of a car
sample_lorry = Vehicle("white",8,"3500cc")



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
          
class Aeroplane(Vehicle):

     def __init__(self, color, year, make):
          self.color = color # An example of an instance attribute
          self.year = year
          self.make = make

     def driving(self):
          return "Flying"


toyota_car = Car("red", 2020, "Toyota")
suzuki_car = Car("blue", 2021, "Suzuki")
jet = Aeroplane("blue", 2022, "Boeng")






if __name__ == "__main__":
     # print(sample_car._engine)
     # print(sample_car.get_engine_type())
     # print(toyota_car.__engine_type())  # This should throw an error because the method is a private method in the parent class
#   print(suzuki_car.location_of_manufacture) 
    # This will raise an error because car_number is not defined in this scope
    print(jet.driving())


