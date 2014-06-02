#coding:utf-8

import struct

PHONE_DAT = "phone.dat"

def getHumanCartType(cartType):
    if cartType == 1:
        return "移动"
    elif cartType ==2:
        return "联通"
    else:
        return "电信"

def getPhoneInfo(phone):
    phone = int(str(phone)[0:7] )
    with open(PHONE_DAT) as f:
        content = f.read()
    
    headFmt = "!4si"
    version,firstRecordOffset = struct.unpack(headFmt,content[:struct.calcsize(headFmt)])
    # print version,firstRecordOffset 
    recordFmt = "!iiB"
    singelRecordLength = struct.calcsize(recordFmt)
    recordNum = ( len(content) - firstRecordOffset) / singelRecordLength 
    l = 0
    r = recordNum
    while l<=r:
        m = (l+r)/2
        currentOffset = firstRecordOffset+m*singelRecordLength
        currentPhone,recordOffset,cartType = struct.unpack(recordFmt,content[ currentOffset:currentOffset+singelRecordLength ])
        if currentPhone > phone:
            r = m -1
        elif currentPhone < phone:
            l = m + 1
        else:
            start = recordOffset + struct.calcsize(headFmt)
            end = start + content[start:].find('\0')
            return "%s|%s"%(content[start:end],getHumanCartType(cartType))

    return None

if __name__ == "__main__":
    for i in range(1890000,1890100):
        print i,getPhoneInfo(i)
