import os
from flask import Flask, request, jsonify
from models import db, Student  

app = Flask(__name__)

# Configure the database URI (use SQLite for this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'

# Initialize the database
db.init_app(app)

# Create tables before first request (if not already created)
@app.before_request
def create_tables():
    if not os.path.exists('students.db'):
        with app.app_context():
            db.create_all()
            print("DB CREATED")

# 1. Get all students
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()  # Get all students from the database
    return jsonify([student.to_dict() for student in students])  # Convert to dict and return as JSON

# 2. Insert a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    age = data.get('age')
    grade = data.get('grade')

    if not first_name or not last_name or not age or not grade:
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new student and add to the session
    new_student = Student(first_name=first_name, last_name=last_name, age=age, grade=grade)
    db.session.add(new_student)
    db.session.commit()  # Commit the transaction

    return jsonify({"message": "Student added successfully"}), 201

# 3. Update a student's information
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = Student.query.get(student_id)  # Get student by ID

    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Update fields
    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.age = data.get('age', student.age)
    student.grade = data.get('grade', student.grade)

    db.session.commit()  # Commit the changes

    return jsonify({"message": "Student updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
