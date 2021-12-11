from datetime import datetime

def list_students(cnx, cursor):
    cursor.execute("SELECT * FROM students")
    results = []
    for (student_id, student_name, student_email, grade) in cursor:
        results.append([
            student_id,    
            student_name,    
            student_email,    
            grade
        ])
    cnx.commit()
    return results


def grab_faces(cnx, cursor):
    cursor.execute("SELECT * FROM faces")
    results = []
    for row in cursor:
        results.append({"id": row[0], "embeddings": row[1:]})
    cnx.commit()
    return results


def add_student(cnx, cursor, student_id, student_name, student_email, grade, embedding):
    
    add_student = f"INSERT INTO students (student_id, student_name, student_email, grade) VALUES ({student_id}, '{student_name}', '{student_email}', {grade})"
    cursor.execute(add_student)

    embeddings = ""
    for i in range(128):
        embeddings += f"`embedded_{i}`, "
    embedding = list(map(str, embedding))
    
    add_face = f"INSERT INTO faces (student_id, {embeddings[:-2]}) VALUES ({student_id}," +  ", ".join(embedding) + ")"
    cursor.execute(add_face)
    cnx.commit()


def add_attendence(cnx, cursor, student_id):
    add_student = "INSERT INTO attendence (student_id, timestamp) VALUES (%s, %s)"
    student_employee = (student_id, datetime.now())
    cursor.execute(add_student, student_employee)
    cnx.commit()


def list_attendence(cnx, cursor, student_id):
    add_student = f"SELECT * FROM attendence where student_id = {student_id}"
    cursor.execute(add_student)
    results = []
    for row in cursor:
        results.append([row[1]])
        
    get_student = f"SELECT * FROM students where student_id = {student_id}"
    cursor.execute(get_student)
    name = "Student Not Found"
    for row in cursor:
        name = row[1]
        break
    cnx.commit()
    
    return results, name

def get_name(cnx, cursor, student_id):

    get_student = f"SELECT * FROM students where student_id = {student_id}"
    cursor.execute(get_student)
    name = "Unknown"
    for row in cursor:
        name = row[1]
        break
    cnx.commit()
    
    return name



