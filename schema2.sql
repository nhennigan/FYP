CREATE TABLE module (
code VARCHAR(45) NOT NULL,
name VARCHAR(45) NULL,
semester INT NULL,
ECTs INT NULL);

INSERT INTO module VALUES
('EE123','Analogue Designs',2,5); 

CREATE TABLE exam (
examId VARCHAR(45) NOT NULL,
moduleCode VARCHAR(45) NOT NULL,
time TIME,
date DATE,
duration INT,
PRIMARY KEY (examId),
FOREIGN KEY (moduleCode) REFERENCES module(code));

INSERT INTO exam VALUES
('EXAM1','EE123',09:30:00,2021-06-01,120);

  CREATE TABLE `student` (
  `studentId` INT NOT NULL,
  `fName` VARCHAR(45) ,
  `lName` VARCHAR(45),
  PRIMARY KEY (`studentId`));

  INSERT INTO student VALUES
  (12345678,'Niamh','Hennigan'),
  (23456789,'John','Jones'),
  (34567890,'Mary','OConnor'),
  (45678901,'Luke','Curran'),
  (56789012,'Meadhbh','Keane'),
  (67890123,'Katie','Whelan'),
  (78901234,'Michael','Talty'),
  (89012345,'Aine','Ronan'),
  (90123456,'Rachel','Foxe');

  CREATE TABLE `lecturer` (
  `lecturerId` INT NOT NULL,
  `fName` VARCHAR(45) ,
  `lName` VARCHAR(45),
  PRIMARY KEY (`lecturerId`));

CREATE TABLE `course` (
  `code` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) ,
  PRIMARY KEY (`code`));

CREATE TABLE `lectModule` (
  `staffId` int NOT NULL,
  `modCode` VARCHAR(45)  NOT NULL,
  PRIMARY KEY (`staffId`,`modCode`),
  FOREIGN KEY (`modCode`) REFERENCES `module`(`code`),
  FOREIGN KEY (`staffId`) REFERENCES `lecturer`(`lecturerId`));

CREATE TABLE `organise` (
  `staffId` int NOT NULL,
  `examId` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`staffId`,`examId`),
  FOREIGN KEY (`examId`) REFERENCES `exam`(`examId`),
  FOREIGN KEY (`staffId`) REFERENCES `lecturer`(`lecturerId`));

 CREATE TABLE `studentExam` (
  `studentId` int NOT NULL,
  `examId` VARCHAR(45)  NOT NULL,
  PRIMARY KEY (`studentId`,`examId`),
  FOREIGN KEY (`examId`) REFERENCES `exam`(`examId`),
  FOREIGN KEY (`studentId`) REFERENCES `student`(`studentId`));

 CREATE TABLE `courseModule` (
  `courseCode` VARCHAR(45) NOT NULL,
  `modCode` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`courseCode`,`modCode`),
  FOREIGN KEY (`courseCode`) REFERENCES `course`(`code`),
  FOREIGN KEY (`modCode`) REFERENCES `module`(`code`));

 CREATE TABLE `studentModule` (
  `studentId` INT NOT NULL,
  `modCode` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`studentID`,`modCode`),
  FOREIGN KEY (`studentID`) REFERENCES `student`(`studentId`),
  FOREIGN KEY (`modCode`) REFERENCES `module`(`code`));

CREATE TABLE `courseStudent` (
  `studentId` INT NOT NULL,
  `courseCode` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`studentID`,`courseCode`),
  FOREIGN KEY (`studentID`) REFERENCES `student`(`studentId`),
  FOREIGN KEY (`courseCode`) REFERENCES `course`(`code`));

CREATE TABLE admin(
	staffId INT NOT NULL,
	fName VARCHAR(45) ,
	lName VARCHAR(45),
	PRIMARY KEY (staffId));

ALTER TABLE module
	ADD PRIMARY KEY(examId);
