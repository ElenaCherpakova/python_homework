import sqlite3


def add_student(cursor, name, age, major):
    try:
        cursor.execute(
            "INSERT INTO Students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database.")


def add_course(cursor, name, instructor):
    try:
        cursor.execute(
            "INSERT INTO Courses (course_name, instructor_name) VALUES (?, ?)", (name, instructor))
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database.")


def enroll_student(cursor, student, course):
    # For a tuple with one element, you need to include the comma
    cursor.execute("SELECT * FROM Students WHERE name = ?", (student,))
    results = cursor.fetchall()
    if len(results) > 0:
        student_id = results[0][0]
    else:
        print(f"There was no student named {student}.")
        return
    cursor.execute("SELECT * FROM Courses WHERE course_name = ?", (course,))
    results = cursor.fetchall()
    if len(results) > 0:
        course_id = results[0][0]
    else:
        print(f"There was no course named {course}.")
        return
    cursor.execute(
        "SELECT * FROM Enrollments WHERE student_id = ? AND course_id = ?", (student_id, course_id))
    results = cursor.fetchall()
    if len(results) > 0:
        print(f"Student {student} is already enrolled in course {course}.")
        return
    cursor.execute(
        "INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))

with sqlite3.connect('../db/school.db') as conn:
    # This turns on the foreign key constraint
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    # Insert sample data into tables

    add_student(cursor, 'Alice', 20, 'Computer Science')
    add_student(cursor, 'Bob', 22, 'History')
    add_student(cursor, 'Charlie', 19, 'Biology')
    add_course(cursor, 'Math 101', 'Dr. Smith')
    add_course(cursor, 'English 101', 'Ms. Jones')
    add_course(cursor, 'Chemistry 101', 'Dr. Lee')

    enroll_student(cursor, "Alice", "Math 101")
    enroll_student(cursor, "Alice", "Chemistry 101")
    enroll_student(cursor, "Bob", "Math 101")
    enroll_student(cursor, "Bob", "English 101")
    enroll_student(cursor, "Charlie", "English 101")

    conn.commit()
    print("Sample data inserted successfully.")

    cursor.execute("SELECT * FROM Students WHERE name = 'Alice'")
    results = cursor.fetchall()
    for row in results:
        print(row)

    cursor.execute('SELECT * FROM Courses WHERE course_name LIKE "math%"')
    results = cursor.fetchall()
    for row in results:
        print(f'math here{row}')
    cursor.execute("SELECT Students.name, Courses.course_name FROM Students JOIN Enrollments ON Students.student_id = Enrollments.student_id JOIN Courses ON Enrollments.course_id = Courses.course_id")
    results = cursor.fetchall()
    for row in results:
        print(row)
        
    cursor.execute("SELECT s.name, c.course_name FROM Students AS s JOIN Enrollments AS e ON s.student_id = e.student_id JOIN Courses AS c ON e.course_id = c.course_id")
    results = cursor.fetchall()
    for row in results:
        print(row)
        
    cursor.execute("SELECT Students.name, Courses.course_name FROM Enrollments JOIN Students ON Enrollments.student_id = Students.student_id JOIN Courses ON Enrollments.course_id = Courses.course_id")
    results = cursor.fetchall()
    for row in results:
        print(row)
        
    cursor.execute("UPDATE Students SET name='Charles', age=20 WHERE name ='Charlie'")
    if cursor.rowcount > 0:
        print("Student 'Charlie' was successfully updated to 'Charles'.")
    else:
        print("No student named 'Charlie' was found to update.")