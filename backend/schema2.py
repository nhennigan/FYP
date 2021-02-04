def get_tables():
    TABLES = {}
    TABLES['module'] = ( "CREATE TABLE `module` (`code` VARCHAR(45) NOT NULL,`name` VARCHAR(45) NULL,`semester` INT NULL,`ECTs` INT NULL,`lecturer_notes` VARCHAR(45),PRIMARY KEY (`code`));")

    TABLES['exam'] = ("CREATE TABLE `exam` (`exam_id` VARCHAR(45) NOT NULL,`module_code` VARCHAR(45) NOT NULL,`time` TIME,`date` DATE,`duration` INT, `venue` VARCHAR(45),PRIMARY KEY (`exam_id`),FOREIGN KEY (`module_code`) REFERENCES `module`(`code`));")

    TABLES['student'] = ("CREATE TABLE `student` (`student_id` INT NOT NULL,`f_name` VARCHAR(45),`l_name` VARCHAR(45),`password` VARCHAR(45), PRIMARY KEY (`student_id`));")

    TABLES['lecturer'] = ("CREATE TABLE `lecturer` (`lecturer_id` INT NOT NULL,`f_name` VARCHAR(45),`l_name` VARCHAR(45),PRIMARY KEY (`lecturer_id`));")
 
    TABLES['course'] = ("CREATE TABLE `course` (`code` VARCHAR(45) NOT NULL,`name` VARCHAR(45),PRIMARY KEY (`code`));")

    TABLES['lect_module'] = ("CREATE TABLE `lect_module` (`staff_id` int NOT NULL,`mod_code` VARCHAR(45)  NOT NULL,FOREIGN KEY (`mod_code`) REFERENCES `module`(`code`),FOREIGN KEY (`staff_id`) REFERENCES `lecturer`(`lecturer_id`));")
 
    TABLES['admin'] = ("CREATE TABLE `admin` (`staff_id` int NOT NULL, `f_name` VARCHAR(45), `l_name` VARCHAR(45), PRIMARY KEY (`staff_id`));") 

    TABLES['organise'] = ("CREATE TABLE `organise` (`staff_id` int NOT NULL,`exam_id` VARCHAR(45) NOT NULL, PRIMARY KEY (`staff_id`,`exam_id`),FOREIGN KEY (`exam_id`) REFERENCES `exam`(`exam_id`),FOREIGN KEY (`staff_id`) REFERENCES `lecturer`(`lecturer_id`));")

    TABLES['student_exam'] = ("CREATE TABLE `student_exam` (`student_id` int NOT NULL,`exam_id` VARCHAR(45)  NOT NULL,FOREIGN KEY (`exam_id`) REFERENCES `exam`(`exam_id`),FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`));")

    TABLES['course_module'] = (" CREATE TABLE `course_module` (`course_code` VARCHAR(45) NOT NULL,`mod_code` VARCHAR(45) NOT NULL ,PRIMARY KEY (`course_code`,`mod_code`),FOREIGN KEY (`course_code`) REFERENCES `course`(`code`),FOREIGN KEY (`mod_code`) REFERENCES `module`(`code`));")

    TABLES['student_module'] = ("CREATE TABLE `student_module` (`student_id` INT NOT NULL,`mod_code` VARCHAR(45) NOT NULL,PRIMARY KEY (`student_id`,`mod_code`),FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`),FOREIGN KEY (`mod_code`) REFERENCES `module`(`code`));")

    TABLES['course_student'] = ("CREATE TABLE `course_student` (`student_id` INT NOT NULL,`course_code` VARCHAR(45) NOT NULL,FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`),FOREIGN KEY (`course_code`) REFERENCES `course`(`code`));")


    return TABLES

def get_data():
    DATA = {}
    DATA['module']=[('EE123','Analogue Designs',2,5,"Ask for log tables"),('EE456','System On Chip Design',2,5,'Bring calulcator')]
    DATA['exam']=[('EXAM1','EE123','08:00:00','2021-06-01',120,'The Kingfisher')]
    DATA['student']=[(12345678,'niamh','hen','pw'),(23456789,'John','Jones','pw'),(34567890,'Mary','OConnor','pw')]
    DATA['lecturer']=[(1,'Sinead','Grimes')]
    DATA['course']=[('BP','Computer and Electronic Engineering')]
    DATA['lect_module']=[(1,'EE123')]
    DATA['admin']=[(1,'Peter','Mangan')]
    DATA['organise']=[(1,'EXAM1')]
    DATA['student_exam']=[(12345678, 'EXAM1'),(23456789,'EXAM1')]
    DATA['course_module']=[('BP','EE123')]
    DATA['student_module']=[(12345678, 'EE123')]
    DATA['course_student']=[(12345678, 'BP')]
    
    return DATA 

def get_instructions():
    INSTRUCTIONS= ["""INSERT INTO `module`(`code`,`name`,`semester`,`ECTs`,`lecturer_notes`) VALUES (%s,%s,%s,%s,%s);""","""INSERT INTO `exam` (`exam_id`,`module_code`,`time`,`date`, `duration`,`venue`) VALUES (%s,%s,%s,%s,%s,%s);""","""INSERT INTO `student`(`student_id`, `f_name`, `l_name`, `password`) VALUES (%s,%s,%s,%s);""","""INSERT INTO `lecturer`(`lecturer_id`,`f_name`,`l_name`) VALUES (%s,%s,%s);""","""INSERT INTO `course`(`code`,`name`) VALUES (%s,%s);""","""INSERT INTO `lect_module`(`staff_id`, `mod_code`) VALUES (%s,%s);""","""INSERT INTO `admin`(`staff_id`,`f_name`,`l_name`) VALUES (%s,%s,%s);""","""INSERT INTO `organise`(`staff_id`,`exam_id`) VALUES (%s,%s);""","""INSERT INTO `student_exam`(`student_id`,`exam_id`) VALUES (%s,%s);""","""INSERT INTO `course_module`(`course_code`,`mod_code`) VALUES (%s,%s);""","""INSERT INTO `student_module`(`student_id`,`mod_code`) VALUES (%s,%s);""","""INSERT INTO `course_student`(`student_id`,`course_code`) VALUES (%s,%s);"""]
    return INSTRUCTIONS

def get_names():
    NAMES=["module","exam","student","lecturer","course","lect_module","admin","organise","student_exam","course_module","student_module","course_student"]
