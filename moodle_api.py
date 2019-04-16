from requests import get, post
# Module variables to connect to moodle api
KEY = "SECRET API KEY"
URL = "https://moodle.site.com"
ENDPOINT="/webservice/rest/server.php"

def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.

    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict==None:
        out_dict = {}
    if not type(in_args) in (list,dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args)==list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args)==dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict

def call(fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.

    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update({"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
    response = post(URL+ENDPOINT, parameters)
    response = response.json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response

class CourseList():
    """Class for list of all courses in Moodle and order them by id and idnumber."""
    def __init__(self):
        # TODO fullname atribute is filtered
        # (no <span class="multilang" lang="sl">)
        courses_data = call('core_course_get_courses')
        self.courses = []
        for data in courses_data:
            self.courses.append(Course(**data))
        self.id_dict = {}
        self.idnumber_dict = {}
        for course in self.courses:
            self.id_dict[course.id] = course
            if course.idnumber:
                self.idnumber_dict[course.idnumber] = course
    def __getitem__(self, key):
        if 0<= key < len(self.courses):
            return self.courses[key]
        else:
            raise IndexError
                
    def by_id(self, id):
        "Return course with given id."
        return self.id_dict.get(id)
    
    def by_idnumber(self, idnumber):
        "Course with given idnumber"
        return self.idnumber_dict.get(idnumber)
    
    def update_courses(courses_to_update, fields):
        "Update a list of courses in one go."
        if not ('id' in fields):
            fields.append('id')
        courses = [{k: c.__dict__[k] for k in fields} for c in courses_to_update]
        return call("core_course_update_courses", 
             courses = courses)
    
class Course():
    """Class for a single course.
    
    Example:
    >>> Course(name="Example course", shortname="example", categoryid=1, idnumber=123)
    """
    def __init__(self, **data):
        self.__dict__.update(data)
        
    def create(self):
        "Create this course on moodle"
        res = call('core_course_create_courses', courses = [self.__dict__])
        if type(res) == list:
            self.id = res[0].get('id')
    
    def update(self):
        "Update course"
        r = call('core_course_update_courses', courses = [self.__dict__])
    
    
class User():
    """Class for a single user.
    
    Example:
    >>> User(name="Janez", surname="Novak", email="janez.novak@student.si", username="jnovak", password="sila varno geslo")"""
    
    def __init__(self, **data):
        self.__dict__.update(data)
    
    def create(self):
        "Create new user on moodle site"
        valid_keys = ['username', 
                      'firstname', 
                      'lastname', 
                      'email', 
                      'auth',
                      'idnumber',
                      'password']
        values = {key: self.__dict__[key] for key in valid_keys}
        res = call('core_user_create_users', users = [values])
        if type(res) == list:
            self.id  = res[0].get('id')
            
    def update(self, field=None):
        "Upadte user data on moodle site"
        if field:
            values = {"id": self.id, field: self.__dict__[field]}
        else:
            values = self.__dict__
        r = call('core_user_update_users', users = [values])
    
    def get_by_field(self, field='username'):
        "Create new user if it does not exist, otherwise update data"
        res = call('core_user_get_users_by_field', field = field, values = [self.__dict__[field]])
        if (type(res) == list) and len(res) > 0:
            self.__dict__.update(res[0])
            return self
        else:
            return None
    def create_or_get_id(self):
        "Get Moodle id of the user or create one if it does not exists."
        if not self.get_by_field():
            self.create()

    def enroll(self, roleid=5):
        "Enroll users in courses with specific role"
        if len(self.courses)<=0:
            return None
        enrolments = []
        for course in self.courses:
            enrolments.append({'roleid': roleid, 'userid': self.id, 'courseid': course.id})
        r = call('enrol_manual_enrol_users', enrolments = enrolments)
        return r

    def enrolments(self, m_courses):
        "Get moodle courses, the user has to enroll"
        self.courses = []
        for idnumber in self.course_idnumbers:
            course = m_courses.by_idnumber(idnumber)
            if course:
                self.courses.append(course)
        return self.courses
                
class Cathegory():
    pass

class Enrolments():
    pass