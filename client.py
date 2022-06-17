#client.py
import socket
import random
import os
from threading import Thread


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5002
s = socket.socket()
print(f" Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print(" Connected.")
# if 0 not register
#if 1 register
#if 2 log in
#if 3 join to group
conditon = 0
condiition = 0
PmCondition = 0
mainnuser = ""
pmConLAST = 0
GpCondition = 0
shart = 0
def prrrrrint():
    while True:
     message = s.recv(1024).decode()
     print(message)
     setCondition(message)


maaainUsser = ""

t = Thread(target=prrrrrint)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()
fail = 0
print("1.If you want to register type {Make} please")
print("2.If you want to connect type{Connection} please")
print("3.If you want to join to Group, type{Group} please")
print("4.If you want show Users, type{Users} please")
print("5.If you want to  GM, type{GM} please")
print("6.If you want to PM, type{PM} please")
print("7.If you want to exit, type{End} please")


# Returns length of string

def setCondition (massage):
     global condiition
     try:
      if (massage.split(' ')[1]=="Accepted"):
         condiition = 1
      if(massage.split(' ')[0]=="Connected"):
         condiition = 2
     except:
         pass


def makeperson(user , password , id) :
  a= f"Make -Option <user:{user}> -Option <pass:{password}> -Option<id:{id}>"
  s.send(a.encode("utf-8"))

def operation():
 while True:
    global PmCondition
    global pmConLAST
    global GpCondition
    global fail
    global conditon
    global mainnuser
    global condiition
    args = input()

    if (args=="Make"):
        print("your name:")
        mainUsser = input()
        print("your password:")
        mainPass = input()
        print("your Id:")
        maiinId = input()
        makeperson(mainUsser, mainPass, maiinId)

    elif (args =="Connection"):
        if condiition == 2:
            print("you should connected man")
        else:
            print("your name:")
            mainUsser = input()
            print("your password:")
            mainPass = input()
            a=f"Connect -Option <user:{mainUsser}> -Option <pass:{mainPass}>"
            s.send(a.encode("utf-8"))


    elif (args == 'Group'):
        if condiition<2 :
         print("ERROR -Option <You shoud login at first !>")
        elif condiition == 3:
         # if conditon == 3 , You have already joined the group
         print("ERROR -Option <you are already Log in!>")
        elif condiition==2:
          condiition = 3
          a = f"Group -Option <user:{mainUsser}> -Option <gname:Group_Name>"
          s.send(a.encode("utf-8"))


    elif (args == 'Users'):
         if (condiition <=2):
            print("ERROR -Option <You shoud join to group at first !")
         else:
          a = f"Users -Option <user:{mainUsser}>"
          if condiition >= 3:
           print("USERS_LIST:")
           s.send(a.encode("utf-8"))



    elif (args == 'GM'):
            if condiition<=2:
             print("ERROR -Option <You shoud join to group at first !>")
            else:
             condiition =4
             print("please Enter your Massage Len")
             MsgLen = input()
             print("please Enter your Massage Body")
             MsgBody = input()
             a = f"GM -Option <to:GAPNAME> -Option <message_len:{MsgLen}> -Option <message_body:”{MsgBody}”>"
             s.send(a.encode("utf-8"))


    elif (args == 'PM'):
        if condiition<=1:
            print("ERROR -Option <You shoud connect at first !>")
        elif condiition<=2:
            print("ERROR -Option <You shoud join to group at first !>")
        else:
         print("please Enter your Massage Len")
         MsgLen = input()
         print("please Enter the name that you want to sent massage")
         userToSend = input()
         print("please Enter your Massage Body")
         MsgBody = input()
         a = f"PM -Option <message_len:{MsgLen}> -Option <to:{userToSend}> -Option <message_body:”{MsgBody}”>"
         s.send(a.encode("utf-8"))


    elif (args == 'End'):
     if int(condiition) < 3:
        print("ERROR -Option <reason: you should join at first")
     else:
      a = f"End -Option <id: {mainUsser} OR GAPNAME>"
      s.send(a.encode("utf-8"))
      if condiition >= 3:
       break
    else:
        print("be careful,you entered incorrectly, Try again please")



operation()
