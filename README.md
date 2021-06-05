#sample command:
python3 FTPdownloader.py  -f -u myuser:mypass@127.0.0.1 \
	-s "/parent 0/parent 1/James Kurose, Keith Ross - Computer Networking_ A Top-Down Approach.pdf" \
	-s "/parent 0/parent 1/Chacon, Scott_Straub, Ben - Pro Git (2014, Apress) - libgen.lc (1).pdf" \
	-d /mnt/d/test_docker
	
python3 FTPdownloader.py  -r -u myuser:mypass@127.0.0.1 \
	-s "/parent 0/parent 1/" \
	-d /mnt/d/test_docker
	
python3 FTPdownloader.py  -f -u myuser:mypass@127.0.0.1 `
	-s "/parent 0/parent 1/James Kurose, Keith Ross - Computer Networking_ A Top-Down Approach.pdf" `
	-s "/parent 0/parent 1/Chacon, Scott_Straub, Ben - Pro Git (2014, Apress) - libgen.lc (1).pdf" `
	-d D:\test_docker
	
python3 FTPdownloader.py  -r -u myuser:mypass@127.0.0.1 `
	-s "/parent 0/parent 1/" `
	-d D:\test_docker
	
	
#create docker enviroment with ftp server to test, require docker installed:
#FTP server fauria/vsftpd to create
#https://hub.docker.com/r/fauria/vsftpd/

docker run -d \
-v /mnt/d/test_docker:/home/vsftpd \
-p 22:22 -p 20:20 -p 21:21 -p 21100-21110:21100-21110 \
-e FTP_USER=myuser -e FTP_PASS=mypass \
-e PASV_ADDRESS=127.0.0.1 -e PASV_MIN_PORT=21100 -e PASV_MAX_PORT=21110 \
--name vsftpd --restart=always fauria/vsftpd

#Add user to ftp server
docker exec -i -t vsftpd bash
mkdir /home/vsftpd/myuser
echo -e "myuser\nmypass" >> /etc/vsftpd/virtual_users.txt
/usr/bin/db_load -T -t hash -f /etc/vsftpd/virtual_users.txt /etc/vsftpd/virtual_users.db
exit
docker restart vsftpd
