import datetime
from subprocess import Popen, PIPE

def run_this_scpt(scpt, args=[]):
    p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(scpt)
    if int(stdout)==1:
        print ("Updated ", args[1])
##    print(stderr, stdout)
    return stdout

f=open("/Library/Application Support/Serviio/log/serviio.log")
##/Users/apl/bin/test.log")
data=f.readlines()
f.close()
dic={}

for line in data:
    if line.find('stopped') != -1 and line.find('archive.org') == -1:
        d=line[0:19]
        if d[10]=='T':
            dd=datetime.datetime.strptime(d,'%Y-%m-%dT%H:%M:%S')
        else:
            dd=datetime.datetime.strptime(d,'%Y-%m-%d %H:%M:%S')
        op = line.find('(')
        cp = line.rfind('])')
        tt = line[op+1:cp]
        br = tt.find('[', len(tt)//2 - 6)
        title = tt[0:br-1]
        trno = tt[br+1:br+3]
        if (not trno.isdigit()):
            trno = tt[br+3:br+5]
            
        if (trno.isdigit()):
            dic[tuple([trno, title])] = datetime.datetime.strftime(dd, '%m-%d-%Y %I:%M:%S %p')
        else:
            print(line)
print(dic)

for key, val in dic.items():
    run_this_scpt('''on run {x, y, z} 
        tell Application "Music"
           set command2 to {"date -j -f '%m-%d-%Y %r' ", quoted form of z, " '+%s'"}
           do shell script (command2 as text)
           set newDate to result
           set updated to 0
           set results to (every file track of playlist "Library" whose name is y and track number is x)
           repeat with t in results
              get played date of t
              set prevDate to date string of result
              set command to {"date -j -f '%A, %B %d, %Y' ", quoted form of the prevDate, " '+%s'"}
              do shell script (command as text)
              set oldDate to result
              if newDate - oldDate > 86400
                 set played date of t to date z
                 get played count of t
                 set myCount to result
                 set played count of t to myCount + 1
                 set updated to 1
              end if
           end repeat
        end tell
    updated
    end run''', [key[0], key[1], val])
