from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edutrack.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.String(10), nullable=False)

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = Student(name=data['name'], age=data['age'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'id': new_student.id}), 201

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'age': s.age} for s in students])

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    student = Student.query.get(id)
    if student:
        student.name = data['name']
        student.age = data['age']
        db.session.commit()
        return jsonify({'id': student.id}), 200
    return jsonify({'message': 'Student not found'}), 404

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted'}), 200
    return jsonify({'message': 'Student not found'}), 404

@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    new_course = Course(title=data['title'], description=data['description'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'id': new_course.id}), 201

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{'id': c.id, 'title': c.title, 'description': c.description} for c in courses])

@app.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    data = request.get_json()
    course = Course.query.get(id)
    if course:
        course.title = data['title']
        course.description = data['description']
        db.session.commit()
        return jsonify({'id': course.id}), 200
    return jsonify({'message': 'Course not found'}), 404

@app.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get(id)
    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'message': 'Course deleted'}), 200
    return jsonify({'message': 'Course not found'}), 404

@app.route('/grades', methods=['POST'])
def create_grade():
    data = request.get_json()
    new_grade = Grade(student_id=data['student_id'], course_id=data['course_id'], grade=data['grade'])
    db.session.add(new_grade)
    db.session.commit()
    return jsonify({'id': new_grade.id}), 201

@app.route('/grades', methods=['GET'])
def get_grades():
    grades = Grade.query.all()
    return jsonify([{'id': g.id, 'student_id': g.student_id, 'course_id': g.course_id, 'grade': g.grade} for g in grades])

@app.route('/grades/<int:id>', methods=['PUT'])
def update_grade(id):
    data = request.get_json()
    grade = Grade.query.get(id)
    if grade:
        grade.grade = data['grade']
        db.session.commit()
        return jsonify({'id': grade.id}), 200
    return jsonify({'message': 'Grade not found'}), 404

@app.route('/grades/<int:id>', methods=['DELETE'])
def delete_grade(id):
    grade = Grade.query.get(id)
    if grade:
        db.session.delete(grade)
        db.session.commit()
        return jsonify({'message': 'Grade deleted'}), 200
    return jsonify({'message': 'Grade not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)