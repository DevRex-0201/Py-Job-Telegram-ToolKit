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


# Function to ask for duration using Tkinter
def ask_duration():
    ROOT = tk.Tk()
    ROOT.withdraw()
    USER_INP = simpledialog.askstring(title="Set Duration", prompt="Enter Duration in Seconds:")
    return int(USER_INP)

def safe_append_to_worksheet(worksheet, data, max_retries=5, delay=5):
    for _ in range(max_retries):
        try:
            worksheet.append_row(data)
            return
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}. Retrying...")
            time.sleep(delay)
    print("Failed to append data after retries.")

def login_to_website(driver, username, password, login_url):
    try:
        driver.get(login_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_username')))
        username_field = driver.find_element(By.ID, 'login_username')
        password_field = driver.find_element(By.ID, 'login_password')
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        username_field.send_keys(username)
        password_field.send_keys(password)
        submit_button.click()

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
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            break  # Exit loop if successful
        except Exception as e:
            if driver:  # Check if driver was initialized
                driver.quit()
            time.sleep(5)  # Wait before retrying
            if attempt == 1:  # Last attempt
                print(f"Failed to initialize driver after 2 attempts: {e}")
                return None  # Return None or raise an exception

    return driver
async def send_mail():
    bot_token = "YOUR_BOT_TOKEN_HERE"  # Replace YOUR_BOT_TOKEN_HERE with your actual bot token
    chat_id = "YOUR_CHAT_ID"  # Replace YOUR_CHAT_ID with your actual chat ID
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text="Re-login failed. Retrying...")

async def send_mail():
    print('send_mail')
    bot = telegram.Bot("6877424292:AAHUnzus7LNyGlzmX--KB8t1vh3w3yxP6CU")
    async with bot:
        print(await bot.get_me())
        chat_id = (await bot.get_updates())
        print(chat_id)
        await bot.send_message(text="Re-login failed. Retrying...", chat_id=1123788700)

def main():
    total_data = [["Data Time", "Huay 264", "Huay VIP 264", "LTO 264", "LTO VIP 264", "ชัดเจน 264", "ชัดเจน VIP 264"]]
    duration = ask_duration()
    dotenv.load_dotenv()
    google_credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
    if not google_credentials_path:
        raise ValueError("Google Sheets credentials path is not set.")

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_credentials_path, scope)
    client = gspread.authorize(creds)

    sheet_url = "https://docs.google.com/spreadsheets/d/1r_96ut4UIoDEkSYQqyaSCNKppQwR7VyXZPn-lWOKcvI/edit?usp=sharing"
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.get_worksheet(0) or spreadsheet.add_worksheet(title="Sheet1", rows="100", cols="20")

    header_names = ["Data Time", "Huay 264", "Huay VIP 264", "LTO 264", "LTO VIP 264", "ชัดเจน 264", "ชัดเจน VIP 264"]
    if not worksheet.row_values(1):
        worksheet.insert_row(header_names, index=1)

    while True:       
        driver = init_driver()
        login_url = 'https://dnabet.vip/login'
        username = 'Gargoyle007'
        password = 'Gg123456'

        if not login_to_website(driver, username, password, login_url):
            print("Login failure.")
            driver.quit()
            return
        for _ in range(20):

            try:
                driver.get("https://dnabet.vip/lotto/result")
                time.sleep(5)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'result-container')))
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                div_elements = soup.find_all('div', class_='sc-9e723fdc-0 krDVwH undefined card border-gradient !lg:p-[20px] !p-[10px]')
                order = [8, 9, 16, 17, 12, 13]
                data = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                data_com = []   
                for item in order:
                    if item < len(div_elements):
                        div_element = div_elements[item]
                        span_element = div_element.find('span', class_='ant-typography text-[0.85rem] lg:text-[1rem]')
                        divs_font_numeral = div_element.find_all('strong')
                        if span_element and len(divs_font_numeral) >= 2:
                            data.extend([span_element.get_text().split(" ")[-1], divs_font_numeral[3].get_text(), divs_font_numeral[4].get_text()])
                            data_com.extend([span_element.get_text().split(" ")[-1], divs_font_numeral[3].get_text(), divs_font_numeral[4].get_text()])
                        else:
                            driver.refresh()
                if len(data) <= 1:
                    driver.refresh() 
                print(data)
                if len(data) >= 19 and data_com != total_data[-1]:
                    total_data.append(data_com)
                    safe_append_to_worksheet(worksheet, data)

                    if data_com[0] == "1":
                        print("Day")
                        all_rows = worksheet.get_all_values()
                        number_of_rows = len(all_rows)
                        if number_of_rows > 10:
                            time.sleep(3300)                

                    if data_com[0] == "2" and data_com[1] == "-":
                        all_rows = worksheet.get_all_values()
                        number_of_rows = len(all_rows)
                        worksheet.delete_rows(2,number_of_rows)

                    if data_com[0] == data_com[3] == data_com[6] == data_com[9] == data_com[12] == data_com[15]:
                        print("Value1 of lotto are same")
                        time.sleep(150)

                time.sleep(duration)
            except TimeoutException as e:            
                driver.quit()
                time.sleep(5)
                driver = init_driver()
                login_url = 'https://dnabet.vip/login'
                username = 'Gargoyle007'
                password = 'Gg123456'
                try:
                    driver.get(login_url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_username')))
                    username_field = driver.find_element(By.ID, 'login_username')
                    password_field = driver.find_element(By.ID, 'login_password')
                    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

                    username_field.send_keys(username)
                    password_field.send_keys(password)
                    submit_button.click()

                    WebDriverWait(driver, 10).until(EC.url_changes(login_url))
                    time.sleep(10)
                except TimeoutException as e:
                    print(f"Login timeout: {e}. Retrying...")
                    driver.quit()        
                except Exception as e:
                    print(f"Login error: {e}")
                    driver.quit()
                print(f"Error: {e}. Timeout error")
            except Exception as e:            
                driver.quit()
                time.sleep(5)
                driver = init_driver()
                login_url = 'https://dnabet.vip/login'
                username = 'Gargoyle007'
                password = 'Gg123456'
                try:
                    driver.get(login_url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_username')))
                    username_field = driver.find_element(By.ID, 'login_username')
                    password_field = driver.find_element(By.ID, 'login_password')
                    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

                    username_field.send_keys(username)
                    password_field.send_keys(password)
                    submit_button.click()

                    WebDriverWait(driver, 10).until(EC.url_changes(login_url))
                    time.sleep(10)
                except TimeoutException as e:
                    print(f"Login timeout: {e}. Retrying...")
                    driver.quit()        
                except Exception as e:
                    print(f"Login error: {e}")
                    driver.quit()
                print(f"Error: {e}. Attempting re-login.")
        driver.quit()

if __name__ == "__main__":
    main()