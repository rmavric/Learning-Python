from vehicle import Vehicle

class Bus(Vehicle):
    def __init__(self, starting_top_speed=100):  # bus has it's own constructor because it has one extra property
        super().__init__(starting_top_speed)     # but with that constructor we have overwritten constructor from vehicle
                                                 # so now we don't have __warning set to []
                                                 # we have to call parent constructor of the base class and that is super
                                                 # now we get attributes that are defined in base class


        self.passengers = []

    def add_group(self, passengers):
        self.passengers.extend(passengers)

bus1 = Bus(150)
bus1.add_warning('Test')
bus1.add_group(['Max', 'Manuel', 'Anna'])
print(bus1.passengers)
bus1.drive()