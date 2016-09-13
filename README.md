# Python client for Moodle Web services
Lightweight client for Moodle REST web services
## Enable Webservices
Go to `Site administration -> Plugins -> Web services -> Overview` and follow the instructions to enable web services 
and generate authorization token. 
## Basic usage
The main function is `moodle_api.call(function_name, **kwargs)` that calls moodle API function with specific name. 

Arguments to API function are passed as keyword arguments for example `courseids=[1,2,3]`, 
`categories=[{'id':1,'name':'Some name'},{'id':2,'name':'Some other name'}]`, ... 

Consult `Site administration -> Plugins -> Web services -> API Documentation` for specific arguments for enabled API functions.
## Example
```python
>>> import moodle_api
>>> moodle_api.URL = "https://my.moodle.site"
>>> moodle_api.KEY = "xxxxx (moodle secret token)"
>>> course5 = moodle_api.call('core_course_get_contents', courseid=5)
>>> course5[0].keys()
dict_keys(['id', 'summary', 'name', 'visible', 'summaryformat', 'modules'])
```
