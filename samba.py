import smbclient

server = "samba_server_address"
username = "your_username"
password = "your_password"

smbclient.register_session("samba_server_address", username="your_username", password="your_password")

with smbclient.open_file(r"\\samba_server_address\path\to\file", mode='r', username='your_username', password='your_password') as file:
    content = file.read()

print(content)