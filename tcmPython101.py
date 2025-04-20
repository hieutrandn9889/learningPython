import sys
import time

print(sys.version) #Output the Python version
print(sys.executable) #Output the Python executable path
print(sys.platform) #Output the platform name

for i in range(1, 5):
    sys.stdout.write(str(i) + ' ')
    sys.stdout.flush() #Flush the output buffer to ensure all data is written to the console

for i in range(1, 5):
    print(i)

for i in range(0, 51):
    time.sleep(0) #Sleep for 1 second
    sys.stdout.write("{} [{}%] \r".format(i, '#' * i))
    sys.stdout.flush() #Flush the output buffer to ensure all data is written to the console
sys.stdout.write("\n") #Print a new line after the progress bar

print(sys.argv)

if len(sys.argv) !=3:
    print("[X] To run {} enter a username and password".format(sys.argv[0]))
    sys.exit(1) #Exit the program with an error code
    username = sys.argv[1] #Get the username from the command line arguments
    password = sys.argv[2] #Get the password from the command line arguments
    print("[*] Username: {}".format(username)) #Output the username
    print("[*] Password: {}".format(password)) #Output the password