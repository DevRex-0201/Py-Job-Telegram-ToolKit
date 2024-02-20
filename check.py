import os
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import asyncio
import telegram
from telegram import Bot  # Make sure to import Bot correctly
from bs4 import BeautifulSoup
from io import BytesIO
import gzip
import brotli
import json
import re

headers_initial = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Referer': 'https://www.upwork.com/nx/find-work/most-recent',
    'Cache-Control': 'max-age=0',
    'Cookie': '__cflb=02DiuEXPXZVk436fJfSVuuwDqLqkhavJbqbp97u3PHh2j; visitor_id=89.221.225.12.1708119145312000; device_view=full; _gcl_au=1.1.324997147.1708119126; spt=ca765098-d367-449a-a84c-60489a04056b; _cq_duid=1.1708119125.cSvWhHmvB7CtMcYJ; _tt_enable_cookie=1; _ttp=UrWOChugIi2l3J6zH8YrueEHP5C; _gcl_au=1.1.324997147.1708119126; __pdst=6b595fdd971e4487917b4d1a74b67b50; G_ENABLED_IDPS=google; OptanonAlertBoxClosed=2024-02-16T21:32:41.301Z; country_code=IL; cookie_prefix=; cookie_domain=.upwork.com; _cq_suid=1.1708323201.39w645GET4OvGOCx; _gid=GA1.2.1372887026.1708323201; _uetsid=fbf1db70ceed11eeb6a88f923d557751; _uetvid=fbf22340ceed11eea2c4bd48120efee5; IR_gbd=upwork.com; 5deb36f3sb=oauth2v2_6bb1e95e0049f19b4b0879ced911cb75; dtCookie=v_4_srv_4_sn_9B30B7930D7A3B7F9D5690E6288567CD_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1_rcs-3Acss_0; FindWorkHome:hasInterviewsOrOffers=0; umq=1101; _cfuvid=Al.WBssHbWAnZ4HyJ.NNB_9jbFFrbWZ2NRUo5iAIpbY-1708328343516-0.0-604800000; _upw_ses.5831=*; a8940548sb=oauth2v2_a45410d4115cb9d1148b3d424146c256; recognized=3af548b0; company_last_accessed=d1036373428; 4ca92f36sb=oauth2v2_ffe73c5b093782238e000880b97ea467; AWSALBTG=sIR9Pw4L4h8pHYe3wjN+Um9Yz8M8A3ZqIrK7cC8qEOwBhL5eJUomVH2ZYjRUV6JHEZdfOjqJSckUZ6kObtjcFzx5ooAXq0G/5ALoWdnofCtdnJjratjCpSxJ/jUplZfu8m/FFiF/JTr3gwK7LLVAmEBPwri3FOiEli2H176r0w8l; AWSALBTGCORS=sIR9Pw4L4h8pHYe3wjN+Um9Yz8M8A3ZqIrK7cC8qEOwBhL5eJUomVH2ZYjRUV6JHEZdfOjqJSckUZ6kObtjcFzx5ooAXq0G/5ALoWdnofCtdnJjratjCpSxJ/jUplZfu8m/FFiF/JTr3gwK7LLVAmEBPwri3FOiEli2H176r0w8l; asct_vt=oauth2v2_627533144375ac2d189aa0aee8ad6fc4; user_uid=1674122182226448384; current_organization_uid=1674122182226448385; oauth2_global_js_token=oauth2v2_702486cc76c211c809e03e7ccabf9383; master_access_token=5bec1e1b.oauth2v2_e1a7999cc2ce4c76c23ab3cd8170bfd7; console_user=3af548b0; SZ=da5c5ce3243f219467b7ea1d994d153a744bbc25bcb7ad8dc5e71212a6fe603f; 58ef0f3asb=oauth2v2_427944c944ec6c6d554ff7c166e55c13; user_oauth2_slave_access_token=5bec1e1b.oauth2v2_e1a7999cc2ce4c76c23ab3cd8170bfd7:1674122182226448384.oauth2v2_723f9234fcb4dae568bb83010f616b99; ftr_blst_1h=1708351517860; __cf_bm=pyMDxmFzDbDPKa0tPjsfzo_Nvq3slKcuE84DUNSiIM4-1708352812-1.0-AecwViq+/jseo/95Jou+QjZfMOktYVgOqvhzUAIvO9lXSmgmTV5dHxa4uQfBXJmD4bAJr4YBIFz/2KUiI787oi0=; XSRF-TOKEN=7f7e34fc2ea4938a4de3d673def85df6; FindWorkHome:freelancerMenuSpacing=188px; vjd_gql_token=oauth2v2_4ec75d31d3354579ae34aaba5af58caf; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Feb+19+2024+09%3A30%3A14+GMT-0500+(Eastern+Standard+Time)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=276dabae-cf13-4024-89eb-6c9a3dc6032c&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=IL%3BTA; _upw_id.5831=eeda803d-c70f-470a-93e0-a5a5c7507497.1708119125.5.1708353014.1708337331.6e1cdd5a-f730-48dc-9926-45d63a919b87.71033c0a-5985-4e3c-9de7-c05b792a1714.6d46a017-28cb-4352-8d6e-d959c7914c26.1708342563982.334; _ga=GA1.2.336013119.1708119126; AWSALB=FyFLMRoQ8PUoNY4JDauk8AKKcas7hvw1RL3GkqlHoIcjWqcQHM21rm/IO7lAB4IhwYV7LEzBGkPtO2DwDI2aiUJmy3H2qwJ6Lk0Qt2UL1n9kFUMEDcSYDkSSiS/o; AWSALBCORS=FyFLMRoQ8PUoNY4JDauk8AKKcas7hvw1RL3GkqlHoIcjWqcQHM21rm/IO7lAB4IhwYV7LEzBGkPtO2DwDI2aiUJmy3H2qwJ6Lk0Qt2UL1n9kFUMEDcSYDkSSiS/o; forterToken=1926dd312ced4a2598f51157c8d10c48_1708353013744__UDF43-m4_14ck; _rdt_uuid=1708119128235.53146387-b0fa-4254-a192-257d3deac46e; _ga_KSM221PNDX=GS1.1.1708350830.6.1.1708353016.0.0.0; IR_13634=1708353017066%7C0%7C1708350836579%7C%7C; enabled_ff=!CLOBJPGV2RJP,!RMTAir3Hired,JPAir3,CI9570Air2Dot5,!RMTAir3Talent,!RMTAir3Home,!CI12577UniversalSearch,!air2Dot76Qt,air2Dot76,!CI17409DarkModeUI,!CI10857Air3Dot0,!i18nGA,!SSINavUser,OTBnrOn,i18nOn,!MP16400Air3Migration,SSINavUserBpa,CI11132Air2Dot75,!CI10270Air2Dot5QTAllocations,TONB2256Air3Migration',
    # Add other headers as needed
}

def get_initial_cookies(url, headers):
    with requests.Session() as session:
        response = session.get(url, headers=headers)
        return response.cookies

async def send_mail(content):
    bot = telegram.Bot("")
    async with bot:
        chat_id = (await bot.get_updates())
        await bot.send_message(text=content, chat_id=6449392325)
        
def main():
    check_data = {}
    while True:
        file_path = 'urls.txt'
        if os.path.exists('urls.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:                                        
                # Read each line in the file
                for url in file:
                    with requests.Session() as session:
                        # Update the session's cookies with the provided cookies
                        headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'max-age=100',
                        'Cookie': 'b2dd513dsb=oauth2v2_2bb88b342fa18ff34243d82540c485a0; 47a26286sb=oauth2v2_8983df22e67d8d62c3c95508e2a05fca; a39f48f8sb=oauth2v2_bd5e45ea902eb152e5dc0efc66d02dbf; b7d968f4sb=oauth2v2_369954d9473de203611bf939ad703cac; __cflb=02DiuEXPXZVk436fJfSVuuwDqLqkhavJbqbp97u3PHh2j; visitor_id=89.221.225.12.1708119145312000; device_view=full; _gcl_au=1.1.324997147.1708119126; spt=ca765098-d367-449a-a84c-60489a04056b; _cq_duid=1.1708119125.cSvWhHmvB7CtMcYJ; _tt_enable_cookie=1; _ttp=UrWOChugIi2l3J6zH8YrueEHP5C; _gcl_au=1.1.324997147.1708119126; __pdst=6b595fdd971e4487917b4d1a74b67b50; G_ENABLED_IDPS=google; OptanonAlertBoxClosed=2024-02-16T21:32:41.301Z; cookie_prefix=; country_code=IL; cookie_domain=.upwork.com; _cq_suid=1.1708323201.39w645GET4OvGOCx; _gid=GA1.2.1372887026.1708323201; _uetsid=fbf1db70ceed11eeb6a88f923d557751; _uetvid=fbf22340ceed11eea2c4bd48120efee5; IR_gbd=upwork.com; 5deb36f3sb=oauth2v2_6bb1e95e0049f19b4b0879ced911cb75; dtCookie=v_4_srv_4_sn_9B30B7930D7A3B7F9D5690E6288567CD_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1_rcs-3Acss_0; FindWorkHome:hasInterviewsOrOffers=0; _cfuvid=Al.WBssHbWAnZ4HyJ.NNB_9jbFFrbWZ2NRUo5iAIpbY-1708328343516-0.0-604800000; a8940548sb=oauth2v2_a45410d4115cb9d1148b3d424146c256; recognized=3af548b0; company_last_accessed=d1036373428; 4ca92f36sb=oauth2v2_ffe73c5b093782238e000880b97ea467; asct_vt=oauth2v2_627533144375ac2d189aa0aee8ad6fc4; oauth2_global_js_token=oauth2v2_702486cc76c211c809e03e7ccabf9383; master_access_token=5bec1e1b.oauth2v2_e1a7999cc2ce4c76c23ab3cd8170bfd7; user_uid=1674122182226448384; console_user=3af548b0; current_organization_uid=1674122182226448385; SZ=da5c5ce3243f219467b7ea1d994d153a744bbc25bcb7ad8dc5e71212a6fe603f; 58ef0f3asb=oauth2v2_427944c944ec6c6d554ff7c166e55c13; user_oauth2_slave_access_token=5bec1e1b.oauth2v2_e1a7999cc2ce4c76c23ab3cd8170bfd7:1674122182226448384.oauth2v2_723f9234fcb4dae568bb83010f616b99; AWSALBTG=IV8VbqS0cJlBNlPXVJMo+0DnSUKc9WOTgw3V846ctYu0JGzRC6/P2kScDp4e8xM6H8My2ti1j4n+oh+Ftg5K28eDtXzrZcFw+GUS5Mtqc+gpIhv2TFpRNJyyBTBuF5fCRLOtv4TIfLKPLrLz2+VAq8VHq/HzMRKe3Ysq4qkkFxeN; AWSALBTGCORS=IV8VbqS0cJlBNlPXVJMo+0DnSUKc9WOTgw3V846ctYu0JGzRC6/P2kScDp4e8xM6H8My2ti1j4n+oh+Ftg5K28eDtXzrZcFw+GUS5Mtqc+gpIhv2TFpRNJyyBTBuF5fCRLOtv4TIfLKPLrLz2+VAq8VHq/HzMRKe3Ysq4qkkFxeN; UniversalSearchNuxt_vt=oauth2v2_2e3096bb5faf48de9cb59bac71f67320; 6b5011c7sb=oauth2v2_5fd6d7cf57993e18e42ccebf5375fe0d; channel=other; umq=1101; _upw_ses.5831=*; ftr_blst_1h=1708378974579; vjd_gql_token=oauth2v2_449924c811fe80766e431ae71f8db552; __cf_bm=JID1VWbrrYDMRSf24irDn0idJDAn38cmy9y5KkrXyEc-1708380594-1.0-AY85kC890c87lSkx6vpG7YYmFzciikzabQXzouxBObwx2I5FW4EQSZ5gS7v2vCdwCtS9GIQ5w2auVskm+IhsVV8=; XSRF-TOKEN=f58ed251d53226af2cc9bd2d4eba04ba; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Feb+19+2024+17%3A09%3A42+GMT-0500+(Eastern+Standard+Time)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=276dabae-cf13-4024-89eb-6c9a3dc6032c&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=IL%3BTA; enabled_ff=CI11132Air2Dot75,!air2Dot76Qt,!SSINavUser,OTBnrOn,!MP16400Air3Migration,TONB2256Air3Migration,!CI17409DarkModeUI,!CI10270Air2Dot5QTAllocations,!RMTAir3Home,!RMTAir3Hired,!CI10857Air3Dot0,air2Dot76,!CI12577UniversalSearch,SSINavUserBpa,!i18nGA,i18nOn,!RMTAir3Talent,CI9570Air2Dot5,!CLOBJPGV2RJP,JPAir3; FindWorkHome:freelancerMenuSpacing=188px; _ga_KSM221PNDX=GS1.1.1708377793.11.1.1708380586.0.0.0; _ga=GA1.1.336013119.1708119126; _rdt_uuid=1708119128235.53146387-b0fa-4254-a192-257d3deac46e; IR_13634=1708380587071%7C0%7C1708377796892%7C%7C; forterToken=1926dd312ced4a2598f51157c8d10c48_1708379106861__UDF43-m4_14ck; _upw_id.5831=eeda803d-c70f-470a-93e0-a5a5c7507497.1708119125.10.1708380806.1708375847.2e9b6c29-abcf-4a59-b9b4-475c4864695f.08b33065-1785-417a-9905-d063e9a74691.2e31a169-96a3-4114-800f-a4033c6b795e.1708377790166.42; AWSALB=r0LhrbxN78ubz+jmzj3LLfauQ3E0KY/ZDDn0RtS2ogLTxuAtT+Thwfuqc6SWSO4BZ8ANd2VfNnWjAsB4vDmS8TGwp2gILojDgKYpmid76HgrfUHJ0Xmmdt1qkgdq; AWSALBCORS=r0LhrbxN78ubz+jmzj3LLfauQ3E0KY/ZDDn0RtS2ogLTxuAtT+Thwfuqc6SWSO4BZ8ANd2VfNnWjAsB4vDmS8TGwp2gILojDgKYpmid76HgrfUHJ0Xmmdt1qkgdq',
                        'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                        'Sec-Ch-Ua-Mobile': '?0',
                        'Sec-Ch-Ua-Platform': '"Windows"',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                        }
                        # Make the GET request
                        response = session.get(url, headers=headers)
                        print(response.status_code)
                        # Check if the request was successful (status code 200)
                        if response.status_code == 200:
                            # Parse the HTML content using BeautifulSoup
                            soup = BeautifulSoup(response.text, 'html.parser')
                        
                            # Example: print the title of the page
                            # title = soup.title.text
                            for script_element in soup.find_all('script'):
                                if 'clientActivity' in script_element.text:
                                    data = script_element.text
                                    json_initial_text = data.split('clientActivity:{')[1].split('},weeklyRetainerBudget')[0]
                                    proposals = str(json_initial_text.split(',')[1].split(':')[1])
                                    break
                                else:
                                    proposals = 'c'
                            activity_items = soup.find('ul', class_='client-activity-items list-unstyled').find_all('li')
                            viewed_time = 'Not viewed'  
                            hires = '0'       
                            for item in activity_items:
                                if ('Proposals:' in item.text) and 'c' in proposals or 'd' in proposals or 'g' in proposals or 'm' in proposals:
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
                                message = soup.title.text + '\n' + url + '\n' + 'Proposals: ' + proposals  + '\n' + 'Last viewed by client: ' + viewed_time  + '\n' + 'Hires: ' + hires  + '\n' + 'Interviewing: ' + interviews  + '\n' + 'Invites sent: ' + invites_sent  + '\n' + 'Unanswered invites: ' + unanswered_invites 
                                asyncio.run(send_mail(message))
                            check_data[url] = viewed_time
                            print(message)
                        else:
                            print("Failed to retrieve the page. Status Code:", response.status_code)
                        print('\n')
                time.sleep(1)
if __name__ == "__main__":
    main()