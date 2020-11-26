DROP TABLE IF EXISTS module;
CREATE TABLE module (
	code VARCHAR(45) NOT NULL,
	name VARCHAR(45) NOT NULL,
	semester INT NULL,
	ECTs INT NULL);

INSERT INTO module VALUES
  ('EE123','Analogue Designs',2,5); 

DROP TABLE IF EXISTS exam;
CREATE TABLE exam (
	examId VARCHAR(45) NOT NULL,
	moduleCode VARCHAR(45) NOT NULL,
	time TIME,
	date DATE,
	duration INT);

#INSERT INTO exam VALUES
#  ('EXAM1','EE456',093000,2021-06-01,120);

DROP TABLE IF EXISTS student;
  CREATE TABLE `student` (
  `studentId` INT NOT NULL,
  `fName` VARCHAR(45) ,
  `lName` VARCHAR(45));

#INSERT INTO student VALUES
#  (12345678,'Niamh','Hennigan'),
#  (23456789,'John','Jones'),
#  (34567890,'Mary','OConnor'),
#  (45678901,'Luke','Curran'),
#  (56789012,'Meadhbh','Keane'),
#  (67890123,'Katie','Whelan'),
#  (78901234,'Michael','Talty'),
#  (89012345,'Aine','Ronan'),
#  (90123456,'Rachel','Foxe');

DROP TABLE IF EXISTS lecturer;
CREATE TABLE lecturer (
  lecturerId INT NOT NULL,
  fName VARCHAR(45) ,
  lName VARCHAR(45));

#INSERT INTO lecturer VALUES
#(1,'Sinead','Grimes');

DROP TABLE IF EXISTS course;
CREATE TABLE course (
  code VARCHAR(45) NOT NULL,
  name VARCHAR(45));

#INSERT INTO course VALUES
#('BP','Computer and Electronic Engineering');

DROP TABLE IF EXISTS lectModule;
CREATE TABLE lectModule (
  staffId int NOT NULL,
  modCode VARCHAR(45)  NOT NULL);

#INSERT INTO lectModule VALUES
#(1,'EE123');

DROP TABLE IF EXISTS organise;
CREATE TABLE `organise` (
  `staffId` int NOT NULL,
  `examId` VARCHAR(45) NOT NULL);

DROP TABLE IF EXISTS studentExam;
 CREATE TABLE `studentExam` (
  `studentId` int NOT NULL,
  `examId` VARCHAR(45)  NOT NULL);

DROP TABLE IF EXISTS courseModule;
 CREATE TABLE `courseModule` (
  `courseCode` VARCHAR(45) NOT NULL,
  `modCode` VARCHAR(45) NOT NULL);

DROP TABLE IF EXISTS studentModule;
 CREATE TABLE `studentModule` (
  `studentId` INT NOT NULL,
  `modCode` VARCHAR(45) NOT NULL);

DROP TABLE IF EXISTS courseStudent;
CREATE TABLE `courseStudent` (
  `studentId` INT NOT NULL,
  `courseCode` VARCHAR(45) NOT NULL);

DROP TABLE IF EXISTS admin;
CREATE TABLE admin(
	staffId INT NOT NULL,
	fName VARCHAR(45) ,
	lName VARCHAR(45));

ALTER TABLE module
	ADD PRIMARY KEY(code);

ALTER TABLE exam 
	ADD PRIMARY KEY(examId);
#	ADD KEY moduleCode(moduleCode);

ALTER TABLE student
        ADD PRIMARY KEY(studentId);

ALTER TABLE lecturer
        ADD PRIMARY KEY(lecturerId);

ALTER TABLE course
        ADD PRIMARY KEY(code);

ALTER TABLE lectModule
        ADD PRIMARY KEY(staffId,modCode);
#        ADD KEY modCode(modCode)
#	ADD KEY staffId(staffId);

ALTER TABLE organise
        ADD PRIMARY KEY(staffId,examId);
#        ADD KEY examId(examId)
#	ADD KEY staffId(staffId);

ALTER TABLE studentExam
	ADD PRIMARY KEY(studentId,examId);
#	ADD KEY studentId(studentId)
#	ADD KEY examId(examId);

ALTER TABLE courseModule
        ADD PRIMARY KEY(courseCode,modCode);
#	ADD KEY courseCode(courseCode)
#	ADD KEY modCode(modCode);

ALTER TABLE studentModule
        ADD PRIMARY KEY(studentId,modCode);
#        ADD KEY studentId(studentId)
#	ADD KEY modCode(modCode);

ALTER TABLE courseStudent
        ADD PRIMARY KEY(studentId,courseCode);
#        ADD KEY studentId(studentId)
#	ADD KEY courseCode(courseCode);

ALTER TABLE admin
        ADD PRIMARY KEY(staffId);

ALTER TABLE exam
  ADD CONSTRAINT FOREIGN KEY (moduleCode) REFERENCES module(code); 

ALTER TABLE lectModule
  ADD CONSTRAINT FOREIGN KEY (modCode) REFERENCES module(code),
  ADD CONSTRAINT FOREIGN KEY (staffId) REFERENCES lecturer(lecturerId);

ALTER TABLE organise
  ADD CONSTRAINT FOREIGN KEY (examId) REFERENCES exam(examId),
  ADD CONSTRAINT FOREIGN KEY (staffId) REFERENCES lecturer(lecturerId);

ALTER TABLE studentExam
  ADD CONSTRAINT FOREIGN KEY (examId) REFERENCES exam(examId),
  ADD CONSTRAINT FOREIGN KEY (studentId) REFERENCES student(studentId);

ALTER TABLE courseModule
  ADD CONSTRAINT FOREIGN KEY (courseCode) REFERENCES course(code),
  ADD CONSTRAINT FOREIGN KEY (modCode) REFERENCES module(code);

ALTER TABLE studentModule
  ADD CONSTRAINT FOREIGN KEY (studentID) REFERENCES student(studentId),
  ADD CONSTRAINT FOREIGN KEY (modCode) REFERENCES module(code);

ALTER TABLE courseStudent
  ADD CONSTRAINT FOREIGN KEY (studentID) REFERENCES student(studentId),
  ADD CONSTRAINT FOREIGN KEY (courseCode) REFERENCES course(code);
