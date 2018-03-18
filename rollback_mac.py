import sys
import os

def main():    
    # Update Main System
    # for macbook air environment
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = r'appcfg.py'
    os.system(cmd + ' --oauth2 rollback ' + cur_dir)

if __name__ == "__main__":
    main()