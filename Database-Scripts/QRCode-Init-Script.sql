-- CREATE USER 'QuickReportApp'@'localhost' IDENTIFIED BY 'password';
-- GRANT ALL PRIVILEGES ON qr_report_v1.*  TO 'QuickReportApp'@'localhost';
 

DROP SCHEMA IF EXISTS qr_report_v1;
CREATE SCHEMA IF NOT EXISTS qr_report_v1 DEFAULT CHARACTER SET utf8 ;
USE qr_report_v1 ;


DROP TABLE IF EXISTS qr_report_v1.Users;
CREATE TABLE IF NOT EXISTS qr_report_v1.Users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    passwordHash VARCHAR(128) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY(id)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS qr_report_v1.Assets;
CREATE TABLE IF NOT EXISTS qr_report_v1.Assets (
    id INT NOT NULL AUTO_INCREMENT,
    uniqueIdentifier VARCHAR(16) NOT NULL,
    building VARCHAR(255) NOT NULL,
    roomNumber VARCHAR(255) NOT NULL,
    appliance VARCHAR(255) NOT NULL,
    serviceRequired BOOLEAN DEFAULT FALSE,
    userID INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (userID) REFERENCES qr_report_v1.Users(id)
) ENGINE = InnoDB;
