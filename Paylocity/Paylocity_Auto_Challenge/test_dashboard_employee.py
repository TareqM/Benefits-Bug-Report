import requests
import json
from typing import Final
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from Constants import BASE_URL, HEADER, HTTP_SUCCESS
from User import User


def test_employee_api_collection():
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


def test_add_employee():
    LOGIN_URL: Final = BASE_URL + 'Account/LogIn'
    DOM_ROW: Final = "tr"
    DOM_COL: Final = "td"
    EMPLOYEE_BENEFIT_COST_YEAR: Final = 1000.00
    DEPENDENT_BENEFIT_COST_YEAR: Final = 500.00
    PAYCHECKS_YEAR: Final = 26.00
    EMPLOYEE_BENEFIT_COST_PAYCHECK: Final = EMPLOYEE_BENEFIT_COST_YEAR / PAYCHECKS_YEAR
    DEPENDENT_BENEFIT_COST_PAYCHECK: Final = DEPENDENT_BENEFIT_COST_YEAR / PAYCHECKS_YEAR

    def get_table_rows(table):
        return table.find_elements(By.TAG_NAME, DOM_ROW)

    def get_table_columns(table):
        return table.find_elements(By.TAG_NAME, DOM_COL)

    driver = webdriver.Chrome(executable_path="C:\driver101\chromedriver_win32\chromedriver.exe")
    driver.get(LOGIN_URL)
    # Log in
    driver.find_element_by_id('Username').send_keys(User.USER_NAME)
    driver.find_element_by_id('Password').send_keys(User.PASSWORD)
    driver.find_element_by_xpath('/html/body/div/main/div/div/form/button').click()
    # Add Employee
    driver.find_element_by_id('add').click()
    driver.find_element_by_id('firstName').send_keys(User.FIRST_NAME)
    driver.find_element_by_id('lastName').send_keys(User.LAST_NAME)
    driver.find_element_by_id('dependants').send_keys(1)
    driver.find_element_by_id('addEmployee').click()
    time.sleep(3)
    employees_table = driver.find_element(By.XPATH, '//*[@id="employeesTable"]/tbody')
    employees = get_table_rows(employees_table)
    for employee in employees:
        employee_data = get_table_columns(employee)
        first_name = employee_data[1].text
        last_name = employee_data[2].text
        dependents = int(employee_data[3].text)
        salary = float(employee_data[4].text)
        gross_pay = float(employee_data[5].text)
        benefits_cost = float(employee_data[6].text)
        net_pay = float(employee_data[7].text)
        if first_name == User.FIRST_NAME:
            assert employee_data[1].is_displayed()
            assert round(EMPLOYEE_BENEFIT_COST_PAYCHECK + DEPENDENT_BENEFIT_COST_PAYCHECK * dependents,
                         2) == benefits_cost