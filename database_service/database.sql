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

