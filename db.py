import json  

class Course():
    id = int
    name = str
    date = int
    description = str
    domain = list[str]
    chapters = list[dict[str, str]]
    rating = dict[str, int] | None

def read_file():
    with open("course.json") as file:
        data = json.load(file)
        return data
    
def find_course(id: int):
    courses = read_file()
    selected_course = None
    for course in courses:
        if course['id'] == id:
            selected_course = course
    return selected_course

def update(id: int, data: tuple([str, dict[str, int]])):   
    courses = read_file()  
    for current_course in courses:
        if current_course['id'] == id:
            key, value = data
            current_course[key] = value
    with open("course.json", 'w') as file:
        json.dump(courses, file, indent=4)
        
def sort(sort_by: str, data):
    # sort_by == 'date' [DESCENDING]
    if sort_by == 'date':
        sort_field = 'date'
        sort_order = -1

    # sort_by == 'rating' [DESCENDING]
    elif sort_by == 'rating':
        sort_field = 'rating.total'
        sort_order = -1

    # sort_by == 'alphabetical' [ASCENDING]
    else:  
        sort_field = 'name'
        sort_order = 1

    query = {}
    if domain:
        query['domain'] = domain


    courses = db.courses.find(query, {'name': 1, 'date': 1, 'description': 1, 'domain':1,'rating':1,'_id': 0}).sort(sort_field, sort_order)
    return list(courses)
        