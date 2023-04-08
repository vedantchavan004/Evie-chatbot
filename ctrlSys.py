import os
import pycaw.pycaw as pycaw
import sys

def assistantCtrl(message,response):
    
    if message == "evie stop":
        reply="interrupt"
        response= reply         
        
    elif "open youtube" in message.lower():        
        reply="Opening Youtube"
        response= reply
        os.system("start https://www.youtube.com/")        
            
    elif "change volume" in message.lower():
        # Extract the requested volume level from the message
        volume_level = int(message.split()[-1])
        
        # Check that the requested volume level is within the valid range (0-100)
        if volume_level < 0 or volume_level > 100:
            reply = "Please specify a volume level between 0 and 100."
            response= reply
        else:
            # Use the pycaw library to set the system volume
            sessions = pycaw.AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session.SimpleAudioVolume
                volume.SetMasterVolume(float(volume_level / 100), None)
            reply = f"Volume set to {volume_level}."
            response= reply
    
    else:
        response = response 
        

    return response
        




