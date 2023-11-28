import contextlib
from enum import Enum
from typing import Union, Annotated
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from db import read_file, update, find_course

app = FastAPI()
# client = MongoClient('mongodb://localhost:27017/')
# db = client['courses']
db = read_file()

class SortTypes(str, Enum):
    alphabetical = "alphabetical"
    date = "date"
    rating = "rating"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/courses")
async def get_courses(sort_by: Annotated[str, SortTypes] = 'date', domain: str = None):
    # set the rating.total and rating.count to all the courses based on the sum of the chapters rating
    all_courses = read_file()
    for course in all_courses:
        total = 0
        count = 0
        for chapter in course['chapters']:
            with contextlib.suppress(KeyError):
                total += chapter['rating']['total']
                count += chapter['rating']['count']
        # db.courses.update_one({'_id': course['_id']}, {'$set': {'rating': {'total': total, 'count': count}}})
        # update(course['id'], {'rating': {'total': total, 'count': count}})
        update(course['id'], tuple(['rating', {'total': total, 'count': count}]))
    # # sort_by == 'date' [DESCENDING]
    # if sort_by == 'date':
    #     sort_field = 'date'
    #     sort_order = -1

    # # sort_by == 'rating' [DESCENDING]
    # elif sort_by == 'rating':
    #     sort_field = 'rating.total'
    #     sort_order = -1

    # # sort_by == 'alphabetical' [ASCENDING]
    # else:  
    #     sort_field = 'name'
    #     sort_order = 1

    # query = {}
    # if domain:
    #     query['domain'] = domain


    # courses = db.courses.find(query, {'name': 1, 'date': 1, 'description': 1, 'domain':1,'rating':1,'_id': 0}).sort(sort_field, sort_order)
    # return list(courses)
    return read_file()

@app.get("/courses/{course_id}")
async def get_course(course_id: int):
    # course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0, })
    course = find_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    return course
    

@app.get("/courses/{course_id}/{chapter_id}")
async def get_chapter(course_id: int, chapter_id: int):
    # course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0, })
    course = find_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    chapters = course.get('chapters', [])
    try:
        chapter = chapters[int(chapter_id)]
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail='Chapter not found') from e
    return chapter

@app.post('/courses/{course_id}/{chapter_id}')
def rate_chapter(course_id: int, chapter_id: int, rating: int = Query(..., gt=-2, lt=2)):
    # course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0, })
    course = find_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    chapters = course.get('chapters', [])
    try:
        chapter = chapters[int(chapter_id)]
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail='Chapter not found') from e
    try:
        chapter['rating']['total'] += rating
        chapter['rating']['count'] += 1
    except KeyError:
        chapter['rating'] = {'total': rating, 'count': 1}
    # db.courses.update_one({'_id': ObjectId(course_id)}, {'$set': {'chapters': chapters}})
    update(course['id'], ('chapters', chapters))
    return chapter 
