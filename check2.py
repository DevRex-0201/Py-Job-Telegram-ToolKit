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
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import asyncio
import telegram
from telegram import Bot  # Make sure to import Bot correctly

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
    bot = telegram.Bot("")
    async with bot:
        chat_id = (await bot.get_updates())
        await bot.send_message(text=content, chat_id=6449392325)

def main():
    check_data = {}
    while True:       
        driver = init_driver()
        login_url = 'https://www.upwork.com/ab/account-security/login'
        username = 'andreasfischer0201+100@gmail.com'
        password = 'jrw20200417'

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
            file_path = 'urls.txt'
            if os.path.exists('urls.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:                                        
                    # Read each line in the file
                    for url in file:
                        try:
                            driver.get(url)
                            proposals = 0
                            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'job-details-content')))
                            page_source = driver.page_source
                            soup = BeautifulSoup(page_source, 'html.parser')
                            for script_element in soup.find_all('script'):
                                if 'clientActivity' in script_element.text:
                                    data = script_element.text
                                    json_initial_text = data.split('clientActivity:{')[1].split('},weeklyRetainerBudget')[0]
                                    proposals = str(json_initial_text.split(',')[1].split(':')[1])
                                    break
                                else:
                                    proposals = 'c'
                            print(json_initial_text)
                            activity_items = soup.find('ul', class_='client-activity-items list-unstyled').find_all('li')
                            viewed_time = 'Not viewed'  
                            hires = '0'       
                            for item in activity_items:
                                if ('Proposals:' in item.text) and ('c' in proposals or 'd' in proposals or 'g' in proposals or 'm' in proposals or 't' in proposals  or 'z' in proposals or 'o' in proposals ):
                                    proposals = str(item.find(class_='value').text.replace('\n', '').strip())
                                if 'Last viewed by client' in item.text:
                                    viewed_time = str(item.find(class_='value').text.replace('\n', '').strip())
                                if 'Hires:' in item.text:
                                    hires = str(item.find(class_='value').text.replace('\n', '').strip())
                                if 'Interviewing' in item.text:
                                    interviews = str(item.find(class_='value').text.replace('\n', '').strip())
                                if 'Invites sent:' in item.text:
                                    invites_sent = str(item.find(class_='value').text.replace('\n', '').strip())
                                if 'Unanswered invites:' in item.text:
                                    unanswered_invites = str(item.find(class_='value').text.replace('\n', '').strip())
                            message = soup.title.text + '\n' + url + '\n' + 'Proposals: ' + proposals  + '\n' + 'Last viewed by client: ' + viewed_time  + '\n' + 'Hires: ' + hires  + '\n' + 'Interviewing: ' + interviews  + '\n' + 'Invites sent: ' + invites_sent  + '\n' + 'Unanswered invites: ' + unanswered_invites 

                            if url in check_data and 'seconds' in viewed_time:
                                mark = '*********************************************************'
                                message = mark + '\n' + soup.title.text + '\n' + url + '\n' + 'Proposals: ' + proposals  + '\n' + 'Last viewed by client: ' + viewed_time  + '\n' + 'Hires: ' + hires  + '\n' + 'Interviewing: ' + interviews  + '\n' + 'Invites sent: ' + invites_sent  + '\n' + 'Unanswered invites: ' + unanswered_invites 
                                asyncio.run(send_mail(message))
                            check_data[url] = viewed_time
                            print('\n')
                            print(message)
                            print('\n')
                            
                        except TimeoutException as e:    
                            print(f"Error: {e}")        
                            driver.quit()
                            time.sleep(5)
                            driver = init_driver()
                            login_url = 'https://www.upwork.com/ab/account-security/login'
                            username = 'andreasfischer0201+200@gmail.com'
                            password = 'jrw20200417'

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
                            username = 'andreasfischer0201+200@gmail.com'
                            password = 'jrw20200417'

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
            print(index)
        driver.quit()

if __name__ == "__main__":
    main()