import paramiko

host = '136.166.4.58' # 접속할 서버 주소
transport = paramiko.transport.Transport(host)

# 사용자 정보
userid = 'seyeol.park'
password = 'Sweethome1179!'
# 경로
remotepath = '/ftpbaeg3-grp/Time_S/SW/QPF/220412_V60030a/UPC'
localpath = 'C:/Users/seyeol'

transport.connect(username=userid, password=password) # connect 함수를 사용하여 사용자 계정을 추가
sftp = paramiko.SFTPClient.from_transport(transport) # sftp 객체 생성

sftp.chdir(remotepath) # 서버 경로를 전달하여 접속
files = sftp.listdir() # 해당 경로에 있는 파일명 조회

# remote/local 파일의 전체경로 설정
remote_files = []
local_files = []
if files: # remote
    for f in files:
        remote_files.append(remotepath + '/' + f)
for f in files: # local
    local_files.append((localpath + '/' + f))
    
# 서버에 있는 패키지 파일을 로컬로 다운로드
for idx in range(len(files)):
    sftp.get(remote_files[idx], local_files[idx])

# 필수로 닫아줘야 함
sftp.close()
transport.close()



