import sys
import os

def main():
    if len(sys.argv) == 1:
        print "Please enter the app id"
        return 
    
    appId = sys.argv[1]
    print "appId", appId
    
    # Update Main System
    # for macbook air environment
    #cmd = r'python "C:\Program Files (x86)\Google\google_appengine\appcfg.py"'
    #cmd = r'python "C:\Program Files (x86)\Google\google_appengine\remote_api_shell.py" -s %s.appspot.com' % appId
    cmd = r'remote_api_shell.py -s %s.appspot.com' % appId
    # for normal environment
    #cmd = r'"C:\Program Files (x86)\Google\google_appengine\appcfg.py"'
    #cmd = r'"appcfg.py"'
    #os.system(cmd + " update . " + " -A %s -e zouber129@gmail.com --passin"%appId)
    os.system(cmd)


if __name__ == "__main__":
    main()
