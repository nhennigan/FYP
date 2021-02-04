def get_tables():
    TABLES = {}
    TABLES['module'] = ( "CREATE TABLE `module` (`code` VARCHAR(45) NOT NULL,`name` VARCHAR(45) NULL,`semester` INT NULL,`ECTs` INT NULL,`lecturer_notes` VARCHAR(45),PRIMARY KEY (`code`));")

    TABLES['exam'] = ("CREATE TABLE `exam` (`exam_id` VARCHAR(45) NOT NULL,`module_code` VARCHAR(45) NOT NULL,`time` TIME,`date` DATE,`duration` INT, `venue` VARCHAR(45),PRIMARY KEY (`exam_id`),FOREIGN KEY (`module_code`) REFERENCES `module`(`code`));")

    TABLES['student'] = ("CREATE TABLE `student` (`student_id` INT NOT NULL,`f_name` VARCHAR(45),`l_name` VARCHAR(45),`password` VARCHAR(45), PRIMARY KEY (`student_id`));")

    TABLES['lecturer'] = ("CREATE TABLE `lecturer` (`lecturer_id` INT NOT NULL,`f_name` VARCHAR(45),`l_name` VARCHAR(45),PRIMARY KEY (`lecturer_id`));")
 
    TABLES['course'] = ("CREATE TABLE `course` (`code` VARCHAR(45) NOT NULL,`name` VARCHAR(45),PRIMARY KEY (`code`));")

    TABLES['lect_module'] = ("CREATE TABLE `lect_module` (`staff_id` int NOT NULL,`mod_code` VARCHAR(45)  NOT NULL,FOREIGN KEY (`mod_code`) REFERENCES `module`(`code`),FOREIGN KEY (`staff_id`) REFERENCES `lecturer`(`lecturer_id`));")
 
    TABLES['admin'] = ("CREATE TABLE `admin` (`staff_id` int NOT NULL, `f_name` VARCHAR(45), `l_name` VARCHAR(45), PRIMARY KEY (`staff_id`));") 

    TABLES['organise'] = ("CREATE TABLE `organise` (`staff_id` int NOT NULL,`exam_id` VARCHAR(45) NOT NULL, PRIMARY KEY (`staff_id`,`exam_id`),FOREIGN KEY (`exam_id`) REFERENCES `exam`(`exam_id`),FOREIGN KEY (`staff_id`) REFERENCES `admin`(`staff_id`));")

    TABLES['student_exam'] = ("CREATE TABLE `student_exam` (`student_id` int NOT NULL,`exam_id` VARCHAR(45)  NOT NULL,FOREIGN KEY (`exam_id`) REFERENCES `exam`(`exam_id`),FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`));")

    TABLES['course_module'] = (" CREATE TABLE `course_module` (`course_code` VARCHAR(45) NOT NULL,`mod_code` VARCHAR(45) NOT NULL ,PRIMARY KEY (`course_code`,`mod_code`),FOREIGN KEY (`course_code`) REFERENCES `course`(`code`),FOREIGN KEY (`mod_code`) REFERENCES `module`(`code`));")

    TABLES['student_module'] = ("CREATE TABLE `student_module` (`student_id` INT NOT NULL,`mod_code` VARCHAR(45) NOT NULL,PRIMARY KEY (`student_id`,`mod_code`),FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`),FOREIGN KEY (`mod_code`) REFERENCES `module`(`code`));")

    TABLES['course_student'] = ("CREATE TABLE `course_student` (`student_id` INT NOT NULL,`course_code` VARCHAR(45) NOT NULL,FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`),FOREIGN KEY (`course_code`) REFERENCES `course`(`code`));")


    return TABLES

def get_data():
    DATA = {}

    DATA['module']=[('EE123','Analogue Designs',2,5,"Ask for log tables"),('EE456','System On Chip Design',2,5,'Bring calulcator'),('CT432','Object Oriented Programming',2,5,'Answer all questions'),('BA234','Irish History',2,5,'Answer any 2 questions'),('BA245','Creative Writing',2,10,'References not reuired'),('BA256','Intoduction to Journalism',2,5,'Answer all questions')]

    DATA['exam']=[('EXAM1','EE123','08:00:00','2021-06-01',120,'The Kingfisher'),('EXAM2','EE456','08:00:00','2021-06-01',120,'The Kingfisher'),('EXAM3','CT432','08:00:00','2021-06-01',120,'The Kingfisher'),('EXAM4','BA234','08:00:00','2021-06-01',120,'The Kingfisher'),('EXAM5','BA245','08:00:00','2021-06-01',120,'The Kingfisher'),('EXAM6','BA256','08:00:00','2021-06-01',120,'The Kingfisher')]

    DATA['student']=[(12345678,'Niamh','Hennigan','pw'),(23456789,'John','Jones','pw'),(34567890,'Mary','OConnor','pw'),(45678901,'Luke','Curran','pw'),(56789012,'Meadhbh','Keane','pw'),(67890123,'Katie','Whelan','pw'),(78901234,'Michael','Talty','pw'),(89012345,'Aine','Ronan','pw'),(90123456,'Rachel','Foxe','pw')]
   
    DATA['lecturer']=[(87654321,'Sinead','Grimes'),(89012345,'Martin','Meere'),(86420864,'Fearghal','Morgan',),(88888888,'Liam','Kilmartin'),(87777777,'Desmond','Chambers'),(86666666,'John','Kearney')]

    DATA['course']=[('BP','Computer and Electronic Engineering'),('BA','Bachelor of Arts')]

    DATA['lect_module']=[(88888888,'EE123'),(86420864,'EE456'),(87777777,'CT432'),(86666666,'BA234'),(86666666,'BA245'),(87654321,'BA256')]

    DATA['admin']=[(11111111,'Peter','Mangan')]

    DATA['organise']=[(11111111,'EXAM1'),(11111111,'EXAM2'),(11111111,'EXAM3'),(11111111,'EXAM4'),(11111111,'EXAM5'),(11111111,'EXAM6')]

    DATA['student_exam']=[(12345678, 'EXAM1'),(23456789,'EXAM1'),(34567890,'EXAM1'),(45678901,'EXAM1'),(12345678, 'EXAM2'),(23456789,'EXAM2'),(34567890,'EXAM2'),(45678901,'EXAM2'),(12345678, 'EXAM3'),(23456789,'EXAM3'),(34567890,'EXAM3'),(45678901,'EXAM3'),(56789012,'EXAM4'),(67890123,'EXAM4'),(78901234,'EXAM4'),(89012345,'EXAM4'),(90123456,'EXAM4'),(56789012,'EXAM5'),(67890123,'EXAM5'),(78901234,'EXAM5'),(89012345,'EXAM5'),(90123456,'EXAM5'),(56789012,'EXAM6'),(67890123,'EXAM6'),(78901234,'EXAM6'),(89012345,'EXAM6'),(90123456,'EXAM6')]

    DATA['course_module']=[('BP','EE123'),('BP','EE456'),('BP','CT432'),('BA','BA256'),('BA','BA234'),('BA','BA245')]

    DATA['student_module']=[(12345678, 'EE123'),(23456789, 'EE123'),(34567890, 'EE123'),(45678901, 'EE123'),(12345678, 'EE456'),(23456789, 'EE456'),(34567890, 'EE456'),(45678901, 'EE456'),(12345678, 'CT432'),(23456789, 'CT432'),(34567890, 'CT432'),(45678901, 'CT432'),(56789012,'BA234'),(67890123,'BA234'),(78901234,'BA234'),(89012345,'BA234'),(90123456,'BA234'),(56789012,'BA245'),(67890123,'BA245'),(78901234,'BA245'),(89012345,'BA245'),(90123456,'BA245'),(56789012,'BA256'),(67890123,'BA256'),(78901234,'BA256'),(89012345,'BA256'),(90123456,'BA256')]

    DATA['course_student']=[(12345678, 'BP'),(23456789, 'BP'),(34567890, 'BP'),(45678901, 'BP'),(56789012,'BA'),(67890123,'BA'),(78901234,'BA'),(89012345,'BA'),(90123456,'BA')]
    
    return DATA 

def get_instructions():
    INSTRUCTIONS= ["""INSERT INTO `module`(`code`,`name`,`semester`,`ECTs`,`lecturer_notes`) VALUES (%s,%s,%s,%s,%s);""","""INSERT INTO `exam` (`exam_id`,`module_code`,`time`,`date`, `duration`,`venue`) VALUES (%s,%s,%s,%s,%s,%s);""","""INSERT INTO `student`(`student_id`, `f_name`, `l_name`, `password`) VALUES (%s,%s,%s,%s);""","""INSERT INTO `lecturer`(`lecturer_id`,`f_name`,`l_name`) VALUES (%s,%s,%s);""","""INSERT INTO `course`(`code`,`name`) VALUES (%s,%s);""","""INSERT INTO `lect_module`(`staff_id`, `mod_code`) VALUES (%s,%s);""","""INSERT INTO `admin`(`staff_id`,`f_name`,`l_name`) VALUES (%s,%s,%s);""","""INSERT INTO `organise`(`staff_id`,`exam_id`) VALUES (%s,%s);""","""INSERT INTO `student_exam`(`student_id`,`exam_id`) VALUES (%s,%s);""","""INSERT INTO `course_module`(`course_code`,`mod_code`) VALUES (%s,%s);""","""INSERT INTO `student_module`(`student_id`,`mod_code`) VALUES (%s,%s);""","""INSERT INTO `course_student`(`student_id`,`course_code`) VALUES (%s,%s);"""]
    return INSTRUCTIONS

def get_names():
    NAMES=["module","exam","student","lecturer","course","lect_module","admin","organise","student_exam","course_module","student_module","course_student"]
