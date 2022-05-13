-- CRUD queries for our project. The variables are prefixed with : for now.

-- CUSTOMERS
-- create
INSERT INTO Customers (first_name, last_name, age, email, is_active, street, city, state, zip, country, phone)
VALUES (:first_name, :last_name, :age, :email, :is_active, :street, :city, :state, :zip, :country, :phone);

-- retrieve
SELECT * FROM Customers;

-- update
UPDATE Customers
SET first_name=:first_name, last_name=:last_name, age=:age, email=:email, is_active=:is_active, street=:street, city=:city, state=:state, zip=:zip, country=:country, phone=:phone
WHERE customer_id = :customer_id;

-- delete
DELETE FROM Customers WHERE customer_id = :customer_id;
-- ---------------------------

-- HOUSES
-- create
INSERT INTO Houses (category_id, list_date, list_price, adjusted_price, street, city, state, zip, location_description)
VALUES (:category_id, :list_date, :list_price, :adjusted_price, :street, :city, :state, :zip, :location_description);

-- retrieve
SELECT Categories.name as category, list_date, list_price, adjusted_price, street, city, state, zip, location_description
FROM Houses
LEFT JOIN Categories ON Houses.category_id = Categories.category_id;

-- update
UPDATE Houses
SET category_id =:category_id, list_date =:list_date, list_price =:list_price, adjusted_price =:adjusted_price, street =:street, city =:city, state =:state, zip =:zip, location_description =:location_description
WHERE house_id = :house_id;

-- delete
DELETE FROM Houses WHERE house_id=:house_id;
-- ----------------------------------

-- CATEGORIES
-- create
INSERT INTO Categories (name,rooms, baths)
VALUES (:name, :rooms, :baths);

-- retrieve
SELECT * FROM Categories;

-- update
UPDATE Categories
SET name=:name, rooms=:rooms, baths=:baths
WHERE category_id=:category_id;

-- delete
DELETE FROM Categories WHERE category_id=:category_id
-- -----------------------------------

-- CUSTOMER_HOUSE_WISHES
-- create
INSERT INTO Customer_House_Wishes (house_id, customer_id, create_at, updated_at)
VALUES (:house_id, :customer_id, :create_at, :updated_at);

-- retrieve
SELECT H.street, C.first_name, C.last_name, create_at, updated_at
FROM Customer_House_Wishes
LEFT JOIN Customers C on Customer_House_Wishes.customer_id = C.customer_id
LEFT JOIN Houses H on Customer_House_Wishes.house_id = H.house_id;

-- update
UPDATE Customer_House_Wishes
SET house_id=:house_id, customer_id=:customer_id, create_at=:create_at, updated_at=:updated_at
WHERE wish_id=:wish_id;

-- delete
DELETE FROM Customer_House_Wishes WHERE wish_id=:wish_id;
-- ------------------------------------

-- SALES
-- retrieve
Select H.street, C.first_name, C.last_name, date, sale_price, profit
FROM Sales
INNER JOIN Customers C on Sales.customer_id = C.customer_id
INNER JOIN Houses H on Sales.house_id = H.house_id;

-- create
INSERT INTO Sales (house_id, customer_id, date, sale_price, profit)
VALUES (:house_id, :customer_id, :date, :sale_price, :profit);

-- update
UPDATE Sales
SET house_id=:house_id, customer_id=:customer_id, date=:date, sale_price=:sale_price, profit=:profit
WHERE sale_id = :sale_id;

-- delete
DELETE FROM Sales WHERE sale_id=:sale_id
-- ------------------------------------