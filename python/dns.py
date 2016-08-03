import sys,socket,struct

def GetName(Data,Start,Len=0):
    res=""
    i=Start
    while i<len(Data):
        if (Data[i]==0xc0 or Data[i]==0):
            if (Len==0):
                return res[:-1]
            else:
                res+=GetName(Data,Data[i+1])
                return res
        for j in range(0,Data[i]):
            res+=chr(Data[i+j+1])
        res+="."
        i+=Data[i]+1

def DNS(DNSserver,Domain):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    try:
        s.connect((DNSserver,53))
        Dom=Domain.split(".")
        Dom_byte=b""
        for i in range(0,len(Dom)):
            Dom_byte+=bytes([len(Dom[i])])+bytes(Dom[i],encoding="utf8")
        packet = struct.pack("12B",0,0x01,0x01,0,0,0x01,0,0,0,0,0,0)+Dom_byte+struct.pack("5B",0,0,0x1,0,0x01)
        s.send(packet)
        Data_Orign=s.recv(10240)
        Format=str(len(Data_Orign))+"B"
        Data = struct.unpack(Format, Data_Orign)
        RRs=Data[6]*10+Data[7]
        start=0
        for i in range(12, len(Data)):
            if (Data[i] == 0xc0 ):
                start = i
                break
        for i in range(0, RRs):
            while (start < len(Data)):
                Str = ""
                Str += GetName(Data, Data[start + 1])
                start += 3
                if Data[start] == 5:
                    Str += "   CNAME   "
                elif Data[start] == 1:
                    Str += "     A     "
                else:
                    Str += "   Unknow  "
                start += 9
                if ((Data[start - 2] * 256 + Data[start - 1]) == 4):
                    Str += str(Data[start]) + "." + str(Data[start + 1]) + "." + str(Data[start + 2]) + "." + str(Data[start + 3])
                    print(Str)
                    start += 4
                    continue
                else:
                    Str += GetName(Data, start, Data[start - 2] * 256 + Data[start - 1])
                    start += Data[start - 2] * 256 + Data[start - 1]
                    print(Str)

    except:
        (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
        print("Connect server failed: ", ErrorValue)
        return

DNS("223.5.5.5","www.qq.com")