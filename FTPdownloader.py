#FTPdownloader
##Feature

###Download single file from folder, can download multiple file 
    #use -f
    #python ftpdownloader.py -f -u myuser:mypass@127.0.0.1 -s <from> -d <to>
    #       1                 2 3  4                        4  5     6  7

###Download recursive a folder 
    #use -r option: recursive
    #python ftpdownloader.py -r -u myuser:mypass@127.0.0.1 -s <from> -d <to>
    #       1                 2 3  4                        4  5     6  7

###Download file with regex option in folder
    #use -g option: regex
###Download from a remote server to another remote 
    #use -b option: bypass

#####Download all file with special pattern in folder

from ftplib import FTP
import os 
import sys
import shutil

mode = None
userInfo = None
userName = None
Password = None
IPaddr = None
srcPath = []
desPath = None

#-----------------------------------------------------------------#
def printUsage():
    print('ARGUMENT INCORRECT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('>>>>>USAGE<<<<<')
    print('-----Download single/multiple files:')
    print('python FTPdownloader.py -f -u username:pasword@ServerIPaddress -s <path of file in remote> -s <> -s <>  -d <path of saved file>')
    print('-----Download folder:   ')
    print('python FTPdownloader.py -r -u username:pasword@ServerIPaddress -s <path of folder in remote> -d <path of saved folder>')
    print('>>>>>SAMPLE LINUX<<<<<')
    print('python3 FTPdownloader.py  -f -u myuser:mypass@127.0.0.1 \\')
    print('     	-s "/parent 0/parent 1/James Kurose, Keith Ross - Computer Networking_ A Top-Down Approach.pdf" \\')
    print('     	-s "/parent 0/parent 1/Chacon, Scott_Straub, Ben - Pro Git (2014, Apress) - libgen.lc (1).pdf" \\')
    print('     	-d /mnt/d/test_docker')
    print('>>>>>SAMPLE WINDOWS<<<<<')
    print('python3 FTPdownloader.py  -f -u myuser:mypass@127.0.0.1 `')
    print('     	-s "/parent 0/parent 1/" `')
    print('     	-d D:\\test_docker')

    exit()
#-----------------------------------------------------------------#


#-----------------------------------------------------------------#
def extractFileName(srcPath):
    listFolder =None
    pathName =""
    fileName = None
    pathSplit = srcPath.split('/')
    for index in range(len(pathSplit) -1 ):
        if pathSplit[index] != "":
            # if pathName!= "":
            pathName += '/'
            pathName += pathSplit[index]
    fileName = pathSplit[len(pathSplit)-1]
    print("PathName:{}, FileName:{}".format(pathName,fileName))
    return (pathName,fileName)
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
def parseArg():
    global mode, userName, Password, IPaddr, userInfo, srcPath, desPath
    if len(sys.argv) <2:
        printUsage()
    if sys.argv[1] == '-f':
        mode=sys.argv[1]
    elif  sys.argv[1] == '-r':
        mode=sys.argv[1]
    else:
        printUsage()

    for i in range(len(sys.argv)):
        # print(sys.argv[i])
        if sys.argv[i] == '-u':
            if userName != None or Password!= None or IPaddr != None:
                printUsage()
            userInfo = sys.argv[i+1]
            userInfoSplit = userInfo.split(':')
            userName = userInfoSplit[0]
            userInfoSplit = userInfoSplit[1].split('@')
            Password = userInfoSplit[0]
            IPaddr = userInfoSplit[1]
        if sys.argv[i] == '-s':
            srcPath.append(sys.argv[i+1])
        if sys.argv[i] == '-d':
            if desPath != None:
                printUsage()
            desPath=sys.argv[i+1]


    if len(srcPath) ==0 or desPath == None or userName == None or Password ==None or IPaddr ==None:
        printUsage()
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
def downloadFile():
    print("----Start Download----")
    global mode, userName, Password, IPaddr, userInfo, srcPath, desPath
    ftp = FTP(IPaddr)
    ftp.login(user=userName, passwd = Password)
    for index in range(len( srcPath )):
        (pathName, fileName) = extractFileName(srcPath[index])
        fileValid=0
        ftp.cwd(pathName)
        listCurrentFile=ftp.nlst()
        for file in listCurrentFile:
            if file == fileName:
                fileValid =1
        if fileValid:
            DestPathName = os.path.join(desPath, fileName)
            LocalFile = open(DestPathName, "wb")
            ftp.retrbinary("RETR " + fileName, LocalFile.write, 8*1024)
            LocalFile.close()
            print("File downloaded:{}".format(fileName))
        else:
            print("File not exist:{}".format(fileName))
    print("----Finish Download----")
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
def downloadFolder():
    print("----Start Download----")
    global mode, userName, Password, IPaddr, userInfo, srcPath, desPath
    ftp = FTP(IPaddr)
    ftp.login(user=userName, passwd = Password)
    (pathName, fileName) = extractFileName(srcPath[0])
    print(pathName.split('/')[-1])
    parent_dir =pathName.split('/')[-1]
    work_dir = os.path.join(desPath, parent_dir)
    print(work_dir)
    try: 
        shutil.rmtree(work_dir)
        os.mkdir(work_dir)
    except OSError as error: 
        print(error) 

    downloadFileinFolder(ftp, pathName, work_dir)

    # print(log[0])
    # files = (' '.join(line.split()[8:]) for line in log)
    # print(files)
    # files_list = list(files)
    # print(files_list)
    print("----Finish Download----")
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
def downloadFileinFolder(ftp, pathName, work_dir):
    print("Hiii")
    ftp.cwd(pathName)
    log = []
    ftp.retrlines('LIST', callback=log.append)
    for file in log:
        words =file.split(None, 8)
        filenamee = words[-1]
        print(file)
        print(file[0])
        if file[0] == 'd':
            print("This is dir")
            work_dir = os.path.join(work_dir, filenamee)
            print(work_dir)
            try: 
                os.mkdir(work_dir)
            except OSError as error: 
                print(error) 
            srcPath = os.path.join('/',pathName+'/', filenamee)
            print(srcPath)
            downloadFileinFolder(ftp,srcPath,work_dir)
        else:
            DestPathName = os.path.join(work_dir, filenamee)
            print(DestPathName)
            LocalFile = open(DestPathName, "wb")
            ftp.retrbinary("RETR " + filenamee, LocalFile.write, 8*1024)
            LocalFile.close()
        print(filenamee)
    return True
#-----------------------------------------------------------------#

if __name__ == "__main__":
    parseArg()
    print("Mode:{}".format(mode))
    print("UserName:{} Password:{} RemoteIP:{}".format(userName, Password, IPaddr))
    print("Source:{}".format(srcPath))
    print("Destination:{}".format(desPath))

    if mode == '-f':
        downloadFile()
    elif mode == '-r':
        downloadFolder()
