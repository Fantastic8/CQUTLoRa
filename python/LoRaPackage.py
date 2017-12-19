'''
Created on 2017.8.20

@author: Mark
'''
#class defination
from lib2to3.fixer_util import String
class LoRaPackage:
    '''
    This is a Package class for receiving packages from LoRa and translate them into a class
    '''
    
    # --member variables below
    
    # constant command values
    COMMAND_FETCH='FETCH'
    COMMAND_INSERT='INSERT'
    COMMAND_TDATA='TDATA'
    COMMAND_STANDBY='STANDBY'
    COMMAND_AWAKE='AWAKE'
    COMMAND_RESET='RESET'
    COMMAND_ACKNOWLEDGE='ACKNOWLEDGE'
    COMMAND_RTABLE='RTABLE'
    
    # package initial private parameters
    __NxtAddr=-1
    __NxtChanl=-1
    __SRC=''
    __DES=''
    __PP=''
    __COMMAND_TYPE=''
    __COMMAND_ID=-1
    __COMMAND_CONT=''
    
    # Constructor
    def __init__(self,src='',des='',pp=''):
        self.__NxtAddr=-1
        self.__NxtChanl=-1
        self.__SRC=src
        self.__DES=des
        self.__PP=pp
        self.__COMMAND_TYPE=''
        self.__COMMAND_ID=-1
        self.__COMMAND_CONT=''
        
    # Print all variables
    def printv(self):
        print('NxtAddr='+str(self.__NxtAddr))
        print('NxtAddr='+str(self.__NxtChanl))
        print('SRC='+self.__SRC)
        print('DES='+self.__DES)
        print('PP='+self.__PP)
        print('COMMAND_TYPE='+self.__COMMAND_TYPE)
        print('COMMAND_ID='+str(self.__COMMAND_ID))
        print('COMMAND_CONT='+self.__COMMAND_CONT)

    # getters
    def get_nxt_addr(self):
        return self.__NxtAddr


    def get_nxt_chanl(self):
        return self.__NxtChanl
        
    def get_nxt(self):
        return (self.__NxtAddr,self.__NxtChanl)
     
    def get_src(self):
        return self.__SRC


    def get_des(self):
        return self.__DES


    def get_pp(self):
        return self.__PP


    def get_command_type(self):
        return self.__COMMAND_TYPE


    def get_command_id(self):
        return self.__COMMAND_ID


    def get_command_cont(self):
        return self.__COMMAND_CONT

    # setters
    def set_nxt_addr(self, value):
        self.__NxtAddr = value

    def set_nxt_chanl(self, value):
        self.__NxtChanl = value
       
    def set_nxt(self,addr,chanl):
        self.__NxtAddr=addr
        self.__NxtChanl=chanl
         
    def set_src(self, value):
        self.__SRC = value


    def set_des(self, value):
        self.__DES = value


    def set_pp(self, value):
        self.__PP = value


    def set_command_id(self, value):
        self.__COMMAND_ID = value
    
    '''
    ------------------------------------------------------------------------------------------------------------------------------------------
                                                            properties
    ------------------------------------------------------------------------------------------------------------------------------------------
    '''
    NxtAddr = property(get_nxt_addr, set_nxt_addr, None, None)
    NxtChanl = property(get_nxt_chanl, set_nxt_chanl, None, None)
    SRC = property(get_src, set_src, None, None)
    DES = property(get_des, set_des, None, None)
    PP = property(get_pp, set_pp, None, None)
    COMMAND_TYPE = property(get_command_type, None, None, None)
    COMMAND_ID = property(get_command_id, set_command_id, None, None)
    COMMAND_CONT = property(get_command_cont, None, None, None)
    '''
    ------------------------------------------------------------------------------------------------------------------------------------------
                                                        wrapping function
    ------------------------------------------------------------------------------------------------------------------------------------------
    '''
    
    '''
    set FETCH command
    Input:
        tname: the name of table which user wants to fetch from
        *params: parameters as conditions matching fetch command
    Output:
        void
    '''
    def setFETCH(self,tname,*params):
        '''
        set __COMMAND_TYPE to fetch command
        set __COMMAND_CONT to match right form of parameters
        '''
        self.__COMMAND_TYPE=self.COMMAND_FETCH
        self.__COMMAND_CONT='<TNAME>'+tname+'</TNAME>'
        for param in params:
            self.__COMMAND_CONT+='<PARAM>'+param+'</PARAM>'
        
        
    '''    
    set INSERT command
    Input:
        tname: the name of table which user wants to insert into
        *params: parameters as conditions matching insert command
    Output: void
    '''
    def setINSERT(self,tname,*params):
        '''
        set __COMMAND_TYPE to insert command
        set __COMMAND_CONT to match right form of parameters
        '''
        self.__COMMAND_TYPE=self.COMMAND_INSERT
        self.__COMMAND_CONT='<TNAME>'+tname+'</TNAME>'
        for param in params:
            self.__COMMAND_CONT+='<PARAM>'+param+'</PARAM>'
       
    ''' 
    set TDATA command
    Input:
        massage: the message which user wants to transmit 
    Output:
        void 
    '''
    def setTDATA(self,message):
        '''
        set __COMMAND_TYPE to tdata command
        set __COMMAND_CONT to message
        '''
        self.__COMMAND_TYPE=self.COMMAND_TDATA
        self.__COMMAND_CONT=message
    
    '''
    set STANDBY command
    Input:
        void
    Output:
        void
    '''
    def setSTANDBY(self):
        '''
        set __COMMAND_TYPE to standby command
        clear __COMMAND_CONT and __COMMAND_ID
        '''
        self.__COMMAND_TYPE=self.COMMAND_STANDBY
        self.__COMMAND_CONT=''
        self.__COMMAND_ID=-1
    
    '''
    set AWAKE command
    Input:
        void
    Output:
        void 
    '''
    def setAWAKE(self):
        '''
        set __COMMAND_TYPE to awake command
        clear __COMMAND_CONT and __COMMAND_ID
        '''
        self.__COMMAND_TYPE=self.COMMAND_AWAKE
        self.__COMMAND_CONT=''
        self.__COMMAND_ID=-1
    
    '''
    set RESET command
    Input:
        void
    Output:
        void 
    '''
    def setRESET(self):
        '''
        set __COMMAND_TYPE to reset command
        clear __COMMAND_CONT and __COMMAND_ID
        '''
        self.__COMMAND_TYPE=self.COMMAND_RESET
        self.__COMMAND_CONT=''
        self.__COMMAND_ID=-1
    
    '''
    set ACKNOWLEDGE command
    Input:
        package: the package user wants to reply
        message: the message that user wants to reply
    Output:
        void
    '''
    
    def setACKNOWLEDGE(self,package,message):
        '''
        set __COMMAND_ID to command_id
        set __COMMAND_TYPE to acknowledge command
        set __COMMAND_CONT to message
        set up __SRC
        set up __DES
        set up __PP
        '''
        self.__COMMAND_ID=package.get_command_id()
        self.__COMMAND_TYPE=self.COMMAND_ACKNOWLEDGE
        self.__COMMAND_CONT=message
        
        self.__SRC=package.get_des()
        self.__DES=package.get_src()
        self.__PP=package.get_pp()
        
    '''
    set RTABLE command
    Input: 
        **table: the table which contains whole rout table data
    Output:
        void 
    '''
    def setRTABLE(self,**table):
        '''
        set __COMMAND_TYPE to rtable command
        ***
        '''
        self.__COMMAND_TYPE=self.COMMAND_RTABLE
        
    '''
    wrap
    Input: 
        encoding:
            'utf-8': if user wants to wrap this package into bytes which encoded by 'utf-8'
            'str': if user wants to wrap this package into string
    Output:
        None: if package is unwrappable-error package
        String: the string user is able to transmit
    '''
    def wrap(self,encoding='utf-8'):
        # wrap all attributes in this package
        package=''
        # NxtAddr = 16bits ; NxtChanl = 8bits
        if self.__NxtAddr>0 and self.__NxtChanl>0:
            package+=chr(int('0b'+str(bin(self.__NxtAddr))[2:].rjust(16,'0')[0:8],2))+chr(int('0b'+str(bin(self.__NxtAddr))[2:].rjust(16,'0')[8:16],2))+chr(self.__NxtChanl)
            
        package+='<PACKAGE>'
        
        package+='<SRC>'+self.__SRC+'</SRC>'
        package+='<DES>'+self.__DES+'</DES>'
        package+='<PP>'+self.__PP+'</PP>'
        
        # COMMAND part
        if self.__COMMAND_TYPE==self.COMMAND_STANDBY or self.__COMMAND_TYPE==self.COMMAND_AWAKE or self.__COMMAND_TYPE==self.COMMAND_RESET:
            package+='<'+self.__COMMAND_TYPE+'>'
        elif self.__COMMAND_TYPE==self.COMMAND_FETCH or self.__COMMAND_TYPE==self.COMMAND_INSERT or self.__COMMAND_TYPE==self.COMMAND_TDATA or self.__COMMAND_TYPE==self.COMMAND_ACKNOWLEDGE or self.__COMMAND_TYPE==self.COMMAND_RTABLE:
            if self.__COMMAND_ID<0:
                # error package
                return None
            package+='<'+self.__COMMAND_TYPE+'>'
            package+='<ID>'+str(self.__COMMAND_ID)+'</ID>'
            package+='<CONT>'+self.__COMMAND_CONT+'</CONT>'
            package+='</'+self.__COMMAND_TYPE+'>'
        else:
            # error package
            return None
        package+=''
        package+='</PACKAGE>'
        
        if encoding!='str':
            return package.encode(encoding)
        
        return package
    
    '''
    ------------------------------------------------------------------------------------------------------------------------------------------
                                                        unwrapping procedures
    ------------------------------------------------------------------------------------------------------------------------------------------
    '''
    '''
    unwrap kit function
    '''
    def __unwrapTag(self,package:String,tag:String):
        # check
        if package.find('<'+tag+'>')!=0 or not package.endswith('</'+tag+'>'):
            return None
        return package[len('<'+tag+'>'):len(package)-len('</'+tag+'>')]
    
    def __getTagContent(self,package:String,tag:String):
        # find
        start=package.find('<'+tag+'>')
        end=package.find('</'+tag+'>')
        if start<0 or end<0 or start>end or package.find('<'+tag+'>',start+len('<'+tag+'>'))>0 or package.find('</'+tag+'>',end+len('</'+tag+'>'))>0:
            return None
        return package[start+len('<'+tag+'>'):end]
    
    def __getCommandType(self,package:String):
        command=package[1:package.find('>')]
        if package.find('<'+command+'>')!=0 or not package.endswith('</'+command+'>'):
            return None
        return command
            
    
    '''
    unwrap
    Input:
        package: the String that user wants to translate into LoRaPackage
    Output:
        True: if success
        False: if failed to unwrap
    '''
    def unwrap(self,package:String):
        # checking <PACKAGE>
        nxtaddr=-1
        nxtchanl=-1
        if package.find('<PACKAGE>')==3:
            nxtaddr=int(str(bin(ord(package[0])))[2:]+str(bin(ord(package[1])))[2:],2)
            nxtchanl=ord(package[2])
            package=package[3:]
            
        pack=self.__unwrapTag(package,'PACKAGE')
        if pack==None:
            return False
        package=pack
        # <PACKAGE> checking success
        # batch checking attributes
        src=self.__getTagContent(package, 'SRC')
        if src==None or src=='':
            return False
        
        des=self.__getTagContent(package, 'DES')
        if des==None or des=='':
            return False
        
        pp=self.__getTagContent(package, 'PP')
        if pp==None or pp=='':
            return False
        
        command=package[package.find('</PP>')+5:]
        command_type=self.__getCommandType(command)
        if not (command_type==self.COMMAND_ACKNOWLEDGE or command_type==self.COMMAND_AWAKE or command_type==self.COMMAND_FETCH or command_type==self.COMMAND_INSERT or command_type==self.COMMAND_RESET or command_type==self.COMMAND_RTABLE or command_type==self.COMMAND_STANDBY or command_type==self.COMMAND_TDATA):
            return False
        
        command_id=self.__getTagContent(command,'ID')
        if command_id==None or command_id=='':
            return False
        
        command_cont=self.__getTagContent(command,'CONT')
        if command_cont==None or command_cont=='':
            return False
        
        # check success
        self.__NxtAddr=nxtaddr
        self.__NxtChanl=nxtchanl
        self.__SRC=src
        self.__DES=des
        self.__PP=pp
        self.__COMMAND_TYPE=command_type
        self.__COMMAND_ID=int(command_id)
        self.__COMMAND_CONT=command_cont
        #print(command)
        #print(self.__getCommandType(command))
        #print(package)
        #print(src)
        #print(des)
        #print(pp)
        return True
    
    '''
    get parameters' kit
    '''
    def __getParameters(self,command_cont:String):
        params=[]
        while len(command_cont)>0:
            try:
                tag=command_cont[command_cont.find('<')+1:command_cont.find('>')]
            except Exception:
                break
            params.append(command_cont[command_cont.find('>')+1:command_cont.find('</'+tag+'>')])
            command_cont=command_cont[command_cont.find('</'+tag+'>')+3+len(tag):len(command_cont)]
        return params
   
    '''
    get FETCH command parameters
    Input:
        void
    Output:
        *params: params[0] is name of table followed by all parameters
    '''
    def getFETCH(self):
        if self.__COMMAND_TYPE!=self.COMMAND_FETCH:
            return None
        return self.__getParameters(self.__COMMAND_CONT)
    
    '''
    get INSERT command parameters
    Input:
        void
    Output:
        *params: params[0] is name of table followed by all parameters
    '''
    def getINSERT(self):
        if self.__COMMAND_TYPE!=self.COMMAND_INSERT:
            return None
        return self.__getParameters(self.__COMMAND_CONT)
    
    '''
    get TDATA message
    Input:
        void
    Output:
        message: the message which user wants to transmit
    '''
    def getTDATA(self):
        if self.__COMMAND_TYPE!=self.COMMAND_TDATA:
            return None
        return self.__COMMAND_CONT
    
    '''
    get ACKNOWLEDGE message
    Input:
        void
    Output:
        message: the message which user wants to acknowledge
    '''
    def getACKNOWLEDGE(self):
        if self.__COMMAND_TYPE!=self.COMMAND_ACKNOWLEDGE:
            return None
        return self.__COMMAND_CONT
    
    '''
    is this package a STANDBY command package
    Input:
        void
    Output:
        True: if this package is a STANDBY command package
        False: if this package isn't a STANDBY command package
    '''
    def isSTANDBY(self):
        return self.__COMMAND_TYPE==self.COMMAND_STANDBY
        
    '''
    is this package a AWAKE command package
    Input:
        void
    Output:
        True: if this package is a AWAKE command package
        False: if this package isn't a AWAKE command package
    '''
    def isAWAKE(self):
        return self.__COMMAND_TYPE==self.COMMAND_AWAKE
    
    '''
    is this package a RESET command package
    Input:
        void
    Output:
        True: if this package is a RESET command package
        False: if this package isn't a RESET command package
    '''
    def isRESET(self):
        return self.__COMMAND_TYPE==self.COMMAND_RESET    
