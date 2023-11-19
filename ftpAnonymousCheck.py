#!/bin/python3
import ftplib
import sys


class FTPAnonymousCheck:
    def __init__(self) -> None:
        if len(sys.argv) < 3:
            print('Example Usage: ./%s target port number' % sys.argv[0])
        sys.exit()
        self.target = sys.argv[1]
        try:
            self.port = int(sys.argv[2])
        except:
            print("[-] Please use integer as port number")
            sys.exit()

    def run(self):
        try:
            self.ftp_client = ftplib.FTP()
            self.ftp_client.connect(host=self.target, port=self.port)
            print('[+] Connected successfully')
        except Exception as e:
            print('[+] Something went wrong: %s' % e)
            sys.exit()
        try:
            self.ftp_client.login(user='anonymous')
            print('[+] The target allows anonymous login: %s %d' %
                  (self.target, self.port))
            self.ftp_client.close()
        except Exception as e:
            print("Something went wrong: %s" % e)
            sys.exit()


if __name__ == '__main__':
    client = FTPAnonymousCheck()
    client.run()
