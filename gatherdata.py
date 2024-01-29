from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass
import csv

INSTANCE_URL = "https://url goes here.atlassian.net/" #REPLACE WITH YOUR ATLASSIAN CLOUD URL
PROJECT_ORGANIZATION_URL = "jira/servicedesk/projects/PROJECT GOES HERE/organization/"

def employee():
    urls = ["10", "11", "12"] #Replace with organization ids
    print("Writing emails to file", end = "", flush = True)
    for url in urls:
        driver.get(INSTANCE_URL + PROJECT_ORGANIZATION_URL + url)
        while True:
            with open('email_list.csv', 'a', encoding='utf-8-sig', newline='') as csv_file:
                writer = csv.writer(csv_file)
                WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'//span[contains(@class, "e4whrk-1 kPLknu e4whrk-0 frsmgf")]')))
                time.sleep(5)
                for user in driver.find_elements(By.XPATH,'//span[contains(@class, "e4whrk-1 kPLknu e4whrk-0 frsmgf")]'):
                    writer.writerow([user.text.strip()])
                    print(".", end = "", flush = True)
            try:
                elem = driver.find_element(By.XPATH,'//button[@data-testid="servicedesk-customers-organization-common.ui.table.bracket-pagination.right-button"]')
                if elem.is_enabled():
                    elem.click()
                else:
                    break
            except:
                break
    csv_file.close()
    print("DONE!", end = "", flush = True)
    print()

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

        print("Finished writing!")
        driver.quit()
        exit()
    else:
        exit()