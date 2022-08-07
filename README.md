# What is this ?

DoliBrute is a login brute force tool with captcha bypass for Dolibarr login page.

- Article : https://baadmaro.github.io/posts/Bypass-captcha-using-OCR-on-Dolibarr-login-page/

# Disclaimer

All information and software available on this page are for educational and authorized purposes only.
  
# Install and dependencies

- Python version : Tested on 3.11, 3.6
- tesseract : https://tesseract-ocr.github.io/tessdoc/Home.html#binaries

Installation : 

```
git clone https://github.com/BaadMaro/DoliBrute
cd DoliBrute
pip install -r requirements.txt
``` 

Change the variable `pytesseract.pytesseract.tesseract_cmd` for tesseract binary location and OS.

```python
# Linux
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Windows
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
```



# Usage

```bash
python3 DoliBrute.py -u http://IP/ -U username -P passwords.txt

```

```
 
 _____        _ _ ____             _       
|  __ \      | (_)  _ \           | |      
| |  | | ___ | |_| |_) |_ __ _   _| |_ ___ 
| |  | |/ _ \| | |  _ <| '__| | | | __/ _ \
| |__| | (_) | | | |_) | |  | |_| | ||  __/
|_____/ \___/|_|_|____/|_|   \__,_|\__\___|
  
  DoliBrute is a login brute force tool with captcha bypass for Dolibarr login page.                                        
  V0.1
  Coded by BaadMaro
    
Usage: 
    python3 DoliBrute.py -u http://127.0.0.1/ -U admin -P default-passwords.txt


Options:
  -h, --help     show this help message and exit
  -U USERNAME    specify username
  -P PASSWORDS   specify passwords list
  -u BASE_URL    specify base url with "/" at the end
  --proxy=PROXY  specify proxy with IP:Port
```

## Example

![image](https://user-images.githubusercontent.com/72421091/183272388-cbcc96a1-2340-439d-839e-58b84d613f87.png)


With proxy

![image](https://user-images.githubusercontent.com/72421091/183272309-00587d81-05ef-47e9-8b99-e3611ebb8673.png)


# Tested versions

- [*] 15.0.2

# Lab setup with docker

- https://hub.docker.com/r/tuxgasy/dolibarr

Create docker-compose.yml file as following:

```yaml
version: "3"

services:
    mariadb:
        image: mariadb:latest
        environment:
            MYSQL_ROOT_PASSWORD: root
            MYSQL_DATABASE: dolibarr

    web:
        image: tuxgasy/dolibarr
        environment:
            DOLI_DB_HOST: mariadb
            DOLI_DB_USER: root
            DOLI_DB_PASSWORD: root
            DOLI_DB_NAME: dolibarr
            DOLI_URL_ROOT: 'http://0.0.0.0'
            PHP_INI_DATE_TIMEZONE: 'Europe/Paris'
        ports:
            - "80:80"
        links:
            - mariadb
```

Then run all services docker-compose up -d. Now, go to http://0.0.0.0 to access to the new Dolibarr installation.

# To do

- More clean code.
- HTTPS support ( i need to test it).
- Erros Handling.
- ✅ Succes login test case with 302 redirection.
- OS detection for tesseract_cmd variable.
- Improve OCR detection.
- Use a wordlist for usernames.
- Options for no captcha use.
- Handle errors messages for other languages (?).
- verbose mode.
- Threading.
- Custom User Agent.
- ✅ Proxy support.

# Kudos

Thanks to some exploits authors in exploit-db, I was inspired by their code : 
- Dolibarr ERP-CRM 12.0.3 - Remote Code Execution (Authenticated) https://www.exploit-db.com/exploits/49269 
- Dolibarr 12.0.3 - SQLi to RCE : https://www.exploit-db.com/exploits/49240
