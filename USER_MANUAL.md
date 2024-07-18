# RamiBot - User Manual
## Table of Contents
1. [How to run the program](#how-to-run-the-program)
2. [configuring ports](#configuring-ports)
2. [changing the chatbot responses](#changing-the-chatbot-responses)
3. [Adding new intents](#adding-new-intents)
4. [Adding new responses](#adding-new-responses)
5. [retraining the model](#retraining-the-model)
6. [changing the voice model](#changing-the-voice-model)
7. [changing the face model](#changing-the-face-model)
8. [changing the GUI](#changing-the-gui)
9. [activating the image server](#activating-the-image-server)
10. [connecting to the school database MySQL server](#connecting-to-the-school-database-mysql-server)


## How to run the program
Navigate to the Integrated package directory and run the following python module:
```
    python3 MainApp.py
```
If you're using Pycharm, you can run the program by right-clicking on the MainApp.py file and selecting "Run MainApp".

## Configuring ports
Sometimes, the default port configuration for peripherals like the microphone or camera might not work on your machine. To change the port configuration, navigate to the Integrated package directory and open the file config.py. Change the port number in the following line:
```
    # face recognition
    CAMERA_INDEX = 0
    
    # speech recognition
    DEVICE_INDEX = 3
```
To see what ports are assigned to your peripherals, run the following functions under either the Voicebot or Facerecog packages:

### in Facerecog/face_recog_module:

```
if __name__ == '__main__':
    available_cameras = get_camera_list()
    print(f"Available cameras: {available_cameras}")

    if available_cameras:
        video_capture = cv2.VideoCapture(available_cameras[0])
    else:
        print("No cameras found")
```
sometimes this function doesn't work, so just iterate through the camera list manually by changing the index in the following line until you find the correct camera index:

in Integrated/config.py, change this the value of this line:
```
    # face recog parameters
    CAMERA_INDEX = 0
```


### in Voicebot/voice_assistant_module:
This code will print out a list of mic devices alongside their respective device indexes.
```
if __name__ == '__main__':
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
```

## Activating the image server
Images are stored in the Assets folder and are served by the image server. To activate the image server,
you need to access the airhub server through SSH connection. Look for Sir Luigi for the server credentials.
folder and are served by the image server. 


To activate the image server, follow these steps:

#### 1. Access the Airhub Server:
- Obtain the server credentials from Sir Luigi.
- Establish an SSH connection to the airhub server using the credentials provided.
- You can use puTTY, Terminus (for android), Tabby Terminal, or any terminal emulator that can do SSH.

#### 2. Navigate to the RamiBot Directory:
- Files are stored in the RamiBot directory. Once you have gained access, navigate to that file using this command:

```
    cd var/www/html/RamiBot
```
#### 3. Activate the Virtual Environment:
Navigate to the virtual environment directory and activate it. 
Assuming the virtual environment directory is within the RamiBot directory:
```
    source ramivenv/bin/activate
```

then run the following python module by writing:
```
    python3 serverside.py
```
