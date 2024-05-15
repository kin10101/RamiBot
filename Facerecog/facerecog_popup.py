import os

# Source path (UNC format) to the target folder within the Samba share
source_path = '\\\\192.168.80.2\\sambashare\\RamiBot\\datasets50'

# Destination path where the symbolic link will be created
destination_path = 'D:\\RamiBot Project\\RamibotReal\\Facerecog\\realdatasets'

# Create the symbolic link using mklink command
os.system(f'mklink /d "{destination_path}" "{source_path}"')

print("Symbolic link created successfully.")
