CREATE DATABASE password_bot;
USE password_bot
CREATE TABLE example (id int AUTO_INCREMENT NOT NULL,date date NOT NULL, password varchar(200) NOT NULL, description varchar(255) DEFAULT NULL, PRIMARY KEY (id));
CREATE TABLE users (id int,specials varchar(1) DEFAULT 'T',caps varchar(1) DEFAULT 'T', PRIMARY KEY (id));
CREATE TABLE dictionary (id int NOT NULL AUTO_INCREMENT, word varchar(15) UNIQUE NOT NULL, PRIMARY KEY (id));
