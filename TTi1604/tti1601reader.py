#! python
#
# this scrips establish serial connection between
#PC serial port and TTi1604 bench multimeter.
#When connection established then report display.
#
# Author: kovpeti - petitech.tk
#
# Version:
#  0.1      20.02.2018      Initial version
if __name__ == "__main__":
    import sys
    import serial
    import time
    if len(sys.argv)!=2:
        sys.exit('Usage: tti1601reader COMPORT_NAME')
    else:
        Port=sys.argv[1]                        #get port name
        Ser=serial.Serial()
        Ser.port=Port
        Ser.dsrdtr=0
        Ser.baudrate=9600
        Ser.timeout=1
        Ser.rts=0                                  #activate instruments
        Ser.dtr=1                                  #   RS232 optocoupler
        Ser.open()
        time.sleep(1)
        #try to connect
        loopcounter=0
        ok=0
        print('Try to connect to the instrument ', end='')
        while (loopcounter<15):
            print('.', end='')
            sendbyte=117                        #'u'
            Ser.write(sendbyte)                     #activate remote mode
            time.sleep(1)
            Ser.reset_input_buffer()
            waiting=0
            while (waiting==0):
                waiting=Ser.in_waiting
            RB=Ser.read(10)                     #check answer
            #print(RB)
            if (RB[0]==117) or (RB[0]==13):
                ok=1
                loopcounter = 16
            loopcounter+=1
            Ser.reset_input_buffer()
            time.sleep(1)
        print()
        if ok == 0:
            Ser.close()
            sys.exit('No answer from the instrument');
        #Connection established
        Ser.reset_input_buffer()            #flush buffer
        print('Connection established')
        while (1):
            data=Ser.read(10)               #read data packet
            #print(data)
            display=''
            if data[0]==13:                     #valid?
                #Get measured value
                for i in range(4, 9):
                    if data[i]==252:
                        display+='0'
                    elif data[i]==253:
                        display+='0.'
                    elif data[i]==96:
                        display+='1'
                    elif data[i]==97:
                        display+='1.'
                    elif data[i]==218:
                        display+='2'
                    elif data[i]==219:
                        display+='2.'
                    elif data[i]==242:
                        display+='3'
                    elif data[i]==243:
                        display+='3.'
                    elif data[i]==102:
                        display+='4'
                    elif data[i]==103:
                        display+='4.'
                    elif data[i]==182:
                        display+='5'
                    elif data[i]==183:
                        display+='5.'
                    elif data[i]==190:
                        display+='6'
                    elif data[i]==191:
                        display+='6.'
                    elif data[i]==224:
                        display+='7'
                    elif data[i]==225:
                        display+='7.'
                    elif data[i]==254:
                        display+='8'
                    elif data[i]==255:
                        display+='8.'
                    elif data[i]==230:
                        display+='9'
                    elif data[i]==231:
                        display+='9.'
                    else: display+=' '
                #get sign
                if (data[3] & 0b00000010) >0:
                    display='-'+display
                print(display)
                #get metric
                
                #print(data)
