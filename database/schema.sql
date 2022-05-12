-- The cars table stores all of the information on a car collected using the DLVA VES API
CREATE TABLE Cars
(
    ID TEXT,
    plate TEXT, -- License plate number
    recorded_datetime INT, -- Date and time plate was recorded UNIX TIME
    make TEXT, -- make of car
    manufacture_year INT, -- Year of manufacture UNIX TIME
    emissions REAL, -- Emissions g/km
    fuel_type TEXT, -- Car fuel type
    car_location INT, -- Foreign Key of CarLocations record
    FOREIGN KEY (car_location) REFERENCES CarLocations(ID) 
);

-- The location table stores geographical locations of where the data was collected from
CREATE TABLE CarLocations
(
    ID TEXT, 
    lat REAL, -- Location Latitude
    lon REAL, -- Location Longitude
    location_name TEXT, -- Name of location (street name)
    facing TEXT -- Direction camera is facing (N,E,S,W)
);