import re

def Read_Headers(file):
    headerDict = {}
    f = open(file,'r')
    headersText = f.read()
    headers = re.split('\n',headersText)
    for header in headers:
        result = re.split(':',header,maxsplit=1)
        headerDict[result[0]] = result[1].strip()
    f.close()
    return headerDict

if __name__ == '__main__':
    print(Read_Headers('head_tm.txt'))