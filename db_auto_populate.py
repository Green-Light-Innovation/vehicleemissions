import random
import string
import datetime

from database.objects.car import Car
from database.objects.carlocation import CarLocation

# Locations
locations = [
    "Curzon Street",
    "Bull Street",
    "Corporation Street",
    "Upper Trinity Street",
    "Lower Trinity Street",
    "New Street",
    "Moor Street",
]

car_makes = [
    "Vauxhall",
    "Ford",
    "Fiat",
    "Mini",
    "Honda",
    "Land Rover"
]

def gen_plate_number() -> str:
    plate = ""
    for x in range(6):
        plate += random.choice(list(string.ascii_uppercase + string.digits))
    return plate

def gen_random_time() -> datetime.time:
    return datetime.time(
        random.randint(0, 23), # hour
        random.randint(0, 59), # minute
        random.randint(0, 59), # second
        0 # micro second
    )

# Create 3 - 5 different locations
for x in range(random.randint(3,5)):
    
    # gen random date
    date = datetime.date.fromisocalendar(
        2022,
        random.randint(1, 51), # Random week
        random.randint(1, 7) # Random day
    )
    
    location = CarLocation(
        None,
        float(random.randint(-70, 70)),
        float(random.randint(-70, 70)),
        random.choice(locations),
        random.choice(["N","S","E","W"])
    )
    location.save_to_database()

    

    # Create 50 - 100 cars
    for y in range(random.randint(50,100)):

        car = Car(
            None,
            gen_plate_number(),
            (datetime.datetime.combine(date, gen_random_time())).timestamp(),
            random.choice(car_makes),
            random.randint(2001, 2019),
            random.randint(50,200),
            random.choice(["PETROL", "DIESEL"]),
            random.randint(2022,2023),
            location.get_ID()
        )
        car.save_to_database()