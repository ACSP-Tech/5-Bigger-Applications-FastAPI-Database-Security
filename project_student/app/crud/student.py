from ..model.user_management import Student, Grade
from ..model.user_management import User
from ..sec import pwd_context, SECRET_KEY, ALGORITHM
from fastapi import HTTPException, status
from sqlmodel import select
import jwt
from sqlalchemy import and_


def create_student(data, session, token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        id = payload.get("id")
        #get a single user
        statement = select(User).where(and_(User.email == email, User.id == id)) 
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        statement = select(Student).where(and_(Student.email == data.email.lower().strip(), 
                                               Student.user_id == id))
        student = session.exec(statement).first()  
        if student:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="student details already already exist for this user"
            )    
        # Create student
        new_student = Student(name=data.name, age=data.age, email=data.email, user_id=id)
        # Add grades
        for g in data.grades:
            grade = Grade(subject=g.subject, score=g.score)
            new_student.grades.append(grade)

        session.add(new_student)
        session.commit()
        session.refresh(new_student)
        return new_student
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )
    
def add_to_grade(data, session, token, studentid):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        id = payload.get("id")
        #get a single user
        statement = select(User).where(and_(User.email == email, User.id == id)) 
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        statement = select(Student).where(and_(Student.user_id == id, Student.id == studentid))
        student = session.exec(statement).first()  
        if not student:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="student details not found for this user"
            )   
        
        grade = Grade(subject=data.subject, score=data.score, student_id = studentid)
        #special function that add to a table
        session.add(grade)
        session.commit()
        session.refresh(grade)
        return grade
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#no authentication require to view according to instructions    
def all_student(session):
    try:
        statement = select(Student)
        student = session.exec(statement).all()#eexecute that takes in conditions .all()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no student profile has been added yet"
            )
        return student 
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#no authentication also    
def filter_grade_by_studentid(studentid, session):
    try:
        #get all grade that match the studentid in the path parameter
        statement = select(Grade).where(Grade.student_id == studentid)
        grade = session.exec(statement).all() #eexecute that takes in conditions .all()
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="student id not found"
            )
        return grade
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
def update_student(data, studentid, token, session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        id = payload.get("id")
        #get a single user
        statement = select(User).where(and_(User.email == email, User.id == id)) 
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        #get a single user
        statement = select(Student).where(and_(Student.id == studentid, 
                                               Student.user_id == id))
        student = session.exec(statement).first()   #execute that takes in conditions .all()
        if student:
            student.name = data.name
            student.age = data.age
            #session add
            session.commit()
            session.refresh(student)
            return student
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="unable to update student for this user"
            )
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
def update_record(studentid, data, token, session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        id = payload.get("id")
        #get a single user
        statement = select(User).where(and_(User.email == email, User.id == id)) 
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        #get a single user
        statement = select(Student).where(and_(Student.user_id == id, Student.id == studentid))
        student = session.exec(statement).first()  
        if not student:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="student id details not found for this user"
            )
        statement = select(Grade).where(and_(Grade.id == data.id, Grade.student_id == studentid))
        grade=session.exec(statement).first()
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="grade id details not found for this student"
            )
        grade.subject = data.subject
        grade.score = data.score
        session.commit()
        session.refresh(grade)
        return grade
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
def delete_student(studentid, token, session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        id = payload.get("id")
        #get a single user
        statement = select(User).where(and_(User.email == email, User.id == id)) 
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        #get a single user
        statement = select(Student).where(and_(Student.user_id == id, Student.id == studentid)) 
        student = session.exec(statement).first() #execute that takes in conditions .all()
        if student:
            session.delete(student)
            session.commit()
            res = {
                "message": f"student with {studentid} student id has been successfully deleted"
            }
            return res
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="can't delete record you did not create"
            )
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))