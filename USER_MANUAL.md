# RamiBot - User Manual
## Table of Contents
1. [How to run the program](#how-to-run-the-program)
2. [Configuring ports](#Configuring-ports)
3. [Modifying the Chatbot/Voicebot intents](#Modifying-the-Chatbot/Voicebot-intents)
4. [Adding new intents](#Adding-new-intents)
5. [Changing the intent responses](#Changing-the-intent-responses)
6. [Activating the image server](#Activating-the-image-server)
7. [Changing image server contents](#Changing-image-server-contents)
8. [Changing Voice](#Changing-Voice)

## How to run the program
Navigate to the Integrated package directory and run the following python module:
```
    python3 RAMIBOT.py
```
If you're using Pycharm, you can run the program by right-clicking on the MainApp.py file and selecting "Run MainApp".

## Connecting to the school database MySQL server
RamiBot needs to be connected to the school database to access the necessary information related to the school.


To connect to the school database MySQL server, you need to have the necessary credentials. modify the following lines in the Integrated/config.py file:
```
    # SQL profile for Localhost in laptop
    # HOST = "localhost"
    # USER = "kin"
    # PASSWORD = "asdf"
    # DATABASE ="ramibot_local"
    # AUTOCOMMIT = True
```
Do note that Rami needs to be connected to the APC network for this to work. Contact Sir Luigi for the necessary credentials.

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
## Modifying the Chatbot/Voicebot intents
To modify and edit the responses of RamiBot, navigate to the Integrated package and open:
```
    intents.json
```
This file contains the intents and responses of the chatbot. You can add, remove, or modify the intents and responses in this file.

if in any case that you made a typo or an error in the intents.json file, 
you can use the jsonformatter.org to check the syntax of the file.

or run the following module to check for missing values in the intents.json file:
```
    python3 jsonfinder.py
```
## Adding new intents
To add a new intent, follow this format:
```
    {
        "tag": "intent_name",
        "patterns": ["pattern1", "pattern2", "pattern3"],
        "responses": ["response1", "response2", "response3"]
    }
```
Example:
```
    {
        "tag": "greeting",
        "patterns": ["Hi", "Hello", "Hey", "Greetings"],
        "responses": ["Hello! How can I help you?", "Hi! How can I help you?", "Hey! How can I help you?"]
    }
```

there are also additional parameters that you can add to the intents.json file:
```
    {
        "tag": "intent_name",
        "patterns": ["pattern1", "pattern2", "pattern3"],
        "responses": ["response1", "response2", "response3"],
        "source_image": "image_name",
        "navigate_to": "screen_name"
    }
```
These are optional parameters that you can add to modify the behavior of the voicebot feature.

- source_image - takes in the name of the image file stored in the Assets folder. This image will be displayed in the GUI when the intent is triggered.
- navigate_to - takes in the name of the screen in the GUI that the program will navigate to when the intent is triggered.

After adding the new intent, you need to retrain the model to reflect the changes.


## Changing the intent responses

Example:
```
    {
        "tag": "greeting",
        "patterns": ["Hi", "Hello", "Hey", "Greetings"],
        "responses": ["Hello! How can I help you?", "Hi! How can I help you?", "Hey! How can I help you?"]
    }
```
to:
```
    {
        "tag": "greeting",
        "patterns": ["Hi", "Hello", "Hey", "Greetings"],
        "responses": ["Hello my dear", "wazzup homie", "do I know you? why are you talking to me"]
    }
```

You don't need to retrain the model after changing the responses. 
Though it is recommended to re-run the program to see the changes.





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
To stop or terminate the script, press Ctrl+C.

## Changing image server contents
To change the contents of the image server, you need to have samba installed on your machine. 
Samba is a software suite that provides seamless file and print services to SMB/CIFS clients.

To install samba, run the following command:
```
    sudo apt-get install samba
```
After installing samba, you can access the image server by navigating to the following directory in your file explorer:
```
    smb:// nakalimutan ko marj kaw na magtuloy hehe
```
You will be prompted to enter your credentials. Use the same credentials you used to access the airhub server.

After accessing the image server, you can now add, remove, or modify the images stored in the Assets folder.
please make sure to follow the naming convention of the images to avoid errors in the program.
The names of the images should be in title case and should not contain spaces. use underscores (_) instead.
Names are directly used as the button names in the GUI. __Failure to follow the naming convention will result in the image not being displayed in the GUI.__

Example:
```
    Correct: "Sample_Image.png"
    Incorrect: "sample image.png"
```

## Changing Voice
PiperTTS is the text-to-speech engine used by RamiBot. 
To change the voice of the text-to-speech engine, you need to modify the following lines in the Integrated/voicebot/voice_assistant_module.py file:
```
    def speak(text):
        tts = gTTS(text=text, lang='en')
        filename = 'temp.mp3'
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
```


