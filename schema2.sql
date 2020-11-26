DROP TABLE IF EXISTS module;
DROP TABLE IF EXISTS exam;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS lecturer;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS lectModule;
DROP TABLE IF EXISTS organise;
DROP TABLE IF EXISTS studentExam;
DROP TABLE IF EXISTS courseModule;
DROP TABLE IF EXISTS studentModule;
DROP TABLE IF EXISTS courseStudent;
DROP TABLE IF EXISTS admin;

CREATE TABLE module (
	code VARCHAR(45) NOT NULL,
	name VARCHAR(45) NOT NULL,
	semester INT NULL,
	ECTs INT NULL);

INSERT INTO module VALUES
  ('EE123','Analogue Designs',2,5);

CREATE TABLE exam (
  examId VARCHAR(45) NOT NULL,
  moduleCode VARCHAR(45) NOT NULL,
  time TIME,
  date DATE,
  duration INT);

INSERT INTO exam VALUES
  ('EXAM1','EE123',093000,'2021-06-01',120);

  CREATE TABLE `student` (
  `studentId` INT NOT NULL,
  `fName` VARCHAR(45) ,
  `lName` VARCHAR(45));

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

CREATE TABLE lecturer (
  lecturerId INT NOT NULL,
  fName VARCHAR(45) ,
  lName VARCHAR(45));

INSERT INTO lecturer VALUES
(1,'Sinead','Grimes');

CREATE TABLE course (
  code VARCHAR(45) NOT NULL,
  name VARCHAR(45));

INSERT INTO course VALUES
('BP','Computer and Electronic Engineering');

CREATE TABLE lectModule (
  staffId int NOT NULL,
  modCode VARCHAR(45)  NOT NULL);

INSERT INTO lectModule VALUES
(1,'EE123');

CREATE TABLE admin(
        staffId INT NOT NULL,
        fName VARCHAR(45) ,
        lName VARCHAR(45));

INSERT INTO admin VALUES
(1,'Peter','Mangan');

CREATE TABLE `organise` (
  `staffId` int NOT NULL,
  `examId` VARCHAR(45) NOT NULL);

INSERT INTO organise VALUES
(1,'EXAM1');

CREATE TABLE studentExam (
  studentId int NOT NULL,
  examId VARCHAR(45)  NOT NULL);

INSERT INTO studentExam VALUES
(12345678, 'EXAM1');

CREATE TABLE courseModule (
  courseCode VARCHAR(45) NOT NULL,
  modCode VARCHAR(45) NOT NULL);

INSERT INTO courseModule VALUES
('BP','EE123');

CREATE TABLE studentModule (
  studentId INT NOT NULL,
  modCode VARCHAR(45) NOT NULL);

INSERT INTO studentModule VALUES
(12345678, 'EE123');

CREATE TABLE courseStudent (
  studentId INT NOT NULL,
  courseCode VARCHAR(45) NOT NULL);

INSERT INTO courseStudent VALUES
(12345678, 'BP');


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
