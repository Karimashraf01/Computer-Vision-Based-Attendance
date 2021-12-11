
print("""

   ______________________________________ _______  ________  ________    _______  _________ ___________   ______________.___. _______________________________   _____   
  /  _  \__    ___/\__    ___/\_   _____/ \      \ \______ \ \______ \   \      \ \_   ___ \\\\_   _____/  /   _____/\__  |   |/   _____/\__    ___/\_   _____/  /     \  
 /  /_\  \|    |     |    |    |    __)_  /   |   \ |    |  \ |    |  \  /   |   \/    \  \/ |    __)_   \_____  \  /   |   |\_____  \   |    |    |    __)_  /  \ /  \ 
/    |    \    |     |    |    |        \/    |    \|    `   \|    `   \/    |    \     \____|        \  /        \ \____   |/        \  |    |    |        \/    Y    \\
\____|__  /____|     |____|   /_______  /\____|__  /_______  /_______  /\____|__  /\______  /_______  / /_______  / / ______/_______  /  |____|   /_______  /\____|__  /
        \/                            \/         \/        \/        \/         \/        \/        \/          \/  \/              \/                    \/         \/    


								    BY: @karim.ashraf, @omar.aboelmagd
""")
import time
time.sleep(0.5)
print("Loading libraries...")
from consolemenu import *
from tabulate import tabulate
from consolemenu.items import *
import mysql.connector
from create_tables import create_tables
from db_interface import *
from cv_code import *
import os

cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1')
cursor = cnx.cursor()
create_tables(cnx, cursor)
time.sleep(1.5)


def list_students_menu():
    table = list_students(cnx, cursor)
    print(tabulate(table, headers=["Student ID", "Name", "Email", "Grade"]))
    print()
    print()
    os.system("pause")

def add_student_menu():
    student_id = int(input("Student ID: "))
    student_name = input("Student Name: ")
    student_email = input("Student Email: ")
    grade = int(input("Student Grade: "))
    
    embedding = get_embedding()
    
    add_student(cnx, cursor, student_id, student_name, student_email, grade, embedding)

    print()
    print()
    print(f"Student {student_id} Added Successfully")
    os.system("pause")


def list_attendance_menu():
    student_id = int(input("Student ID: "))
    table, name = list_attendence(cnx, cursor, student_id)
    print("Showing attendance for student:", name)
    print()
    print(tabulate(table, headers=["Timestamp"]))
    print()
    print()
    os.system("pause")




def monitor_menu():
    print("Starting the Monitoring Process...")
    embeddings = grab_faces(cnx, cursor)
    monitor(cnx, cursor, embeddings)
    os.system("pause")


main_menu = ConsoleMenu("Attendence System - Main Menu")

add_student_menu_item = FunctionItem("Add New Student", add_student_menu)
main_menu.append_item(add_student_menu_item)

list_all_students_menu_item = FunctionItem("List All Students", list_students_menu)
main_menu.append_item(list_all_students_menu_item)

list_attendance_menu_item = FunctionItem("Show Attendence for Student", list_attendance_menu)
main_menu.append_item(list_attendance_menu_item)


monitor_menu_item = FunctionItem("Start Monitoring", monitor_menu)
main_menu.append_item(monitor_menu_item)


main_menu.show()

cursor.close()
cnx.commit()
cnx.close()
