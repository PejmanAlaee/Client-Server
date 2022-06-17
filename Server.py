#server.py
import socket
import threading
import datetime
conditon = 0
PmCondition = 0
mainnuser = ""
pmConLAST = 0
GpCondition = 0
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5002

client_sockets = set()
client_socketss = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(10)


print(f"Listening as {SERVER_HOST}:{SERVER_PORT}")
countter = 0


def findLen(str):
	counter = 0
	for i in str:
		counter += 1
	return counter


def client(cs):

  global conditon
  print(f"[Active connections {threading.active_count() - 1}]")

  while True:
    msg = cs.recv(1024).decode()
    if (msg.split(' ')[0] == 'End' and msg.split(' ')[1] == '-Option' and msg.split(' ')[2] == '<id:'):
          with open('file.txt', 'r') as fr:
            lines = fr.readlines()
            # delete client
            with open('file.txt', 'w') as fw:
                for line in lines:
                    a = line.strip('\n').split(" ")
                    if a[0] != msg.split(" ")[3]:
                        fw.write(line)


          for client_socket in client_sockets:
                client_socket.send( f"<{msg.split(' ')[3]}> left the chat room".encode())
          break   


    if (msg.split(' ')[0] == 'Make' and msg.split(' ')[1] == '-Option' and
            msg.split(' ')[3] == '-Option'):
        count = 0
        usser = msg.split(' ')[2].split(":")[1]
        mainUsser = usser.replace('>', '')
        passs = msg.split(' ')[4].split(":")[1]
        mainPass = passs.replace('>', '')
        partTwo = msg.split(' ')[5].split("<")[1]
        mainId = partTwo.split(":")[1]
        maiinId = mainId.split(">")[0]
        if findLen(mainUsser) < 6:
            count = 1
        elif findLen(mainPass) < 6:
            count = 2
        else:
            # check that we dont have this user , pass , id in list
            with open('file.txt') as file_in:
                for line in file_in:
                    w = line.split(" ")
                    try:
                        if w[0] == mainUsser:
                            count = 3
                        elif w[1] == mainPass:
                            count = 4
                        elif w[2] == maiinId:
                            count = 5
                    except:
                     pass

        if count == 0:
         with open("file.txt", 'a') as file_in:
          file_in.write(f'{mainUsser + " " + mainPass + " " + str(maiinId)  + "" + str(conditon)}\n')
         cs.send(f"User Accepted -Option <{maiinId}#>".encode())
        elif count == 1:
         cs.send("User Not Accepted -Option <pelease more than 6 charectors for you Name:>>".encode())
        elif count == 2:
         cs.send("User Not Accepted -Option <pelease more than 6 charectors for you password:>>".encode())
        elif count == 3:
         cs.send("User Not Accepted -Option <we have this usserName , please Try again:>>".encode())
        elif count == 4:
         cs.send("User Not Accepted -Option <we have this password , please Try again>>".encode())
        elif  count == 5:
         cs.send("User Not Accepted -Option <we have this Id , please Try again>>".encode())


    elif (msg.split(' ')[0] == 'Connect' and msg.split(' ')[1] == '-Option'
        and msg.split(' ')[3] == '-Option'):
        global PmCondition
        global pmConLAST
        global GpCondition
        global fail
        global mainnuser
        countLogin = 0
        mainnuser = " "
        usser = msg.split(' ')[2].split(":")[1]
        mainUsserr = usser.replace('>', '')
        passs = msg.split(' ')[4].split(":")[1]
        mainPasss = passs.replace('>', '')
        # check that if we have this user and pass , connected
        with open('file.txt') as file_in:
            for line in file_in:
                w = line.split(" ")
                if w[0] == mainUsserr and w[1] == mainPasss:
                    countLogin = 1
                    iddd = w[2].strip()
                    conditon = 2
                    mainnuser = mainUsserr
                    maaainUsser = mainUsserr
                    PmCondition = 1
            if countLogin != 1:
                countLogin = 0
                iddd = -1
        if int(countLogin)==1:
         client_socketss[mainUsserr]=cs
         cs.send(f"Connected -Option <id:{iddd}> Option<SID:#>".encode())
        elif int(countLogin) == 0:
            cs.send("ERROR -Option <reason:we dont have this person in messenger Software>".encode())


    elif (msg.split(' ')[0] == 'Group' and msg.split(' ')[1] == '-Option' and
         msg.split(' ')[3] == '-Option'):
        userClient=msg.split(" ")[2].split(":")[1][:-1]
        # Send information
        for client_socket in client_sockets:
            if client_socket != cs:
             client_socket.send(f"<{userClient}> join the chat room.".encode())
            if client_socket == cs:
                client_socket.send(f"Hi <{userClient}>, welcome to the chat room".encode())
                try:
                    with open('Gp.txt', 'r') as file:
                        data = file.readlines()
                        client_socket.send("Last PM".encode())
                        for linee in data:
                            n = linee.split("”")
                            if n[0] != " ":
                                client_socket.send(
                                    f"GM -Option <from:{n[0]}> -Option <to:GAPNAME> -Option <message_len:#> -Option <message_body:{n[1]}>".encode())
                except:
                    pass


    elif msg.split(' ')[0] == 'Users' and msg.split(' ')[1] == '-Option':
        answer = ""
        with open('file.txt') as file_in:
                for line in file_in:
                    r = line.split(" ")
                    answer = answer + f"<user_{r[0]}>|"
        cs.send(answer.encode())


    elif (msg.split(' ')[0] == 'GM' and msg.split(' ')[1] == '-Option'
            and msg.split(' ')[3] == '-Option'and msg.split(' ')[5] == '-Option'):
        # using it to get current time
        userrr = ""
        current_time = datetime.datetime.now()
        hour = current_time.hour
        min = current_time.minute
        second = current_time.second
        msgBody = msg.split(':')[3].replace('>', '')
        len = msg.split(' ')[4].split(":")[1]
        leen = len.replace('>', '')
        for k, v in client_socketss.items():
            if v == cs:
                userrr=k
                break
        for client_socket in client_sockets:
                 client_socket.send("NEW PM".encode())
                 client_socket.send(f"( {hour}:{min}:{second} ) GM -Option <from:{userrr}> -Option <to:GAPNAME> -Option <message_len:{leen}> -Option <message_body:{msgBody}>".encode())
        with open("Gp.txt", 'a') as file_in:
            file_in.write(f'{userrr + " " + str(msgBody) + " " + "GP"}\n')


    elif (msg.split(' ')[0] == 'PM' and msg.split(' ')[1] == '-Option' and msg.split(' ')[3] == '-Option'
            and msg.split(' ')[5] == '-Option'):
        # using it to get current time
        current_timee = datetime.datetime.now()
        hourr = current_timee.hour
        minn = current_timee.minute
        secondd = current_timee.second
        msgBody = msg.split(':')[3].replace('>', '')
        len = msg.split(' ')[2].split(":")[1]
        msgLen = len.replace('>', '')
        for k, v in client_socketss.items():
            if v == cs:
                userSend = k
                break
        userCllientPm = msg.split(" ")[4].split(":")[1].replace('>', '')
        i = 0
        # open file for find reciver peername
        with open('file.txt') as file_in:
                for linee in file_in:
                    r = linee.split(" ")
                    if r[0] == userCllientPm:
                        i =1
                        #find it
                    try:
                     wn = client_socketss[userCllientPm]
                    except:pass
        #search in client that active for send Pm to client that we want
        for client_sockett in client_sockets:
            if i == 0:
                cs.send("no thread from this userName".encode())
                break
            elif client_sockett == wn:
             with open('chat.txt', 'r') as file:
                data = file.readlines()
                client_sockett.send(f"Last Pm from {userSend}".encode())
                # we search in each line in file to find reciever and sender name
                for linee in data:
                     n = linee.split(" ")
                     if n[0]==userSend and n[1] == userCllientPm:
                        # set line that first client want to send
                        senderPm = n
                        client_sockett.send(f"PM -Option <from:{senderPm[0]}> -Option <to:ME> -Option <message_len:#> -Option <message_body:{senderPm[2]}>".encode())
                        # set line that second client want to send
                     elif n[1] == userSend and n[0] == userCllientPm:
                            reciverPm = n
                            client_sockett.send(f"PM -Option <from:ME> -Option <to:{reciverPm[1]}> -Option <message_len:#> -Option <message_body:{reciverPm[2]}>".encode())

                with open("chat.txt", 'a') as file_in:
                    file_in.write(f'{userSend + " " + userCllientPm + " " + str(msgBody) + " "+"private"}\n')
                    # after all we send New Pm here
                    client_sockett.send(f"NEW PM FROM : {userSend}".encode())
                    client_sockett.send(f"( {hourr}:{minn}:{secondd} )PM -Option <from:{userSend}> -Option <to:{userCllientPm}> -Option <message_len:{msgLen}> -Option <message_body:{msgBody}>".encode())
                    break

while True:
    client_socket, client_address = s.accept()
    print(f"{client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    tread = threading.Thread(target=client, args=(client_socket,))
    tread.daemon = True
    # start the thread
    tread.start()
