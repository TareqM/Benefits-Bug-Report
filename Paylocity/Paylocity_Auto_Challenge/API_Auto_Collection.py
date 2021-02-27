import requests
import json
from typing import Final
from Constants import BASE_URL
from Constants import HEADER
from Constants import HTTP_SUCCESS

EMPLOYEE_API_URL: Final = BASE_URL + 'api/employees/'

BODY: Final = {
    "firstName": "Natasha",
    "lastName": "Romanoff",
    "dependants": 3
    }

# POST Employee
post_response = requests.post(EMPLOYEE_API_URL, headers=HEADER, json=BODY)
assert post_response.status_code == HTTP_SUCCESS

# GET_Employee list
employee_list = requests.get(EMPLOYEE_API_URL, headers=HEADER)
assert employee_list.status_code == HTTP_SUCCESS

# Parse Employee id
json_response = json.loads(employee_list.text)

for i in json_response:
    if i['firstName'] == 'Natasha':
        id = i['id']
        break

# GET Employee
url_id = EMPLOYEE_API_URL + id
get_natasha = requests.get(url_id, headers=HEADER)
assert get_natasha.status_code == HTTP_SUCCESS

# PUT employee
update_data = {
    'id': id,
    'firstName': 'Wanda',
    'lastName': 'Maximoff',
    'dependants': 2
    }

update_employee = requests.put(EMPLOYEE_API_URL, headers=HEADER, json=update_data)
assert update_employee.status_code == HTTP_SUCCESS

# DELETE Employee
del_employee = requests.delete(url_id, headers=HEADER)
assert del_employee.status_code == HTTP_SUCCESS