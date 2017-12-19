'''
#serial part
import serial

# open serial port
ser = serial.Serial("/dev/ttyAMA0", 115200)

def receive():
    while True:
        # acquire characters from receiver
        count = ser.inWaiting()
        if count != 0:
            # read all characters and show them back 
            recv = ser.read(count)
            ser.write(recv)
        # clear buff
        ser.flushInput()
        # necessary delay time
        time.sleep(0.1)
'''
import pymysql
import threading
import random
import serial
import time
from LoRaPackage import *
from lib2to3.fixer_util import String

#serial port
ser = serial.Serial("COM3", 115200)
'''ser = serial.Serial("/dev/ttyAMA0", 115200)'''
#converge buff
converge=""
#packages buff
packages=[]
# self physical address
selfAD="01";

#connect to database
con= pymysql.connect(
    host='localhost',
    port = 3306,
    user='CQUTLoRa',
    passwd='cqutlora',
    db ='CQUTLoRa',
    )
cur = con.cursor()

con2= pymysql.connect(
    host='localhost',
    port = 3306,
    user='CQUTLoRa',
    passwd='cqutlora',
    db ='CQUTLoRa',
    )
cur2 = con2.cursor()
#forbidden table list for LoRa to access
forbiddenDB=['LUser','LGateway','LRUser','LRNode','LANode','LCNode']

'''
A thread which is used to constantly extract package from a bunch of string that received from LoRa
'''
def distributor():
    global converge
    global packages
    while True:
        startp=converge.find("<PACKAGE>")
        endp=converge.find("</PACKAGE>",startp)
        #refine
        s=converge.find("<PACKAGE>",startp+9,endp)
        while s>0:
            startp=s
            s=converge.find("<PACKAGE>",startp+9,endp)
        if startp>-1 and endp>0 and startp<endp:
            package=converge[startp:endp+10]
            packages.append(package)
            converge=converge[endp+10:]
            print("Package Receive:\n"+package)
        time.sleep(0.4)

'''
A thread which is used to constantly combine and store the string received from LoRa
'''
def receiver():
    global converge
    global ser
    while True:
        # acquire characters from receiver
        count = ser.inWaiting()
        if count != 0:
            # read all characters and show them back 
            recv = ser.read(count)
            try:
                part=recv.decode('utf-8')
            except:
                continue
            #print(":"+part)
            # add this part of string converge buff
            converge+=part
        # clear buff
        #ser.flushInput()
        # necessary delay time
        time.sleep(0.1)

'''
A thread which is used to accept a new LoRa to this system and send command for LoRa Node
'''
def checker():
    global con2
    global cur2
    global selfAD
    while True:
        #check LANode table
        sqlselect="select * from LANode"
        cur2.execute(sqlselect)
        row=cur2.fetchone()
        con2.commit()
        if not row==None:
            print("Find one")
            
            package=LoRaPackage()
            if package.unwrap(row[0]):
                distributePP(package)
            
            #delete
            seldelete="delete from LANode where RPackage='"+row[0]+"'"
            cur2.execute(seldelete)
            con2.commit()
            print("Delete from LANode Success")
            
        #check LCNode table
        sqlselectC="select * from LCNode"
        cur2.execute(sqlselectC)
        rowC=cur2.fetchone()
        con2.commit()
        if not rowC==None:
            print("Find one Command")
            
            package=LoRaPackage()
            package.set_src(selfAD)
            package.set_des(rowC[0])
            package.set_pp("0")
            
            if rowC[1]=="STANDBY":
                package.setSTANDBY()
            elif rowC[1]=="AWAKE":
                package.setAWAKE()
            elif rowC[1]=="RESET":
                package.setRESET()
            
            sendPackage(package)
            
            #delete
            seldelete="delete from LCNode where LoRaId='"+rowC[0]+"'"
            cur2.execute(seldelete)
            con2.commit()
            print("Delete from LCNode Success")
            
        time.sleep(1)
'''
A thread which is used to handle each type of packages received from LoRa
'''
def handler():
    global packages
    global selfAD
    while True:
        if len(packages)>0:
            #pop out first to handle            
            package=LoRaPackage()
            if not package.unwrap(packages.pop(0)):
                print("Broken package")
                continue
            #check DES
            if package.get_des()==selfAD:
                #ready to handle
                command_type=package.get_command_type()
                if command_type==LoRaPackage.COMMAND_INSERT:
                    handle_insert(package)
                else:
                    #check PP
                    if checkPP(package.get_src(),package.get_pp()):
                        if command_type==LoRaPackage.COMMAND_FETCH:
                            handle_fetch(package)
                        elif command_type==LoRaPackage.COMMAND_TDATA:
                            handle_tdata(package)
                        elif command_type==LoRaPackage.COMMAND_ACKNOWLEDGE:
                            handle_acknowledge(package)
                        elif command_type==LoRaPackage.COMMAND_RTABLE:
                            handle_rtable(package)
        else:
            time.sleep(0.1)

'''
A function which serves to handle INSERT packages
'''
def handle_insert(package:LoRaPackage):
    global con
    global cur
    params=package.getINSERT()
    if len(params)<1:
        return False
    
    # trying to access PP table
    if params[0]=='LGateway' and len(params)==1:
        try:
            sqlgateway="select LoRaPP from LGateway where LoRaId='"+package.get_src()+"'"
            cur.execute(sqlgateway)
            row=cur.fetchone()
            con.commit()
            if row==None:
                #new PP
                #insert a request to database
                sqlr="insert into LRNode values('"+package.get_src()+"','"+package.wrap('str')+"')"
                cur.execute(sqlr)
                con.commit()
                print("Request has been sent.")
            else:
                acknowledge(package, row[0])
                print("LoRa "+package.get_src()+"'s PP have been retrieved.")
            return True
        except:
            con.rollback()
            #error send acknowledge package
            acknowledge(package,"ERROR")
            print("Failed to retrieve or distribute new PP!")
            return False
    elif len(params)>1:
        #check PP
        if checkPP(package.get_src(),package.get_pp()):
            #check forbidden table list
            if checkforbiddenDB(params[0]):
                #for test purpose
                try:
                    sql="insert into "+params[0]+" values('"+params[1]+"'"
                    for p in params[2:]:
                        sql+=",'"+p+"'"
                    sql+=")"
                    cur.execute(sql)
                    con.commit()
                    
                    #success send acknowledge package
                    acknowledge(package,"SUCCESS")
                    print("One row has been insert into table "+params[0])
                    return True
                except:
                    con.rollback()
                    
                    #for test purpose
                    if params[0]=="LNode":
                        #update
                        try:
                            sqlupdate="update LNode set LoRaPD='"+params[2]+"' where LoRaId='"+params[1]+"'"
                            cur.execute(sqlupdate)
                            con.commit()
                            print("One row has been update in table "+params[0])
                            return True
                        except:
                            con.rollback()
                            print("Failed to update in table "+params[0]+"!")
                            return False
                    else:
                        #error send acknowledge package
                        acknowledge(package,"ERROR")
                        print("Failed to insert into table "+params[0]+"!")
                        return False
            else:
                print("Access forbidden")
                acknowledge(package,"ERROR")
                return True
    else:
        return False
    return True

'''
A function which serves to handle FETCH packages
'''
def handle_fetch(package:LoRaPackage):
    global con
    global cur
    #PP has already been checked
    params=package.getFETCH()
    if len(params)<1:
        return False
    #check forbidden table list
    if checkforbiddenDB(params[0]):
        try:
            #get table field
            fields=[]
            sqld="describe "+params[0]
            cur.execute(sqld)
            rowsd=cur.fetchall()
            for r in rowsd:
                fields.append(r[0])
            
            #prepare sql
            sql="select * from "+params[0]
            
            index=-1
            pflag=False
            for p in params[1:]:
                index+=1
                if p=='*':
                    continue
                if sql.find('where')<0:
                    sql+=" where"
                if not pflag:
                    sql+=" "+fields[index]+"='"+p+"'"
                    pflag=True
                else:
                    sql+=" and "+fields[index]+"='"+p+"'"
            print(sql)
            cur.execute(sql)
            rows=cur.fetchall()
            
            ack=""
            for r in rows:
                ack+="<TR>"
                for l in range(0,len(r)):
                    ack+="<TD>"+r[l]+"</TD>"
                ack+="</TR>"
            
            #success send acknowledge package
            acknowledge(package, ack)
            con.commit()
            
            print("Fetch from table "+params[0])
            return True
        except:
            con.rollback()
            #error send acknowledge package
            acknowledge(package,"ERROR")
            print("Failed to fetch from table "+params[0]+"!")
            return False
    else:
        print("Access forbidden")
        acknowledge(package,"ERROR")
        return True
    
'''
A function check lnode
'''
def lnode():
    pd=[]
    while True:
        sqlnode="select * from LNode order by LoRaId"
        cur.execute(sqlnode)
        con.commit()
        rowsd=cur.fetchall()
        for r in rowsd:
            if(rowsd.index(r)>len(pd)):
                pd.append(r[1])
                continue
            if(r[1]==pd[rowsd.index(r)]):
                sqlnode2="update LNode set LoRaPD='0' where LoRaId='"+r[0]+"'"
                cur.execute(sqlnode2)
                con.commit()        
        time.sleep(3000)
    
'''
A function which serves to handle TDATA packages
'''
def handle_tdata(package:LoRaPackage):
    a=a
    
'''
A function which serves to handle ACKNOWLEDGE packages
'''
def handle_acknowledge(package:LoRaPackage):
    a=a
    
'''
A function which serves to handle RTABLE packages
'''
def handle_rtable(package:LoRaPackage):
    a=a
   
'''
distribute a PP to a LoRa Node
'''
def distributePP(package:LoRaPackage):
    global con
    global cur
    #new PP
    newPP=generatePP(10)
    try:
        sql="insert into LGateway values('"+package.get_src()+"','"+newPP+"')"
        cur.execute(sql)
        con.commit()
    except:
        print("Insert Failed")
    acknowledge(package, newPP)
    print("LoRa "+package.get_src()+"'s PP have been distributed.")
'''
-----------------------------------------------------tool kit---------------------------------------------------------------------
'''
def acknowledge(package:LoRaPackage,message:String): 
    #success send acknowledge package
    acknowledge=LoRaPackage()
    acknowledge.setACKNOWLEDGE(package,message)
    ser.write(acknowledge.wrap())
    # clear buff
    ser.flushInput()
        
def checkPP(SRC:String,PP:String):
    #check PP
    cur.execute("select * from LGateway where LoRaId='"+SRC+"' and LoRaPP='"+PP+"'")
    row=cur.fetchone()
    if row==None:
        #PP check failed
        print("Invalid PP")
        return False
    con.commit()
    return True

def generatePP(digit:int):
    sample=['1','2','3','4','5','6','7','8','9','0',
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
            ]
    PP=""
    while digit>0:
        PP+=sample[int(random.random()*len(sample))]
        digit-=1
    return PP

def checkforbiddenDB(tname:String):
    for t in forbiddenDB:
        if tname==t:
            return False
    return True
    
def sendPackage(package:LoRaPackage):
    ser.write(package.wrap())
    # clear buff
    ser.flushInput()
'''
main function
'''
def main():
    while cur==None:
        time.sleep(2)
        print("Cannot connect to Database")
    
    '''
    set up distributor
    '''
    di=threading.Thread(target=distributor)
    di.start()
    #di.join()
    
    '''
    set up receiver
    '''
    re=threading.Thread(target=receiver)
    re.start()
    #re.join()
    
    '''
    set up handler
    '''
    ha=threading.Thread(target=handler)
    ha.start()
    #ha.join()
    
    '''
    set up checker
    '''
    ch=threading.Thread(target=checker)
    ch.start()
    #ac.join()
    
    
    '''
    set up lnode checker(delete)
    '''
    ln=threading.Thread(target=lnode)
    ln.start()
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
            cur.close()
            con.close()
            cur2.close()
            con2.close()