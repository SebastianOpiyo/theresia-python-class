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

     def drive(self):
          print(f"Driving")
    
     def fuel(self):
          print(f"fueling")

    

    


# instantiate
Car = Vehicle("red",4,"2000cc")  # An instance of a vehicle in the name of a car
Lorry = Vehicle("white",8,"3500cc")

if __name__ == "__main__": 
    #  print(type(Car))
    # print(f"The color if the car is {Car.color}")
    # Car.drive()
    Car.fuel()
    # print(f"The engine size of the lorry is {Lorry.engine}")
    #  print(type(Lorry))


