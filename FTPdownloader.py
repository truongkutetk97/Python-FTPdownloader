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
    #python ftpdownloader.py -r -u myuser:mypass@127.0.0.1 -s <from> -d <to> -i <.zip> -e <.exe>
    #       1                 2 3  4                        4  5     6  7
###Download from a remote server to another remote 
    #use -b option: bypass

#####Download all file with special pattern in folder

from ftplib import FTP
import os 
import sys
import shutil
import json
import logging

mode = None
userInfo = None
userName = None
Password = None
IPaddr = None
srcPath = []
desPath = None

includeList = []
excludeList = []
listFileInFolder = []
#-----------------------------------------------------------------#
def printUsage():
    logging.info('ARGUMENT INCORRECT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    logging.info('>>>>>USAGE<<<<<')
    logging.info('-----Download single/multiple files:')
    logging.info('python FTPdownloader.py -f -u username:pasword@ServerIPaddress -s <path of file in remote> -s <> -s <>  -d <path of saved file>')
    logging.info('-----Download folder:   ')
    logging.info('python FTPdownloader.py -r -u username:pasword@ServerIPaddress -s <path of folder in remote> -d <path of saved folder>')
    logging.info('>>>>>SAMPLE LINUX<<<<<')
    logging.info('python3 FTPdownloader.py  -f -u myuser:mypass@127.0.0.1 \\')
    logging.info('     	-s "/parent 0/parent 1/James Kurose, Keith Ross - Computer Networking_ A Top-Down Approach.pdf" \\')
    logging.info('     	-s "/parent 0/parent 1/Chacon, Scott_Straub, Ben - Pro Git (2014, Apress) - libgen.lc (1).pdf" \\')
    logging.info('     	-d /mnt/d/test_docker')
    logging.info('>>>>>SAMPLE WINDOWS<<<<<')
    logging.info('python3 FTPdownloader.py  -f -u myuser:mypass@127.0.0.1 `')
    logging.info('     	-s "/parent 0/parent 1/" `')
    logging.info('     	-d D:\\test_docker')

    exit()
#-----------------------------------------------------------------#


#-----------------------------------------------------------------#
def extractFileName(srcPath):
    pathName =""
    fileName = None
    pathSplit = srcPath.split('/')
    for index in range(len(pathSplit) -1 ):
        if pathSplit[index] != "":
            # if pathName!= "":
            pathName += '/'
            pathName += pathSplit[index]
    fileName = pathSplit[len(pathSplit)-1]
    logging.info("PathName:{}, FileName:{}".format(pathName,fileName))
    return (pathName,fileName)
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
def parseArg():
    global mode, userName, Password, IPaddr, userInfo, srcPath, desPath, includeList, excludeList
    if len(sys.argv) <2:
        printUsage()
    if sys.argv[1] == '-f':
        mode=sys.argv[1]
    elif  sys.argv[1] == '-r':
        mode=sys.argv[1]
    elif  sys.argv[1] == '-g':
        mode=sys.argv[1]
    else:
        printUsage()

    for i in range(len(sys.argv)):
        # logging.info(sys.argv[i])
        if sys.argv[i] == '-u':
            if userName != None or Password!= None or IPaddr != None:
                printUsage()
            userInfo = sys.argv[i+1]
            userInfoSplit = userInfo.split(':')
            userName = userInfoSplit[0]
            userInfoSplit = userInfoSplit[1].split('#')
            Password = userInfoSplit[0]
            IPaddr = userInfoSplit[1]
        if sys.argv[i] == '-s':
            srcPath.append(sys.argv[i+1])
        if sys.argv[i] == '-d':
            if desPath != None:
                printUsage()
            desPath=sys.argv[i+1]
        if sys.argv[i] == '-i':
            includeList.append(sys.argv[i+1])
        if sys.argv[i] == '-e':
            excludeList.append(sys.argv[i+1])


    if len(srcPath) ==0 or desPath == None or userName == None or Password ==None or IPaddr ==None:
        printUsage()
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
def downloadFile():
    logging.info("----Start Download----")
    global mode, userName, Password, IPaddr, userInfo, srcPath, desPath, includeList, excludeList
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
            logging.info("File downloaded:{}".format(fileName))
        else:
            logging.info("File not exist:{}".format(fileName))
    logging.info("----Finish Download----")
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
def downloadFolder():
    logging.info("----Start Download----")
    global mode, userName, Password, IPaddr, userInfo, srcPath, desPath, includeList, excludeList
    ftp = FTP(IPaddr)
    ftp.login(user=userName, passwd = Password)
    (pathName, fileName) = extractFileName(srcPath[0])
    logging.info(pathName.split('/')[-1])
    parent_dir =pathName.split('/')[-1]
    work_dir = os.path.join(desPath, parent_dir)
    logging.info(work_dir)
    try: 
        shutil.rmtree(work_dir)
    except OSError as error: 
        logging.info(error) 
    try: 
        os.mkdir(work_dir)
    except OSError as error: 
        logging.info(error)
    downloadFileinFolder(ftp, pathName, work_dir)
    logging.info("----Finish Download----")
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
def downloadFileinFolder(ftp, pathName, work_dir):
    logging.info("Hiii")
    ftp.cwd(pathName)
    work_dir_persist = work_dir
    log = []
    ftp.retrlines('LIST', callback=log.append)
    for file in log:
        work_dir = work_dir_persist
        words =file.split(None, 8)
        filenamee = words[-1]
        logging.info(file)
        logging.info(file[0])
        if file[0] == 'd':
            logging.info("This is dir")
            work_dir = os.path.join(work_dir, filenamee)
            logging.info(work_dir)
            try: 
                os.mkdir(work_dir)
            except OSError as error: 
                logging.info(error) 
            srcPath = os.path.join('/',pathName+'/', filenamee)
            logging.info(srcPath)
            downloadFileinFolder(ftp,srcPath,work_dir)
        else:
            DestPathName = os.path.join(work_dir, filenamee)
            logging.info(DestPathName)
            LocalFile = open(DestPathName, "wb")
            ftp.retrbinary("RETR " + filenamee, LocalFile.write, 8*1024)
            LocalFile.close()
        logging.info(filenamee)
    return True
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
def downloadPattern():
    global mode, userName, Password, IPaddr, userInfo, srcPath, desPath, includeList, excludeList, listFileInFolder
    if len(includeList) == 0 and len(excludeList) == 0:
        printUsage()
    logging.info(json.dumps(includeList, indent=2))
    logging.info(json.dumps(excludeList, indent=2))
    ftp = FTP(IPaddr)
    ftp.login(user=userName, passwd = Password)
    logging.info("Loggin Success!")
    (srcPathName, fileName) = extractFileName(srcPath[0])
    logging.info('srcPathName:{}'.format(srcPathName.split('/')[-1]))
    parent_dir =srcPathName.split('/')[-1]
    work_dir = os.path.join(desPath, parent_dir)
    logging.info('work_dir:{}'.format(work_dir))
    try: 
        shutil.rmtree(work_dir)
    except OSError as error: 
        logging.info(error) 
    try: 
        os.mkdir(work_dir)
    except OSError as error: 
        logging.info(error)
    getAllFileInFolder(ftp, srcPathName, work_dir)
    # logging.info(json.dumps(listFileInFolder, indent=2))

    logging.info("----Finish Download----")
    return True
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
def getAllFileInFolder(ftp, src_pathName, des_work_dir):
    logging.info("Begin getAllFileInFolder")
    ftp.cwd(src_pathName)
    work_dir_persist = des_work_dir
    log = []
    ftp.retrlines('LIST', callback=log.append)
    for file in log:
        ftp.cwd(src_pathName)
        des_work_dir = work_dir_persist
        words =file.split(None, 8)
        filenamee = words[-1]
        logging.info('file:{}'.format(file))
        logging.info('file[0]:{}'.format(file[0]))
        if file[0] == 'd':
            logging.info("This is dir")
            des_work_dir = os.path.join(des_work_dir, filenamee)
            logging.info('des_work_dir:{}'.format(des_work_dir))
            try: 
                os.mkdir(des_work_dir)
            except OSError as error: 
                logging.info(error) 
            srcPath = os.path.join('/',src_pathName+'/', filenamee)
            logging.info('srcPath:{}'.format(srcPath))
            getAllFileInFolder(ftp,srcPath,des_work_dir)
        else:
            if len(includeList) > 0:
                logging.info('IncludeList:{}'.format(filenamee))
                for index in includeList:
                    if index in filenamee:
                        singleFileName=os.path.join(src_pathName, filenamee)
                        logging.info('Single file name:{}'.format(singleFileName))
                        listFileInFolder.append(singleFileName)
                        DestPathName = os.path.join(des_work_dir, filenamee)
                        logging.info('DestPathName:{}'.format(DestPathName))
                        LocalFile = open(DestPathName, "wb")
                        logging.info('DestPathName:{}'.format(DestPathName))
                        ftp.retrbinary("RETR " + filenamee, LocalFile.write, 8*1024)
                        LocalFile.close()
                        break
            if len(excludeList) > 0:
                logging.info('excludeList:{}'.format(filenamee))
                isExcluded = False
                for index in excludeList:
                    logging.info('index:{},{},{}'.format(index,filenamee,filenamee.find(index)))
                    if  index  in filenamee:
                        isExcluded = True
                        break
                if isExcluded != True:
                    singleFileName=os.path.join(src_pathName, filenamee)
                    logging.info('Single file name:{}'.format(singleFileName))
                    listFileInFolder.append(singleFileName)
                    DestPathName = os.path.join(des_work_dir, filenamee)
                    logging.info('DestPathName:{}'.format(DestPathName))
                    LocalFile = open(DestPathName, "wb")
                    ftp.retrbinary("RETR " + filenamee, LocalFile.write, 8*1024)
                    LocalFile.close()
        logging.info('filenamee:{}'.format(filenamee))
    return True
#-----------------------------------------------------------------#

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='logs_file',
                    filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info('FTP DOwnloader v0.1.1')
    parseArg()
    logging.info("Mode:{}".format(mode))
    logging.info("UserName:{} Password:{} RemoteIP:{}".format(userName, Password, IPaddr))
    logging.info("Source:{}".format(srcPath))
    logging.info("Destination:{}".format(desPath))
    logging.info("includeList:{}, {}".format(includeList, len(includeList)))
    logging.info("excludeList:{}, {}".format(excludeList, len(excludeList)))

    if mode == '-f':
        downloadFile()
    elif mode == '-r':
        downloadFolder()
    elif mode == '-g':
        downloadPattern()