-- Create the database
CREATE DATABASE IF NOT EXISTS StudentsDatabase;

-- Use the created database
USE StudentsDatabase;

-- Create the table
CREATE TABLE IF NOT EXISTS admitted_students (
    student_code INT PRIMARY KEY AUTO_INCREMENT,
    last_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    course VARCHAR(255),
    year INT
);

-- Create table for transfer students
CREATE TABLE IF NOT EXISTS transfer_students (
    student_code INT PRIMARY KEY AUTO_INCREMENT,
    last_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    course VARCHAR(255),
    year INT
);

-- Create table for shifters
CREATE TABLE IF NOT EXISTS shifters (
    student_code INT PRIMARY KEY AUTO_INCREMENT,
    last_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    course VARCHAR(255),
    year INT
);

-- Search for records in the table
SELECT * FROM admitted_students;

-- Search for records in transfer_students table
SELECT * FROM transfer_students;

-- Search for records in shifters table
SELECT * FROM shifters;

-- Insert a record into the table
INSERT INTO admitted_students (last_name, first_name, middle_name, course, year)
VALUES ('Bognalbal', 'Jim Owen','Katigbak', 'BSCS', 2024);

-- Insert records into transfer_students table
INSERT INTO transfer_students (last_name, first_name, middle_name,  course, year)
VALUES ('Doe', 'John', 'Michael', 'Biology', 2023),
       ('Smith', 'Jane', 'Elizabeth', 'Physics', 2022);

-- Insert records into shifters table
INSERT INTO shifters (last_name, first_name, middle_name,  course, year)
VALUES ('Garcia', 'Maria', 'Santos', 'Chemistry', 2023),
       ('Nguyen', 'David', 'Minh', 'Mathematics', 2022);