import os 
import eel
from engine.features import *

eel.init("www")

# Play the assistant sound when the application starts
playAssitantSound()



os.system('start msedge.exe --app="http://localhost:8000/index.html"')
eel.start("index.html",mode=None,host="localhost",block=True)

# pip install playsound==1.2.2
# pip install Eel



