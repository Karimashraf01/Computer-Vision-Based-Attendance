TABLES = {}

TABLES['students'] = (
    "CREATE TABLE `students` ("
        "`student_id` INT NOT NULL AUTO_INCREMENT,"
        "`student_name` varchar(255) NOT NULL,"
        "`student_email` varchar(255) NOT NULL UNIQUE,"
        "`grade` INT(255) NOT NULL,"
        "PRIMARY KEY (`student_id`)"
    ");")



embeddings = ""
for i in range(128):
    embeddings += f"`embedded_{i}` FLOAT NOT NULL, "

TABLES['faces'] = f"CREATE TABLE `faces` (`student_id` INT NOT NULL, {embeddings} PRIMARY KEY (`student_id`));"



TABLES['attendence'] = (
    "CREATE TABLE `attendence` ("
        "`student_id` INT NOT NULL,"
        "`timestamp` DATETIME NOT NULL"
    ");"
    "ALTER TABLE `attendence` ADD CONSTRAINT `attendence_fk0` FOREIGN KEY (`student_id`) REFERENCES `students`(`student_id`);")
TABLES['attendence'] += "ALTER TABLE `faces` ADD CONSTRAINT `faces_fk0` FOREIGN KEY (`student_id`) REFERENCES `students`(`student_id`);"
