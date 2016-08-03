# -*- coding:utf-8 -*-
import requests,json,urllib.parse,datetime,hashlib,random,hmac,base64,time
VultrKey="aa"
AliKey="aa"
AliSecret="aa"

def Vultr(Parse="SUBID",Value="SSVPN"):
    headers={"API-KEY":VultrKey}
    req=requests.get("https://api.vultr.com/v1/server/list",headers=headers)
    result=json.loads(req.text)
    for i in result:
        if result[i]["label"]==Value:
            return result[i][Parse]

def Vultr_Destory(SUBID):
    headers = {"API-KEY": VultrKey}
    Data={"SUBID":SUBID}
    req=requests.post("https://api.vultr.com/v1/server/destroy",headers=headers,data=Data)
    print(req.text)

def Vultr_Create():
    headers = {"API-KEY": VultrKey}
    Data={"DCID":25,"VPSPLANID":29,"OSID":161,"SCRIPTID":20461,"enable_ipv6":"yes","enable_private_network":"yes","label":"SSVPN"}
    req = requests.post("https://api.vultr.com/v1/server/create",headers=headers,data=Data)
    print(req.text)

def Url(a):
    b=""
    for i in range(0,len(a)):
        try:
            if a[i]=='/':
                b+="%2F"
            elif a[i]=='"':
                b+="%22"
            elif a[i]=='*':
                b+="%2A"
            elif a[i]=='=':
                b+="%3D"
            elif a[i]=='+':
                b+="%20"
            elif a[i]=='&':
                b+="%26"
            elif a[i]=='%':
                b+="%25"
            else:
                b+=a[i]
        except:
            continue
    return b

def Ali_Sign(method,a):
    Key=sorted(a.items(), key=lambda d: d[0])
    Key2=urllib.parse.urlencode(Key)
    Key2=Url(Key2)
    Sign=method+"&%2F&"+Key2
    hm=hmac.new(bytearray(AliSecret+"&",encoding="utf8"),Sign.encode("utf8"),digestmod=hashlib.sha1).digest()
    b64hm=base64.b64encode(hm)
    return str(b64hm,encoding="utf8")

def Ali_Public():
    Key={
            "Format":"JSON","Version":"2015-01-09","AccessKeyId":AliKey,"SignatureMethod":"HMAC-SHA1",
            "Timestamp":datetime.datetime.strftime(datetime.datetime.utcnow(),"%Y-%m-%dT%H:%M:%SZ"),"SignatureVersion":"1.0",
            "SignatureNonce":str(random.randint(0,1000000000))+"-"+str(random.randint(0,100000000))}
    return Key

def Ali_Domain_GetRecord(Domainname,RRname):
    Key=Ali_Public()
    Key["Action"]="DescribeDomainRecords"
    Key["DomainName"]=Domainname
    Sign=Ali_Sign("GET",Key)
    Key["Signature"]=Sign
    req=requests.get("http://alidns.aliyuncs.com",params=Key)
    print(req.content)
    for i in json.loads(req.text)["DomainRecords"]["Record"]:
        if i["RR"]==RRname:
            return i

def Ali_Domain_UpdateRecord(Domainname,PRname,NewIP):
    Record=Ali_Domain_GetRecord(Domainname, PRname)
    Record["Action"]="UpdateDomainRecord"
    Record["Value"]=NewIP
    Key=Ali_Public()
    Key.update(Record)
    Sign=Ali_Sign("GET",Key)
    Key["Signature"]=Sign
    req=requests.get("http://alidns.aliyuncs.com",params=Key)
    print(req.text)

def Run():
    print(datetime.datetime.now())
    SI=Vultr(Value="SSVPN")
    Vultr_Destory(SI)
    Vultr_Create()
    time.sleep(120)
    IP=Vultr(Parse="main_ip",Value="SSVPN")
    print(IP)
    print(datetime.datetime.now())
    Ali_Domain_UpdateRecord("fallenangel.cn","ss",IP)
    print(datetime.datetime.now())
