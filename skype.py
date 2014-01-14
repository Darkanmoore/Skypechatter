import sys
import thread
from Skype4Py import Skype, chat
import time
users = sys.argv[1]
client = Skype()
client.Attach()


myfile = open("history.txt", 'w')
chats = client.Chats
for c in chats:
  for m in c.Messages:
   if m.FromHandle == users:
     myfile.write(m.Body)
     myfile.write('\n')
myfile.close()
myfile = open("history.txt", 'r')
tmp = myfile.readline()

def lettura(tmp):
   myfile = open("history.txt", 'r')
   xm = myfile.readline()
   if xm != tmp:
     print '\n\033[1;41m%s\033[1;m'%sys.argv[1],' # ',xm, '\n'
   return xm
   

def carica(tmp,delay):
  i = 0
  while i == 0:
   myfile = open("history.txt", 'r+')
   chats = client.Chats
   for c in chats:
     for m in c.Messages:
      if m.FromHandle == users:
        myfile.write(m.Body)
        myfile.write('\n')
   myfile.close()
   xm = lettura(tmp)
   tmp = xm
   time.sleep(delay)
   

 
print 'YOUR FULL NAME: %s'% client.CurrentUser.FullName
print 'YOUR CONTACTS:'
cont = []
for f in client.Friends:
  if f.OnlineStatus == 'ONLINE':
    print '\033[1;41mFull name: \033[1;m', '\033[1;34m %s \033[1;m'% f.FullName
    print '\033[1;42mStatus:\033[1;m','\033[1;34m %s \033[1;m'% f.OnlineStatus
    print '\033[1;43mContry: \033[1;m','\033[1;34m %s \033[1;m\n'% f.Country
    cont.append(f.FullName)
    

try:
  thread.start_new_thread(carica,(tmp,2,))
except:
  print "Unable to start the thread"

message = ' '
while message != 'exit' or message != 'EXIT': 
  message = raw_input("\033[1;44mYOU: \033[1;m\n>>  ")
  if message == 'exit' or message == 'EXIT':
    break
  if message == '#chusr':
    s = raw_input('Skype Name:')
    for t in cont:
      if t == s:
        users = s
        break
    if s != users:
      print 'Contact is not ONLINE or is not present in your contacts list'
  if message[0] != '#':
   client.SendMessage(users,message)
   print 'message sended'


print 'Arrivederci'
