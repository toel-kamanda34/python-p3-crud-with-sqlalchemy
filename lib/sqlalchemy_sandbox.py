#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='id_pk'
        ),
        UniqueConstraint(
            'email',
            name='unique_email'
        ),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12'
        )
    )

    Index('index_name', 'name')

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String(55))
    grade = Column(Integer)
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())


  #  id = Column(Integer, primary_key=True)
  #  name = Column(String)
    def __repr__(self):
        return f"Student {self.id}: "\
        + f"{self.name}, "\
        + f"Grade {self.grade}"

if __name__ == '__main__':  
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    #session.add(albert_einstein)
    #session.commit()
    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    print(f"New Student ID is {albert_einstein.id}.")
    print(f"New student ID is {alan_turing.id}.")
    
    #session query instance method
    
    students = session.query(Student)

    print([student for student in students]) 
    
    #query using all instance method
    
    students = session.query(Student).all()
    print(students)
    
    #selecting names column
    names = [name for name in session.query(Student.name)]

    print(names)

    #ordering using order_by() method
    students_by_name = [student for student in session.query(
        Student.name).order_by(
        Student.name)]
    
    print(students_by_name)

    #sorting in descending order using the desc()
    students_by_grade_desc = [student for student in session.query(
        Student.name, Student.grade).order_by(
        desc(Student.grade))]
    
    print(students_by_grade_desc)

    #using limit() method to limit the result to 1

    oldest_student = [student for student in session.query(
        Student.name, Student.birthday).order_by(
        Student.birthday).limit(1)]
    
    print(oldest_student)

    #using first() method instead of limit(1)
    oldest_student = session.query(
        Student.name, Student.birthday).order_by(
        Student.birthday).first()

    print(oldest_student)   

    #common sql operations gotten from iporting func

    student_count = session.query(func.count(Student.id)).first()

    print(student_count)

    #filtering a typical filter() statement has a column, a standard operator and a value
    query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11)
    
    for record in query:
        print(record.name)

    #updating data

    for student in session.query(Student):
        student.grade += 1

    session.commit()

    print([(student.name,
            student.grade) for student in session.query(Student)])
    
    #update method allows us to update records without creating records beforehad
    session.query(Student).update({
        Student.grade: Student.grade - 1
    })

    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])

    #using delete() method to delete a record
    #create session, student objects

    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")

    #retrieve the first matching record as an object
    albert_einstein = query.first()

    #delete recors
    session.delete(albert_einstein)
    session.commit()

    #try to retrieve deleted record
    albert_einstein = query.first()

    print(albert_einstein) 

    #calling the delete and deleting all the records returned by query
    query = session.query(
        Student).filter(Student.name =="Albert Einstein"
    )

    query.delete()

    albert_einstein = query.first()

    print(albert_einstein)


