import os
import sys
import math



#本地链接 IPv6 地址. . . . . . . . : fe80::201e:524e:3070:a29a%16
#
#
#未知适配器 oc-helper:00-FF-39-68-F2-C1           get_mac_address():00-FF-39-68-F2-C1
#以太网适配器 以太网:70-B5-E8-99-59-82             get_uumac_address():70b5e8995982
#无线局域网适配器 本地连接* 1:8E-C8-4B-F4-25-F5
#无线局域网适配器 本地连接* 2:9E-C8-4B-F4-25-F5
#以太网适配器 以太网 2:00-FF-AA-65-9D-A7
#无线局域网适配器 WLAN:8C-C8-4B-F4-25-F5
#
#

maptable = [[4,8,3,1,7,5,2,6,9,0],
            [8,1,6,7,2,9,3,4,0,5],
            [6,7,2,4,1,5,0,9,8,3],
            [3,8,0,5,1,4,6,2,7,9],
            [8,1,3,6,0,7,9,4,5,2],
            [7,4,9,2,5,0,8,3,6,1],
            [0,9,5,2,6,4,1,7,3,8],
            [5,1,3,8,0,7,9,4,2,6],
            [9,6,0,4,5,1,8,2,3,7],
            [1,8,5,9,6,3,7,4,0,2]]

def get_macaddress():
    mac = None
    if sys.platform == "win32":
        isEther = False
        for line in os.popen("ipconfig /all"):
            # if line.lstrip().startswith("物理地址"):
            if '以太网' in line:
                isEther = True
            if isEther and '物理地址' in line:
                # mac = line.split(":")[1].strip().replace("-", ":")
                mac = line.split(":")[1].strip()
                break
    else:
        isEther = False
        for line in os.popen("/sbin/ifconfig"):
            if '以太网' in line:
                isEther = True
            if isEther and '物理地址' in line:
                mac = line.split(":")[1].strip()
                break
    return mac


def mac_to_licence(Etheraddress:str):
    Etherstr = ''
    etable = {'A':'10','B':'11','C':'12','D':'13','E':'14','F':'15'}
    for c in Etheraddress:
        if c != '-': 
            if c.isalpha():          
                Etherstr += str(int(etable[c])%10)
            else:
                Etherstr += c  
    print(Etherstr)
    i = 1
    sum = 0
    for x in Etherstr:
        sum += i*int(x)
        i += 1

    index = sum%10
    licence = ''
    i = 0
    for x in Etherstr:
        licence += str(maptable[((index+i+int(x))%10)][int(x)])
        i += 1
    return licence


print(mac_to_licence(get_macaddress()))

