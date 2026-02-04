-- DATABASE PERFORMANCE MONITORING DASHBOARD - LIVE DEMO COMMANDS
-- Copy and paste these sections in MySQL Workbench during your presentation

-- SECTION 1: DATABASE SETUP
CREATE DATABASE IF NOT EXISTS db_monitoring;
CREATE USER IF NOT EXISTS 'monitor_user'@'localhost' IDENTIFIED BY 'monitor123';
GRANT SELECT, PROCESS, SHOW DATABASES ON *.* TO 'monitor_user'@'localhost';
GRANT SELECT ON performance_schema.* TO 'monitor_user'@'localhost';
GRANT SELECT ON information_schema.* TO 'monitor_user'@'localhost';
FLUSH PRIVILEGES;

-- SECTION 2: VERIFY SETUP
SHOW VARIABLES LIKE 'performance_schema';
SHOW GRANTS FOR 'monitor_user'@'localhost';

-- SECTION 3: CREATE DEMO DATA
USE db_monitoring;
CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), email VARCHAR(100));
CREATE TABLE orders (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, product VARCHAR(100), amount DECIMAL(10,2));
INSERT INTO users VALUES (1,'john','john@test.com'), (2,'jane','jane@test.com'), (3,'bob','bob@test.com');
INSERT INTO orders VALUES (1,1,'Laptop',999.99), (2,2,'Mouse',25.50), (3,3,'Keyboard',75.00);

-- SECTION 4: GENERATE ACTIVITY (Run during demo to show real-time changes)
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM orders;
SELECT * FROM users WHERE id > 1;
SELECT SLEEP(2);
SHOW PROCESSLIST;