from flask_sqlalchemy import SQLAlchemy

#Creating an SQLAlchemy instance
db = SQLAlchemy()

#SQLAlchemy - use classes to create db structure
#Create student model
class Student(db.Model):
    __tablename__ = 'student'
    # Define the columns of the Students table
    st_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    grade = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        return {
            'st_id': self.st_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'grade': self.grade
        }
    # this method depics how one object will look like in the table
    def __repr__(self):
        return f"<Student First Name: {self.first_name}, Last Name: {self.last_name}, Age: {self.age}, Grade: {self.grade}>"

    
