from PyPDF2 import PdfFileReader, PdfFileWriter
from io import FileIO as file
import os 

def printMeta(fileName):
    pdfFile = PdfFileReader(file(fileName, 'rb'))
    docInfo = pdfFile.getDocumentInfo()
    print('[*] PDF MetaData For: ' + str(fileName))
    for metaItem in docInfo:
        print(('[+] ' + metaItem + ':' + docInfo[metaItem]))

if __name__ == '__main__':
    #print(os.getcwd())
    printMeta('测试文档.pdf')