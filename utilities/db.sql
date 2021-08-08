DROP DATABASE IF EXISTS `db_fesel`;
CREATE DATABASE IF NOT EXISTS `db_fesel`;
USE `db_fesel`;

/****************************************
 * TABLES CREATION
*****************************************/

CREATE TABLE IF NOT EXISTS `Customer`
(
	`customer_id` INT NOT NULL AUTO_INCREMENT,
	`customer_name` VARCHAR(30) NOT NULL,
	`customer_email` VARCHAR(30),
	`customer_password` VARCHAR(30),
	`customer_phone` VARCHAR(30),
	PRIMARY KEY(`customer_id`)
);

CREATE TABLE IF NOT EXISTS `Contract`
(
	`contract_id` INT NOT NULL AUTO_INCREMENT,
	`contract_start_date` DATETIME NOT NULL,
	`contract_end_date` DATETIME NOT NULL,
	`contract_days` VARCHAR(30),
	`contract_locations` TEXT(500),
	`customer_id` INT NOT NULL,
	FOREIGN KEY (`customer_id`) REFERENCES Customer(`customer_id`),
	PRIMARY KEY (`contract_id`)
);

CREATE TABLE IF NOT EXISTS `Media`
(
	`media_id` INT NOT NULL AUTO_INCREMENT,
	`media_name` VARCHAR(60) NOT NULL,
	`media_gender` TEXT(500),
	`media_age` TEXT(500),
	`media_skin` TEXT(500),
	`contract_id` INT NOT NULL,
	FOREIGN KEY (`contract_id`) REFERENCES Contract(`contract_id`),
	PRIMARY KEY(`media_id`)
);

CREATE TABLE IF NOT EXISTS `Passenger`
(
	`passenger_id` INT NOT NULL AUTO_INCREMENT,
	`passenger_gender` VARCHAR(30),
	`passenger_age` VARCHAR(30),
	`passenger_skin` VARCHAR(30),
	PRIMARY KEY(`passenger_id`)
);

/*CREATE TABLE IF NOT EXISTS `Seenby`
(
	`passenger_id` INT NOT NULL AUTO_INCREMENT,
	`passenger_gender` VARCHAR(30),
	`passenger_age` VARCHAR(30),
	`passenger_skin` VARCHAR(30),
	FOREIGN KEY (`passenger_id`) REFERENCES Passenger(`passenger_id`),
	FOREIGN KEY (`media_id`) REFERENCES Media(`media_id`),
	PRIMARY KEY(`passenger_id`, `media_id`)
);*/


/****************************************
 * DATA INSERTION
*****************************************/

INSERT INTO `Customer`(`customer_name`)
VALUES
	('Elton'),
	('Senelec'),
	('Xelcom');

INSERT INTO `Contract`(`contract_start_date`, `contract_end_date`, `contract_days`, `contract_locations`, `customer_id`)
VALUES
	('2021-07-01 00:00:00', '2022-09-01 00:00:00', '5,6', '', 1),
	('2021-07-01 00:00:00', '2022-09-01 00:00:00', '0,1,2,3,4,5,6', '', 2),
	('2021-07-01 00:00:00', '2022-07-21 00:00:00', '0,1,2,3,4,5,6', '', 1),
	('2021-07-01 00:00:00', '2022-09-01 00:00:00', '0,1,2,3,4,5,6', '', 3),
	('2021-07-01 00:00:00', '2022-09-01 00:00:00', '0,1,2,3,4,5,6', '', 2),
	('2021-07-23 00:00:00', '2022-09-01 00:00:00', '0,1,2,3,5,6', '', 1),
	('2021-07-14 00:00:00', '2022-09-01 00:00:00', '0,1,2,3,4,5,6', '', 2),
	('2021-07-05 00:00:00', '2021-07-21 00:00:00', '0,1,2,3,4,5,6', '', 1);

INSERT INTO `Media`(`media_name`, `media_gender`, `media_age`, `media_skin`, `contract_id`)
VALUES
	('indifferent_1.gif', '', '', '', 1),
	('indifferent_2.gif', '', '', '', 8),
	('children_1.gif', '', 'child,young_adult', '', 2),
	('children_2.gif', '', 'child,young_adult', '', 3),
	('men_adult_1.gif', 'M', 'child,young_adult,adult,middle_aged', '', 4),
	('women_adult_1.gif', 'F', 'child,young_adult,adult,middle_aged', '', 5),
	('women_young_adult_1.gif', 'F', 'child,young_adult,adult,middle_aged', '', 6),
	('seniors_1.gif', '', 'adult,middle_aged,senior', '', 7);