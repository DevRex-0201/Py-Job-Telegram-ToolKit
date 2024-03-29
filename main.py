import os
import requests
import dotenv
import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta, timezone
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import asyncio
import telegram
from telegram import Bot  # Make sure to import Bot correctly

# Load environment variables
dotenv.load_dotenv()

# Use os.getenv to retrieve environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
UPWORK_USERNAME = os.getenv("UPWORK_USERNAME")
UPWORK_PASSWORD = os.getenv("UPWORK_PASSWORD")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
def login_to_website(driver, username, password, login_url):
    try:
        driver.get(login_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_username')))
        username_field = driver.find_element(By.ID, 'login_username')
        submit_button = driver.find_element(By.ID, 'login_password_continue')

        username_field.send_keys(username)
        submit_button.click()
        time.sleep(5)
        
        password_field = driver.find_element(By.ID, 'login_password')
        submit_button_login = driver.find_element(By.ID, 'login_control_continue')
        password_field.send_keys(password)
        submit_button_login.click()
        
        WebDriverWait(driver, 10).until(EC.url_changes(login_url))
        if "login" not in driver.current_url.lower():
            return True
        time.sleep(10)
    except TimeoutException as e:
        print(f"Login timeout: {e}. Retrying...")
        driver.quit()        
    except Exception as e:
        print(f"Login error: {e}")
        driver.quit()
    return False

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = None  # Define driver outside try-except to ensure it's in scope for quit()

    for attempt in range(3):  # Try twice
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            break  # Exit loop if successful
        except Exception as e:
            if driver:  # Check if driver was initialized
                driver.quit()
            time.sleep(5)  # Wait before retrying
            if attempt == 1:  # Last attempt
                print(f"Failed to initialize driver after 2 attempts: {e}")
                return None  # Return None or raise an exception

    return driver

async def send_mail(content):
    bot = telegram.Bot(TELEGRAM_TOKEN)
    async with bot:
        chat_id = (await bot.get_updates())
        await bot.send_message(text=content, chat_id=TELEGRAM_CHAT_ID)

def main():
    total_proects = []
    while True:       
        driver = init_driver()
        login_url = 'https://www.upwork.com/ab/account-security/login'
        username = UPWORK_USERNAME
        password = UPWORK_PASSWORD

        try:
            driver.get(login_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_username')))
            username_field = driver.find_element(By.ID, 'login_username')
            submit_button = driver.find_element(By.ID, 'login_password_continue')

            username_field.send_keys(username)
            submit_button.click()
            time.sleep(5)
            
            password_field = driver.find_element(By.ID, 'login_password')
            submit_button_login = driver.find_element(By.ID, 'login_control_continue')
            password_field.send_keys(password)
            submit_button_login.click()
            
            WebDriverWait(driver, 10).until(EC.url_changes(login_url))                    
            time.sleep(10)
        except TimeoutException as e:
            print(f"Login timeout: {e}. Retrying...")
            driver.quit() 
            continue       
        except Exception as e:
            print(f"Login error: {e}")
            driver.quit()
            continue
        for index in range(60):
            project_title = ''
            try:
                driver.get("https://www.upwork.com/nx/search/jobs?amount=150-&contractor_tier=1,2,3&hourly_rate=10-&payment_verified=1&q=%28scrap,%20OR%20extraction,%20OR%20python,%20OR%20automation%29&sort=recency&t=0,1")
                time.sleep(5)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-list-container')))
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                div_elements = soup.find_all(attrs={"data-ev-label": "search_results_impression"})
                div_elements = div_elements[::-1]
                for div in div_elements:
                    project_title = div.find('a', class_='up-n-link').text.strip()
                    project_url = "https://www.upwork.com" + div.find('a', class_='up-n-link').get('href')
                    project_posted = div.find(attrs={"data-test": "JobTileHeader"}).find('small').find_all('span')[1].text.replace('\n', '').strip()
                    jst_timezone = timezone(timedelta(hours=9))
                    # Get the current date and time in JST
                    current_date_time_jst = datetime.now(jst_timezone)
                    # Format the date and time
                    posted_time = current_date_time_jst.strftime("%m-%d %H:%M")
                    if div.find(attrs={"data-test": "total-spent"}):
                        project_spent = div.find(attrs={"data-test": "total-spent"}).text.replace('\n', '').strip()
                    else:
                        project_spent = 'No spent'
                    project_location = div.find(attrs={"data-test": "location"}).text.replace('\n', '').strip()
                    if 'Hourly' in div.find(attrs={"data-test": "JobInfoFeatures"}).text:
                        project_price = div.find(attrs={"data-test": "job-type-label"}).text.strip()
                    else:
                        project_price = div.find(attrs={"data-test": "is-fixed-price"}).find_all('strong')[1].text.replace('\n', '').strip()
                    project_details = div.find(attrs={"data-test": "JobInfoFeatures"}).text
                    project_description = div.find(attrs={"data-test": "UpCLineClamp JobDescription"}).text.strip()
                    if len(project_description) > 3000:
                        project_description = project_description[:3000]
                    if div.find(attrs={"data-test": "TokenClamp JobAttrs"}):
                        project_skills = ', '.join(span.text for span in div.find(attrs={"data-test": "TokenClamp JobAttrs"}).find_all(attrs={"data-test": "token"}))
                    else:
                        project_skills = "No skills"
                    project = [project_title, project_spent + " " + project_location, project_price, project_description, project_skills]                    
                    if project not in total_proects: 
                        mark = '==================================================='
                        message = project_posted + ' from ' + posted_time + '\n' + project_title + '\n' + project_url + "\n\n" + 'Total Spent: ' + project_spent + '\n' + 'Location: ' + project_location + "\n" + 'Price: ' + project_price + "\n\n" + 'Description: ' + '\n' + project_description + "\n\n" + 'Skills' + '\n' + project_skills + '\n'
                        asyncio.run(send_mail(message))
                        print(project)
                        print('\n')
                    total_proects.append(project) 
                print(index)
                time.sleep(5)
            except TimeoutException as e:    
                print(f"Error: {e}")        
                driver.quit()
                time.sleep(5)
                driver = init_driver()
                login_url = 'https://www.upwork.com/ab/account-security/login'
                username = UPWORK_USERNAME
                password = UPWORK_PASSWORD

                try:
                    driver.get(login_url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_username')))
                    username_field = driver.find_element(By.ID, 'login_username')
                    submit_button = driver.find_element(By.ID, 'login_password_continue')

                    username_field.send_keys(username)
                    submit_button.click()
                    time.sleep(5)
                    
                    password_field = driver.find_element(By.ID, 'login_password')
                    submit_button_login = driver.find_element(By.ID, 'login_control_continue')
                    password_field.send_keys(password)
                    submit_button_login.click()
                    
                    WebDriverWait(driver, 10).until(EC.url_changes(login_url))                    
                    time.sleep(10)
                except TimeoutException as e:
                    print(f"Login timeout: {e}. Retrying...")
                    driver.quit()        
                except Exception as e:
                    print(f"Login error: {e}")
                    driver.quit()
            except Exception as e:  
                print(f"Error: {e}")         
                driver.quit()
                time.sleep(5)
                driver = init_driver()
                login_url = 'https://www.upwork.com/ab/account-security/login'
                username = UPWORK_USERNAME
                password = UPWORK_PASSWORD

                try:
                    driver.get(login_url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_username')))
                    username_field = driver.find_element(By.ID, 'login_username')
                    submit_button = driver.find_element(By.ID, 'login_password_continue')

                    username_field.send_keys(username)
                    submit_button.click()
                    time.sleep(5)
                    
                    password_field = driver.find_element(By.ID, 'login_password')
                    submit_button_login = driver.find_element(By.ID, 'login_control_continue')
                    password_field.send_keys(password)
                    submit_button_login.click()
                    
                    WebDriverWait(driver, 10).until(EC.url_changes(login_url))                    
                    time.sleep(10)
                except TimeoutException as e:
                    print(f"Login timeout: {e}. Retrying...")
                    driver.quit()        
                except Exception as e:
                    print(f"Login error: {e}")
                    driver.quit()
        driver.quit()

if __name__ == "__main__":
    main()