SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS Customer_House_Wishes;
DROP TABLE IF EXISTS Sales;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Houses;
DROP TABLE IF EXISTS Categories;

SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE Categories (
    category_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    rooms INT NOT NULL,
    baths INT NOT NULL,
    PRIMARY KEY (category_id)
);

CREATE TABLE Houses (
    house_id INT NOT NULL AUTO_INCREMENT,
    category_id INT NULL,
    list_date DATE NOT NULL,
    list_price DECIMAL(19,4),
    adjusted_price DECIMAL(19,4),
    street VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zip VARCHAR(255),
    location_description VARCHAR(255),
    PRIMARY KEY (house_id),
    FOREIGN KEY (category_id) REFERENCES Categories (category_id) ON DELETE SET NULL
);

CREATE TABLE Customers (
    customer_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL,
    street VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zip VARCHAR(255),
    country VARCHAR(255),
    phone VARCHAR(255) NOT NULL,
    PRIMARY KEY (customer_id)
);

CREATE TABLE Sales (
    sale_id INT NOT NULL AUTO_INCREMENT,
    house_id INT NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    date DATE NOT NULL,
    sale_price DECIMAL(19,4) NOT NULL,
    profit DECIMAL(19,4),
    PRIMARY KEY (sale_id),
    FOREIGN KEY (house_id) REFERENCES Houses (house_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Customers (customer_id) ON DELETE CASCADE,
    CONSTRAINT unique_house UNIQUE (house_id, sale_id)
);

CREATE TABLE Customer_House_Wishes (
    wish_id INT NOT NULL AUTO_INCREMENT,
    house_id INT NOT NULL,
    customer_id INT NOT NULL,
    create_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (wish_id),
    FOREIGN KEY (house_id) REFERENCES Houses (house_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Customers (customer_id) ON DELETE CASCADE
);

INSERT INTO Categories (name, rooms, baths)
VALUES ('single-family', 3, 2),
('condo',2, 2),
('town house',4 ,3);

INSERT INTO Houses (category_id, list_date, list_price, adjusted_price, street, city, state, zip, location_description)
VALUES 
((SELECT category_id FROM Categories WHERE name='single-family'), '2022-01-02', 848000, 890000, '144 3rd street', 'San Jose', 'CA', '95112', 'Great Place! WOW!'),
((SELECT category_id FROM Categories WHERE name='condo'), '2022-03-02', 649800, 659800, '255 Llano De Los Robles Ave', 'San Jose', 'CA', '95136', 'Wonderful Place! WOW!'),
(NULL, '2022-01-01', 842000, 895200, '1400 Bowe Ave', 'Santa Clara', 'CA', '95051', 'Amazing Place! WOW!');

INSERT INTO Customers (first_name, last_name, age, email, is_active, street, city, state, zip, country, phone)
VALUES ('HuanChun', 'Lin', 25, 'lin@gmail.com', 0, '1701 SW Western Blvd.', 'Corvallis', 'OR', '97333', 'US', '541.737.2464'),
('Satyam', 'Patel', 27, 'patel@gmail.com', 1, '1600 Amphitheatre Parkway', 'Mountain View', 'CA', '97333', 'US', '209.513.0514'),
('Elon', 'Musk', 35, 'musk@gmail.com', 0, '3500 Deer Creek Road', 'Corvallis', 'OR', '97333', 'US', '310.709.9497');

INSERT INTO Customer_House_Wishes (customer_id, house_id, create_at, updated_at)
VALUES ((SELECT customer_id FROM Customers WHERE last_name='Lin'), (SELECT house_id FROM Houses WHERE street='144 3rd street'), '2022-05-02 01:00:00', '2022-05-10 01:00:00'),
((SELECT customer_id FROM Customers WHERE last_name='Patel'), (SELECT house_id FROM Houses WHERE street='144 3rd street'), '2022-05-01 01:00:00', '2022-05-11 01:00:00'),
((SELECT customer_id FROM Customers WHERE last_name='Patel'), (SELECT house_id FROM Houses WHERE street='1400 Bowe Ave'), '2022-05-01 01:00:00', '2022-05-01 01:00:00');

INSERT INTO Sales (house_id, customer_id, date, sale_price, profit)
VALUES ((SELECT house_id FROM Houses WHERE street='144 3rd street'), (SELECT customer_id FROM Customers WHERE last_name='Lin'), '2022-02-28', '890000','340000'),
((SELECT house_id FROM Houses WHERE street='255 Llano De Los Robles Ave'), (SELECT customer_id FROM Customers WHERE last_name='Patel'), '2022-03-15', '659800', '144000'),
((SELECT house_id FROM Houses WHERE street='1400 Bowe Ave'), (SELECT customer_id FROM Customers WHERE last_name='Musk'), '2022-02-28', '895200', '151200');