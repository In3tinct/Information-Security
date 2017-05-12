import xss as xss
import cmd_exe as cmd 
import sql as sql
import fileinclusion as fileinclusion
import sys

if __name__ == "__main__":

    print "enter the IP of the node which you want to exploit"
    dest = raw_input()
    IP = "http://" + dest
    

    print "choose the following attacks from menu"
    print "Menu :"
    print "\t 1. Command execution"
    print "\t 2. Cross site scripting"
    print "\t 3. SQL injection"
    print "\t 4. File Inclusion"
    print "\t 5. To exit"
    
    choice = int(raw_input())

    if choice <1 or choice >5:
        print "wrong choice entered, try again"
    
    elif choice == 1:
            cmd.command(IP)
    elif choice == 2:
            xss.xssAuto(IP)
    elif choice == 3:
            sql.sqlinjection(IP)
    elif choice == 4:
            fileinclusion.fileinclusion(IP)
    elif choice == 5:
            pass
    
    print "exiting the application"



