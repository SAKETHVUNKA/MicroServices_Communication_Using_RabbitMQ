CREATE DATABASE cc_project;

USE cc_project;

CREATE TABLE Products (
  product_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  category VARCHAR(100),
  unit_price DECIMAL(10,2) NOT NULL,
  cost_price DECIMAL(10,2) NOT NULL,
  current_stock INT NOT NULL DEFAULT 0,
  company VARCHAR(255),  
  image BLOB,
  reorder_level INT NOT NULL DEFAULT -1,
  supplier_id INT NOT NULL ,
  date_of_manufacture DATE DEFAULT NULL,
  date_of_expiry DATE DEFAULT NULL,
  PRIMARY KEY (product_id)
);  

CREATE TABLE Suppliers (
  supplier_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  contact_name VARCHAR(255),
  email VARCHAR(255),
  phone_number VARCHAR(20),
  address TEXT,
  PRIMARY KEY (supplier_id)
);

CREATE TABLE Orders (
  order_id INT NOT NULL AUTO_INCREMENT,
  order_date DATE NOT NULL,
  delivery_date DATE,
  total_price DECIMAL(10,2) NOT NULL,
  status ENUM('placed', 'shipped', 'delivered', 'cancelled'),  
  PRIMARY KEY (order_id)
  -- buyer info to be added and handled in backend
);

CREATE TABLE Order_Items (
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (order_id, product_id),  
  FOREIGN KEY (order_id) REFERENCES Orders(order_id),
  FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO Products (name, description, category, unit_price, cost_price, current_stock, company, image, reorder_level, supplier_id, date_of_manufacture, date_of_expiry)
VALUES 
('Laptop', 'High-performance laptop', 'Electronics', 1200.00, 900.00, 10, 'ABC Electronics', NULL, 5, 4, '2024-04-10', '2024-04-15'),
('Smartphone', 'Latest smartphone model', 'Electronics', 800.00, 600.00, 15, 'XYZ Tech', NULL, 7, 4, NULL, NULL),
('Headphones', 'Noise-canceling headphones', 'Electronics', 100.00, 70.00, 20, 'SoundTech', NULL, 10, 4, '2024-04-10', NULL);

INSERT INTO Suppliers (name, contact_name, email, phone_number, address)
VALUES 
('ABC Electronics', 'John Smith', 'john@example.com', '1234567890', '123 Main St, City, Country'),
('XYZ Tech', 'Emily Brown', 'emily@example.com', '9876543210', '456 Oak St, City, Country'),
('SoundTech', 'Michael Johnson', 'michael@example.com', '5551234567', '789 Elm St, City, Country');

INSERT INTO Orders (order_date, delivery_date, total_price, status)
VALUES 
('2024-04-10', '2024-04-15', 2400.00, 'placed'),
('2024-04-12', '2024-04-17', 1600.00, 'shipped'),
('2024-04-14', '2024-04-19', 300.00, 'delivered');

INSERT INTO Order_Items (order_id, product_id, quantity, unit_price)
VALUES 
(1, 1, 2, 1200.00),
(1, 2, 1, 800.00),
(2, 1, 1, 1200.00),
(2, 3, 2, 100.00),
(3, 3, 3, 100.00);
