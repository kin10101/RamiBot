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
Sometimes, the default port configuration for peripherals like the microphone or camera might not work on your machine. To change the port configuration, navigate to the Integrated package directory and open the file Config.py. Change the port number in the following line:
```
    
```
To see what ports are assigned to your peripherals, run the following functions under either the 
```
    ls /dev
```


## Activating the image server
Images are stored in the Assets folder and are served by the image server. To activate the image server, run the following python module:
```
    python3 serverside.py
```
