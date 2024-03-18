# Telegram Job Scraper and Notifier

## Overview

The Job Scraper and Notifier is a sophisticated Python application designed to automate the process of scraping job listings from a specific job site, specifically tailored for projects related to web scraping. Utilizing a combination of web scraping techniques and browser automation with Selenium, this tool filters jobs based on specified criteria (e.g., hourly rate, payment verification, and job type) and notifies the user about new listings via Telegram messages. The script is engineered to operate continuously, ensuring users receive timely updates on potential job opportunities.

## Video Preview

[![Video Preview](https://github.com/DevRex-0201/Project-Images/blob/main/video%20preview/Py-Upwork-Telegram-ToolKit.png)](https://brand-car.s3.eu-north-1.amazonaws.com/Four+Seasons/Py-Job-Telegram-ToolKit.mp4)

## Features

- **Automated Login**: Securely logs into job site using provided credentials to access job listings.
- **Custom Job Filtering**: Retrieves jobs based on predefined search criteria, such as hourly rate, payment verification, and specific keywords.
- **Real-time Notifications**: Sends alerts via Telegram for new job listings, including details like job title, description, budget, client's total spent, and required skills.
- **Error Handling**: Implements robust error handling and retry mechanisms to manage login timeouts and other exceptions, ensuring continuous operation.
- **Headless Browser Support**: Operates in headless mode for efficient background execution without requiring a graphical user interface.

## Prerequisites

Before running the Job Scraper and Notifier, ensure you have the following installed:

- Python 3.6 or newer
- Selenium WebDriver
- ChromeDriver (compatible with your Chrome version)
- BeautifulSoup4 for parsing HTML
- gspread and oauth2client for Google Sheets integration (optional)
- Python `requests` and `dotenv` libraries for handling HTTP requests and environment variables
- Telegram Bot API token and chat ID for sending notifications

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/job-scraper-notifier.git
   cd job-scraper-notifier
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the root directory and specify your credentials and Telegram Bot API token:
   ```
   USERNAME=your_username
   PASSWORD=your_password
   TELEGRAM_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   ```

## Usage

To start the job scraper and notifier, run the `main.py` script:

```bash
python main.py
```

The script will automatically log in to the job site, perform job searches based on the configured criteria, and send Telegram notifications for new job listings.

## Customization

You can customize the job search criteria and notification messages by modifying the relevant sections in the `main.py` script. Adjust the search URL, parsing logic, or message format as needed to fit your specific requirements.

## Troubleshooting

- **Login Issues**: Ensure your username and password are correct and that your account does not have any unresolved security prompts.
- **Telegram Notifications Not Sent**: Verify your Bot API token and chat ID are correct. Ensure your bot has permission to send messages to the specified chat.
- **WebDriver Errors**: Make sure ChromeDriver is installed and its path is correctly configured. Update ChromeDriver if it's not compatible with your Chrome browser version.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests with enhancements, bug fixes, or documentation improvements.

## License

This project is open-source and available under the [MIT License](LICENSE).
