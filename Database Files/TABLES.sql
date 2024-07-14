CREATE DATABASE HOSPITALITY_MANAGEMENT_SYSTEM
USE HOSPITALITY_MANAGEMENT_SYSTEM 

--CREATING TABLE 'USERS' CONTAINING ALL THE USER LOGIN INFORMATION

CREATE TABLE USERS (
	USERID INT PRIMARY KEY IDENTITY,
	USERNAME NVARCHAR(50) UNIQUE NOT NULL,
	PASSWORD NVARCHAR(50) NOT NULL
);

--CREATING TABLE 'HOTELS' CONTAINING HOTEL NAMES 

CREATE TABLE HOTELS (
	HOTELID INT PRIMARY KEY IDENTITY,
	HOTELNAME NVARCHAR(100) NOT NULL
);


--CREATING TABLE 'ROOMS' CONTAINING INFORMATION ABOUT ROOMS

CREATE TABLE ROOMS (
	ROOMID INT PRIMARY KEY IDENTITY,
	HOTELID INT FOREIGN KEY REFERENCES HOTELS(HOTELID),
	ROOMNUMBER NVARCHAR(50) NOT NULL,
	ROOMTYPE NVARCHAR(50) NOT NULL,
	PRICE DECIMAL
);

--CREATING TABLE RESERVATION CONTAINING INFORMATION ABOUT RESERVATIONS

CREATE TABLE RESERVATION(
	RESERVATIONID INT PRIMARY KEY IDENTITY,
	ROOMID INT FOREIGN KEY REFERENCES ROOMS(ROOMID),
	USERNAME NVARCHAR(50) FOREIGN KEY REFERENCES USERS(USERNAME),
	STARTDATE DATE NOT NULL,
	ENDDATE DATE NOT NULL,
	CHECKINDATE DATE NULL,
	CHECKOUTDATE DATE NULL
);





SELECT * FROM USERS
SELECT * FROM HOTELS
SELECT * FROM ROOMS
SELECT * FROM RESERVATION

EXECUTE GENERATEBILL 1

EXECUTE REGISTERROOM 'The Grand Plaza','TGP243','Suite',30000

EXECUTE UserLogin 'Akash','akash@123'