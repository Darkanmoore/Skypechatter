import sys
import thread
from Skype4Py import Skype, chat
import time

users = sys.argv[1]
client = Skype()
client.Attach()

# Save the chat history with the insert user in a ghost file

myfile = open(".history.txt", 'w')
chats = client.Chats
for c in chats:
  for m in c.Messages:
   if m.FromHandle == users:
     myfile.write(m.Body)
     myfile.write('\n')
myfile.close()
myfile = open(".history.txt", 'r')
tmp = myfile.readline()


# Function for reading the history file and printing the new message

def lettura(tmp):
   myfile = open(".history.txt", 'r')
   xm = myfile.readline()
   if xm != tmp:
     print '\n\033[1;41m%s\033[1;m'%sys.argv[1],' # ',xm, '\n'
   return xm
   

# Function for reload the file to update the history

def carica(tmp,delay):
  i = 0
  while i == 0:
   myfile = open(".history.txt", 'r+')
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
   

# Print your data and a list of the ONLINE friends 

print 'YOUR FULL NAME: %s'% client.CurrentUser.FullName
print 'YOUR CONTACTS:'
cont = []
for f in client.Friends:
  if f.OnlineStatus == 'ONLINE':
    print '\033[1;41mFull name: \033[1;m', '\033[1;34m %s \033[1;m'% f.FullName
    print '\033[1;45mSkype id: \033[1;m', '\033[1;34m%s \033[1;m'% f.Handle
    print '\033[1;42mStatus:\033[1;m','\033[1;34m %s \033[1;m'% f.OnlineStatus
    print '\033[1;43mContry: \033[1;m','\033[1;34m %s \033[1;m\n'% f.Country
    cont.append(f.FullName)
    
# Load the thread for read and update the chat history

try:
  thread.start_new_thread(carica,(tmp,2,))
except:
  print "Unable to start the thread"

# Create an instance for chatting or insert second command

message = ' '
while message != 'exit' or message != 'EXIT': 
  message = raw_input("\033[1;44mYOU: \033[1;m\n>>  ")
  
  if message == 'exit' or message == 'EXIT':
    break
  
  # Change the user write in che cmdline
  if message == '#chusr':
    users = raw_input('Skype Name >>')
    print 'User changed'
  # Change your skype status
  
  if message == '#chstate':
   try:
    client.ChangeUserStatus(raw_input('Skype Status >>'))
   except:
     print 'Status name is not valid. Consult the guide with "#--s.help"'
  # Print the list of the possible status
  
  if message == '#--s.help':
    status = ['unknown', 'offline', 'online', 'away', 'na', 'dnd', 'invisible', 'loggedout', 'skypeme']
    print 'STATUS helper'
    for k in status:
      print '\033[1;31m%s\033[1;m' % k
      
  # Print the message of the programm
  if message == '#--version':
    print 'Developed by Marco Schettini. Skype terminal chat v0.1'
    
  # Clear the chat history
  if message == '#clr':
    client.ClearChatHistory()
    
  fl = client.FileTransfers
    
  # Send a message to the user
  if message[0] != '#':
   client.SendMessage(users,message)
   print 'message sended'


print 'GoodBye'
