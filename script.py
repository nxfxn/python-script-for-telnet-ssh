import sys, subprocess
import telnetlib, getpass

f= open('h.txt')
hosts = [x.strip('\n') for x in f.readlines()]

user= raw_input("Username: ")
password = getpass.getpass('Password:')
en_password = getpass.getpass('Enable Password:')

command='show version | i restarted'

for i in hosts:
    try:
        tn=telnetlib.Telnet(i,23,10)
        tn.read_until("Username: ")
        tn.write(user + "\n")
        tn.read_until("Password: ")
        tn.write(password + "\n")
        tn.write("enable\n")
        tn.write(en_password + "\n")
        tn.write("conf t\nline vty 0 4\nlength 0\nend\n")
        tn.write("show version | i restarted\n")
        tn.write("exit\n")
        f2=open ('o.txt', "a+")
        output = tn.read_all() + "\n==================================================\n"
        f2.write(output)
        f2.close()
        tn.close()
        print "%s: Telnet Worked!" %(i)
    except:
        try:
            ssh = subprocess.Popen(["ssh", "%s" %i, command],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result=ssh.stdout.readlines()
            if result == []:
                error=ssh.stderr.readlines()
                print >>ssh.stderr, "SSH ERROR %s" %error
            else:
                print result
                print "%s: SSH Worked!" %(i)
        except:
            print "%s: Host unreachable!" %(i)
