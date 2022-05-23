-- The cars table stores all of the information on a car collected using the DLVA VES API
CREATE TABLE `Cars` (
  `ID` VARCHAR(32) NOT NULL,
  `plate` VARCHAR(16) NULL,
  `recorded_datetime` INT UNSIGNED NULL,
  `make` VARCHAR(255) NULL,
  `manufacture_year` INT UNSIGNED NULL,
  `emissions` REAL UNSIGNED NULL,
  `fuel_type` VARCHAR(255) NULL,
  `car_location` VARCHAR(32) NULL,
  PRIMARY KEY (`ID`));

-- The location table stores geographical locations of where the data was collected from
CREATE TABLE `CarLocations` (
  `ID` VARCHAR(32) NOT NULL,
  `lat` FLOAT NULL,
  `lon` FLOAT NULL,
  `location_name` VARCHAR(255) NULL,
  `facing` VARCHAR(2) NULL,
  PRIMARY KEY (`ID`));

CREATE TABLE `NodeConfig` (
  `ID` VARCHAR(32),
  `location_id` VARCHAR(32),
  `friendly_name` VARCHAR(32)
);