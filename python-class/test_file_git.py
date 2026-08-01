class Car:
    def __init__(self,make:str,colour:str, year:int):
        self.make=make
        self.colour=colour
        self.year=year
    def identify (self):
        print(f"This car is {self.make},with {self.colour} colour.Made in the year {self.year}")
        return

Car_No1=Car("Toyota","Red",2020)
Car_No2=Car("Honda","black",2023)

if __name__=="__main__":
    print(Car_No1.identify())
    print(Car_No2.identify())
