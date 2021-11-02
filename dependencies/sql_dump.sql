CREATE DATABASE password_bot;
CREATE TABLE example (id int AUTO_INCREMENT NOT NULL,date date NOT NULL, password varchar(50) NOT NULL, description varchar(255) DEFAULT NULL, PRIMARY KEY (id));
CREATE TABLE users (id int, PRIMARY KEY (id));
CREATE TABLE dictionary (id int NOT NULL AUTO_INCREMENT, word varchar(15) UNIQUE NOT NULL, PRIMARY KEY (id));
CREATE USER 'tgBot'@'localhost';
ALTER USER 'tgBot'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON passwords.* TO 'tgBot'@'localhost';
FLUSH PRIVILEGES;
