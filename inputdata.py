from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass
import csv

INSTANCE_URL = "https://url goes here.atlassian.net/" #REPLACE WITH YOUR ATLASSIAN CLOUD URL

def employee():
    driver.get(INSTANCE_URL + "jira/servicedesk/projects/project goes here/organization/organization id goes here")
    with open('email_list.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data_list = list(csv_reader)
        grouped_lists = [data_list[i:i + 10] for i in range(0, len(data_list), 10)]
        for sublist in grouped_lists:
            WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'//button[@data-testid="servicedesk-customers-organization-common.ui.add-customers-dialog.button"]')))
            driver.find_element(By.XPATH,'//button[@data-testid="servicedesk-customers-organization-common.ui.add-customers-dialog.button"]').click()
            for item in sublist:
                WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'//textarea[@data-testid="servicedesk-customers-organization-common.common.ui.multiline-text.dynamic-input"]')))
                driver.find_element(By.XPATH,'//textarea[@data-testid="servicedesk-customers-organization-common.common.ui.multiline-text.dynamic-input"]').click()
                driver.find_element(By.XPATH,'//textarea[@data-testid="servicedesk-customers-organization-common.common.ui.multiline-text.dynamic-input"]').send_keys(str(item[0]))
                driver.find_element(By.XPATH,'//button[@data-testid="servicedesk-customers-organization-common.ui.add-customers-dialog.form.fields.dynamic-input-field.add-more-button"]').click()
                time.sleep(.5)
            time.sleep(.5)
            driver.find_element(By.XPATH,'//button[@data-testid="servicedesk-customers-organization-common.common.ui.inline-dialog.footer-controls.submit-button"]').click()
            time.sleep(3)
            driver.refresh()
    csv_file.close()
    

if __name__ == "__main__":
    email_id = input("Email ID : ")
    pw = getpass.getpass("Password : ")

    if email_id != '' and pw != '':
        try:
            options = webdriver.ChromeOptions()
            #options.add_argument("--headless=new") #Remove the comment for headless
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(e)
            exit()

        driver.get(INSTANCE_URL)
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID,'username')))
        driver.find_element(By.ID,'username').send_keys(email_id)
        driver.find_element(By.ID,'login-submit').click()
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID,'password')))
        driver.find_element(By.ID,'password').send_keys(pw)
        driver.find_element(By.ID,'login-submit').click()
        time.sleep(5)

        employee()

        print("Finished importing!")
        driver.quit()
        exit()
    else:
        exit()