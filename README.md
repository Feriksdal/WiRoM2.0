# Wirom2.0 Introduction

This projct is part of my master thesis, and builds upon the work by Joakim Grutle ([original repository](https://github.com/joakimgrutle/WiRoM)). \
Wirom2.0 is an extensible mission planner with usages for different levels of end-users.

![](/Documentation/usage_screenshots/front_page_image.png) 

### YouTube Links to example mission scenarios: 
#### Mission Scenarios
YouTube Playlist: https://youtube.com/playlist?list=PLqDx8urZiY8ww7fJ5Z74JBvw3Md-WvTDG

#### Multi-Robot Mission Demonstration
YouTube Link: https://youtu.be/gWVboH-PivE


#### Large Package Delivery System
YouTube Link: https://youtu.be/wN0N37AJlYo

## Documentation:
Documentation can be found under [**/Documentation**](https://github.com/gunnarkleiven/WiRoM2.0/tree/master/Documentation), 

## Missing Dependensies  
Some users may have to get a hold of dependensies, such as [request](https://pypi.org/project/requests/) and [Pika](https://pika.readthedocs.io/en/stable/).  
Open a terminal, go to where you’ve installed Python (most likely in “program files”).
Then go into the script folder, from there you can run ``pip install pika``, and  ``pip install requests``.


# Quick Startup

Here is a shortended list of instructions for users (windows) that have already installed and run WiRom once on their computer:
Open powershell, or any terminal you prefer
## Terminal 1  
   Change directory using
   ```
   cd ~\WiRoM2.0\web_interface
   ```
   From there, set the envoirment variable; NODE_OPTIONS with:
   ```
   $env:NODE_OPTIONS = "--openssl-legacy-provider"
   ```  
   Afterwards, run it
   ```
   npm start
   ```
   
## Terminal 2  
simliar steps as above, change directory, set envoirment variable, the go back to the main folder and run flask
```
cd ~\WiRoM2.0\backend\.venv\Scripts> .\activate
```
```
$env:FLASK_APP = "backend"
```
```
cd ~\WiRoM2.0\
```
```
flask --app backend run
```
## Terminal 3  
run webots from it's location
```
cd '~\..\..\Program Files\Webots\msys64\mingw64\bin\'
```
```
.\webots.exe --stream
```

# Setup Manual


## Required installations

### Webots
Install this version of Webots: https://github.com/cyberbotics/webots/releases/tag/R2021b
 
### Python:
Download Python 3.9 from their website: 
https://www.python.org/downloads/release/python-3912/ 
#### Note:
We are using this version because Webots only supports up to Python 3.9. Even though the controllers are not implemented through the editor in Webots, it’s best to use the same version to make sure that they are compatible. 


### Node.js / npm:
Downloaded from: https://nodejs.org/en/ 

### RabbitMQ:
Choose the correct operating system from: 
https://www.rabbitmq.com/download.html \
With MacOS it is recommended to use the *Homebrew* package installer.\
On Windows it is recommended to either use the *Chocolatey* package manager or use the installer as an administrative user.\
*Note*: In some cases, e.g., when installing RabbitMQ through the *Chocolatey* package manager, Python 3.10 is installed as well. This creates a conflict for Webots,
because it can only run on Python versions up to 3.9. If a higher version of Python is used, please install version 3.9 and use this instead. 

### Command Line Interface: 
To follow along the next steps, you need to use command line interface. \
On Windows, I have mainly been using the Windows Terminal: \
https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701?hl=en-us&gl=US \
MacOS users can use the Terminal command line. 

### Cloning the repository
To download the source code, clone the repository to your machine using the command: 
```
git clone https://github.com/gunnarkleiven/WiRoM2.0.git
```
To run the system, you need to run 3 processes:
-	The web interface
-	The backend Server
-	Webots simulator

## Setting up the DSL (optional)
This step is for the users who wish to use the Domain Specific Language to generate new robots, either through the provided editor in the web interface or by using VC Code. \
Navigate into the *robot-generator* folder:
```
cd Wirom2.0/robot-generator
```
and run
```
npm install
```
For a longer walkthrough of the Robot-Generator DSL, see the documentation in *Wirom2.0/Documentation/dsl_usage_guide.md*



## Running the web interface 
Navigate to the *web_interface* folder:
```
cd Wirom2.0/web_interface
```
Before running it for the first time, you need to install the required packages by running the command
```
npm install
```
After this, start the web interface by running
```
npm start
```

## Running the flask (Python) server
Navigate to the proper folder by the command
```
cd Wirom2.0/backend
```
To help manage the different dependencies, it is useful to create a Python virtual environment. When you install it for the first time, run the following command \
on **Windows**:
```
python -m venv .venv
```
or on **macOS/Linux**:
```
python3 -m venv .venv
```
The last argument is the name of the directory of the environment, in this case *".venv"* \
\
To initiate the virtual environment, run the command \
On **Windows**
```
./.venv/Scripts/activate
```
on **Mac**
```
source .venv/bin/activate
```
You should see the name of your virtual environment displayed somewhere at the bottom of your terminal window, depending on your settings for the CLI. \
To exit the virtual environment, use the command
```
deactivate
```

After this, you need to install the dependencies. This is done with the command
```
pip install -r requirements.txt
```

Next step is to set the Flask environment variable, using the command
On **Windows**
```
$env:FLASK_APP = "backend"
```
Or on **MacOS**
```
export FLASK_APP=backend
```
Finally, navigate one folder up
```
cd ..
```
And then start the server
```
flask run
```

## Running Webots
To run Webots in the streaming mode, you need to start it with the **--stream** option. \
It is recommended to do this, to get the full application displayed in the web interface. However, it is also possible to run Webots as a normal program/application, without having it stream directly to the browser.\
First, navigate to the Webots folder. This location depends both on the operating system as well as the user settings chosen when installing it. For *Windows* it is commonly located at *'\Program Files\Webots\msys64\mingw64\bin\'*. On *MacOS* *TODO double check the location for mac* *\AppData\Local\Programs\Webots\msys64\mingw64\bin*. \

To start Webots on Windows, run
```
./webots.exe --stream
```
or on Mac:
```
./webots --stream
```

Finally, open the world file **delivery-missionUpdated.wbt** located at *Wirom2.0/backend/worlds/delivery-missionUpdated.wbt*


## Exiting the processes
To stop any of the processes running, simply press **"Ctrl + c"** for Windows or **"control + c"** for Mac in their respective terminal windows.




# Questionnaire and the Results
[Link to Questionnaire](https://forms.gle/pJenEdvGNWA5XqHKA) \
[Link to questionnaire results](https://docs.google.com/spreadsheets/d/1D_NcRZRw7PmODAQEjfruaG6gOBp2WE-AdQlvPdiA9JM/edit?usp=sharing)
