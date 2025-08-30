# importing the necessary requirement
from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.student import StudentCreate, StudentRead, GradeCreate, GradeRead, StudentUpdate
from ..sec import pwd_context, SECRET_KEY, ALGORITHM
from app.utils import check_filepath
from ..dep import auth, get_session
from ..crud.student import create_student, add_to_grade, all_student, filter_grade_by_studentid, update_student, update_record, delete_student
import json

router = APIRouter()

@router.post("/students/create-student", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student_with_grades(data:StudentCreate, session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to student
        message = create_student(data, session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/students/add-grade/{studentid}", response_model=GradeRead, status_code=status.HTTP_201_CREATED)
def add_new_grade_to_student(studentid: int, data:GradeCreate, session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to grade
        message = add_to_grade(data, session, token, studentid)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/students/view-student", status_code=status.HTTP_200_OK)
def view_all_student(session=Depends(get_session)):
    try:
        #inteaction with database and show all students on the database
        message = all_student(session)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/students/view-student-grade/{studentid}", status_code=status.HTTP_200_OK)
def view_student_grade(studentid: int, session=Depends(get_session)):
    try:
        #inteaction with database and show all students on the database
        message = filter_grade_by_studentid(studentid, session)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.patch("/students/update-student-info/{studentid}", status_code=status.HTTP_200_OK)
def update_student_record(data:StudentUpdate, studentid:int, token=Depends(auth), session=Depends(get_session)):
    try:
        student = update_student(data, studentid, token, session)
        return student
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.patch("/students/update-student-grade-info/{studentid}", status_code=status.HTTP_200_OK)
def update__grade_record(studentid: int, data:GradeRead, token=Depends(auth), session=Depends(get_session)):
    try:
        grade = update_record(studentid, data, token, session)
        return grade
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/students/delete-student-grade-info/{studentid}", status_code=status.HTTP_200_OK)
def delete_student_record(studentid:int, token=Depends(auth), session=Depends(get_session)):
    try:
        deleted = delete_student(studentid, token, session)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))