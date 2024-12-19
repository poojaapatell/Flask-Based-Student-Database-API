import unittest
from app import app, db
from models import Student
import json

class StudentAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all() 
    
    def test_add_student_missing_fields(self):
        student_data = {
            "first name": "Sally",
            "last_name": "Shore",
            "grade": 10
        }

        response = self.client.post('/students', json=student_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Missing required fields')

    
    def test_get_students(self):
        student_data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 18,
            "grade": 12
        }
        self.client.post('/students', json=student_data)
        
        response = self.client.get('/students')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['first_name'], 'John')
        self.assertEqual(data[0]['last_name'], 'Doe')
    
    def test_update_student(self):
        student_data = {
        "first_name": "Bob",
        "last_name": "Johnson",
        "age": 18,
        "grade": 75
        }
    
        response = self.client.post('/students', json=student_data)
        self.assertEqual(response.status_code, 201)
    
        with self.app.app_context():
            student = Student.query.filter_by(first_name="Bob").first()
    
        self.assertIsNotNone(student)

        update_data = {
        "first_name": "Bobby",  
        "last_name": "Johnson",
        "age": 18,
        "grade": 80
        }

        response = self.client.put(f'/students/{student.st_id}', json=update_data)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            updated_student = Student.query.get(student.st_id)
    
        self.assertEqual(updated_student.first_name, "Bobby")
        self.assertEqual(updated_student.grade, 80)


    def test_update_student_not_found(self):
        update_data = {
            "first_name": "NonExisting",
            "last_name": "Student",
            "age": 99,
            "grade": 99
        }
        response = self.client.put('/students/99999', json=update_data)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Student not found')

if __name__ == '__main__':
    unittest.main()


