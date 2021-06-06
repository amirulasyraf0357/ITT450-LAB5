import socket
import tqdm
import os
from cryptography.fernet import Fernet


SEPARATOR="<SEPARATOR>"
BUFFER_SIZE=8888

host="192.168.56.101"
port=8888


filename = input(str("Please enter the name of the file to be transfer : ")) #enter name of file that about to be transfer including it file type

filesize=os.path.getsize(filename)

print("Encrypt file...")
with open('filekey.key', 'rb') as filekey:
    key = filekey.read()
  
# using the generated key
fernet = Fernet(key)

with open(filename, 'rb') as file:
    original = file.read()

# encrypting the file
encrypted = fernet.encrypt(original)

with open(filename, 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
  
s=socket.socket()

s.connect((host,port))

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress=tqdm.tqdm(range(filesize),f"Sending{filename}",unit="B",unit_scale=True,unit_divisor=1024)

with open(filename,"rb") as f:
	for _ in progress:
		bytes_read=f.read(BUFFER_SIZE)
		if not bytes_read:
			break
		s.sendall(bytes_read)
		progress.update(len(bytes_read))
s.close()