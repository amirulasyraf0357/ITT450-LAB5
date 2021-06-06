
import socket
import tqdm
import os
from cryptography.fernet import Fernet

SERVER_HOST="0.0.0.0"
SERVER_PORT=8888
BUFFER_SIZE=4096
SEPARATOR="<SEPARATOR>"

s=socket.socket()
print("Socket successfully created")

s.bind((SERVER_HOST,SERVER_PORT))
print("socket binded to " + str(SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket,address=s.accept()
print(f"[+] {address} is connected.")

received=client_socket.recv(BUFFER_SIZE).decode()
filename,filesize=received.split(SEPARATOR)

filename=os.path.basename(filename)

filesize=int(filesize)

progress=tqdm.tqdm(range(filesize),f"Receiving{filename}",unit="B",unit_scale=True,unit_divisor=1024)

# opening the key
with open('serverkey.key', 'rb') as filekey:
    key = filekey.read()
  
# using the generated key
fernet = Fernet(key)

with open(filename,"wb") as f:


        for _ in progress:
                bytes_read=client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                        break
                f.write(bytes_read)
                progress.update(len(bytes_read))

with open(filename, 'rb') as enc_file:
    encrypted = enc_file.read()
    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

        # opening the file in write mode and
        # writing the decrypted data
with open(filename, 'wb') as dec_file:
    dec_file.write(decrypted)

client_socket.close()
s.close()