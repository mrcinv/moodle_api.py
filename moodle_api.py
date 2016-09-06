from requests import get, post
# Module variables to connect to moodle api
KEY = "SECRET API KEY"
URL = "https://moodle.site.com"
ENDPOINT="/webservice/rest/server.php"

def rest_api_parameters(in_args, prefix='', out_dict={}):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.

    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
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

def call_mdl_function(fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.

    Example: 
    >>> call_mdl_function('core_course_update_courses',courses=[{'id':1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    print(parameters)
    parameters.update({"wstoken": KEY,'moodlewsrestformat':'json', "wsfunction": fname})
    response = post(URL+ENDPOINT, parameters)
    return response.json()


class Course():
    """Class representing moodle course."""
