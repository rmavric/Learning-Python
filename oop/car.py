from vehicle import Vehicle     # Car inherits from Vehicle so we need to import it

class Car(Vehicle):         # in parantheses we need to define class from that we want to inherit
    # top_speed = 100
    # warnings = []

    """
    def __init__(self, starting_top_speed=100):     #special method, built in method, this is a constructor to a class, dunder methods/functions
                                                    #self argument is automatically passed by python
                                                    #we can add additional argument depending what we want to set
        self.top_speed = starting_top_speed
        #self.warnings = []          #this is public variable
        self.__warnings = []        #those underscores tell python that this is private variable
                                    #it can be accessed from isnide the class, not outside
                                    #but it is not the rule it's only convention, but python will give us a sign 



    def __repr__(self):     #for all methods of our class we need to put in self argument
        print('Printing...')
        return 'Top Speed: {}, Warnings: {}'.format(self.top_speed, len(self.__warnings))   # __repr__ needs to return something
                                                                                            # it returns what should be output


    
    def add_warning(self, warning_text):
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)



    def get_warnings(self):
        return self.__warnings
    """  


    def brag(self):
        print('Look how cool my car is!')


car1 = Car()
car1.drive()

# Car.top_speed = 200
car1.add_warning('New warning')         #this is attribute
# car1.__warnings.append([])
# print(car1.__dict__)                  #this prints out object as a dictionary
print(car1)                             #this prints out object but like address in memory 
                                        #car1.__dict__ => if we edit this dictionary we won't edit car1 object because
                                        #car1.__dict__ is only a snapshot of car1 instance




car2 = Car(200)
car2.drive()
print(car2.get_warnings())





car3 = Car(250)
car3.drive()
print(car3.get_warnings())




"""
__init__()  => constructor

__str__()  => string output

__repr__()  => general output, what we want to output => it will be called when we print our object

__dict__  => converts to dictionary
"""