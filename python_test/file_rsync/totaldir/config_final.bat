::python脚本的文件路径
SET PY_PATH=C:/Users/Administrator/Desktop/跨平台文件同步/
::rsync的可执行文件路径
SET RSYNCEXE_PATH=E:/cwrsync/rsync_client/
::rsync监控的文件目录
SET RSYNC_PATH=D:/101/Server
::rsync指令的src参数，表示源路径
SET C2S_SRC=/cygdrive/D/101/
::rsync指令的dst参数，表示目标路径
SET C2S_DST=root@192.168.9.209::qin/
::rsync指令的src参数，表示客户端主动更新服务端修改的文件的源路径
SET UPDATE_SRC=root@192.168.9.209::qin/
::rsync指令的src参数，表示客户端主动更新服务端修改的文件的目标路径（和srcPath一样）
SET UPDATE_DST=/cygdrive/D/101/
::标识连接的用户名
SET CLIENT_NAME=qin
::rsync指令的本地密码文件路径
SET RSYNC_PW_FILE=/cygdrive/E/cwrsync/rsync_client/rsyncd.password
::服务器的ip和端口信息
SET SERVER_IP_AND_PORT=192.168.9.209:5570

python %PY_PATH%client.py %CLIENT_NAME% %RSYNCEXE_PATH%rsync.exe %RSYNC_PATH% %C2S_SRC% %C2S_DST% %UPDATE_SRC% %UPDATE_DST% %RSYNC_PW_FILE% %SERVER_IP_AND_PORT%
pause
exit