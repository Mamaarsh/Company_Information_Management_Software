create database Orders;
use Orders;
create table Info (
	infoid int auto_increment primary key,
    userid int unique,
	firstname varchar(100),
    lastname varchar(100),
    companyname varchar(100)
);

create table Company (
	companyid int auto_increment primary key,
    userid int unique,
    companyname varchar(100),
    internal int,
    prephone varchar(3),
    phone varchar(10) unicode,
    phone2 varchar(10) unicode,
    mobilephone varchar(15) unicode
);