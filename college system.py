import mysql.connector as mysql

db = mysql.connect(host="localhost", user="root", password="",database="college")

command_handler = db.cursor(buffered=True)

def student_session(username):
    print("Login successful")
    print("")
    print("Welcome to the student session")
    while 1:
        print("")
        print("Student Menu")
        print("1. View Register....")
        print("2. Download Register...")
        print("3. Logout")
        
        user_option = str(input("Option:"))
        if user_option == "1":
            print("")
            print("View Register")
            username = (str(username),)
            command_handler.execute("SELECT username,date,status FROM attendance WHERE username = %s", username)
            records = command_handler.fetchall()
            print("Displaying the records")
            for record in records:
                print(record)

        elif user_option == "2":
            print("")
            print("Download Register")
            username = (str(username),)
            command_handler.execute("SELECT username,date,status FROM attendance WHERE username = %s", username)
            records = command_handler.fetchall()
            print("Downloading the records")
            for record in records:
                with open("register.txt", "w") as f:
                    f.write(str(records)+"\n")
                f.close()
            print("Download Complete")
        
        elif user_option == "3":
            print("")
            print("Logout is successful")
            break

        else:
            print("")
            print("Invalid option")

def teacher_session():
    print("Login successful")
    print("")
    print("Welcome to the teacher session")
    while 1:
        print("")
        print("Teacher Menu")
        print("1. Mark Student Register....")
        print("2. View Register...")
        print("3. Logout")

        user_option = str(input("Option:"))
        if user_option == "1":
            print("")
            print("Mark Student Register")
            command_handler.execute("SELECT username FROM users WHERE privilege = 'student'")
            records = command_handler.fetchall()
            date = str(input("Date : DD/MM/YYYY : "))

            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")

                status = str(input("Status for : " + str(record) + " P/A/L : "))
                query_vals = (str(record), date, status)
                command_handler.execute("INSERT INTO attendance (username,date,status) VALUES (%s, %s, %s)", query_vals)
                db.commit()
                print(record + " has been marked as " + status)

        elif user_option == "2":
            print("")
            print("View Register")
            command_handler.execute("SELECT username,date,status FROM attendance")
            records = command_handler.fetchall()
            print("Displaying all records")
            for record in records:
                print(record)

        elif user_option == "3":
            print("")
            print("Logout is successful")
            break
        
        else:
            print("")
            print("Invalid option")


def admin_session():
    print("Login successful")
    print("")
    print("Welcome to the admin session")
    while 1:
        print("")
        print("Admin Menu")
        print("1. Register new Student....")
        print("2. Register new Teacher...")
        print("3. Delete existing Student...")
        print("4. Delete existing Teacher...")
        print("5. Delete existing attendances...")
        print("6. Logout")

        user_option = str(input("Option:"))
        if user_option == "1":
            print("Register new Student")
            username = str(input("Student username:"))
            password = str(input("Student password:"))
            query_vals = (username, password)
            command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s, %s,'student')", query_vals)
            db.commit()
            print(username + " has been registered as student")
        
        elif user_option == "2":
            print("Register new Teacher")
            username = str(input("Teacher username:"))
            password = str(input("Teacher password:"))
            query_vals = (username, password)
            command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s, %s,'teacher')", query_vals)
            db.commit()
            print(username + " has been registered as teacher")

        elif user_option == "3":
            print("")
            print("Delete Existing Student Account")
            username = str(input("Student username:"))
            query_vals = (username, "student")
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege =%s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print(username + " does not exist")
            else:
                print(username + " has been deleted")

        elif user_option == "4":
            print("")
            print("Delete Existing Teacher Account")
            username = str(input("Teacher username:"))
            query_vals = (username, "teacher")
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege =%s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print(username + " does not exist")
            else:
                print(username + " has been deleted")

        elif user_option == "5":
            print("")
            print("Delete Existing Attendances")
            username = str(input("Student username:"))
            date = str(input("Date: "))
            query_vals = (username, date)
            command_handler.execute("DELETE FROM attendance WHERE username = %s AND date = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print(username + " does not exist")
            else:
                print(username + " attendance has been deleted")

        elif user_option == "6":
            print("")
            print("Logout is successful")
            break

        else:
            print("Invalid option")

def auth_student():
    print("")
    print("Student Login")
    print("")
    username = str(input("Username: "))
    password = str(input("Password: "))
    query_vals = (username, password)
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege ='student'", query_vals)
    if command_handler.rowcount <= 0:
        print("Invalid Login")
    else:
        student_session(username)

def auth_teacher():
    print("")
    print("Teacher Login")
    print("")
    username = str(input("Username: "))
    password = str(input("Password: "))
    query_vals = (username, password)
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = 'teacher'", query_vals)
    if command_handler.rowcount <= 0:
        print("Invalid Login")
    else:
        teacher_session()

def auth_admin():
    print("")
    print("Administrator Login")
    print("")
    username = str(input("Username: "))
    password = str(input("Password: "))
    if username == "admin":
        if password == "password":
            admin_session()
        else:
            print("Invalid password")
    else:
        print("Invalid Login")


def main():
    while 1:
        print("")
        print("Welcome to the college management system")
        print("")
        print("1. Login as a Student...")
        print("2. Login as a Teacher...")
        print("3. Login as a Administrator...")

        user_option = str(input("Option:"))

        if user_option == "1":
            auth_student()
        elif user_option == "2":
            auth_teacher()
        elif user_option == "3":
            auth_admin()
        else:
            print("Invalid option")

main()