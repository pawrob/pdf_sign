CREATE DATABASE pdf_signatures;

USE pdf_signatures;
CREATE TABLE pdf_signatures (
    id INT NOT NULL AUTO_INCREMENT,
    signature VARCHAR(10000) NOT NULL,

    PRIMARY KEY(id)
);
