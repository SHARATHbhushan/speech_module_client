import asyncio
import tempfile

from playsound import playsound

import edge_tts 



import espeakng
import time
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool

class tts_engine():
    import asyncio
    def __init__(self):
        rospy.Subscriber("tts/phrase", String, self.callback)
        self.pubStatus = rospy.Publisher('/stt_session_key', Bool, queue_size=0)
        self.asynci = asyncio.get_event_loop()

    def callback(self, msg):
        phrase = msg.data
        self.app(phrase)
        
    async def main(phrase):
        """
        Main function
        """

        communicate = edge_tts.Communicate()
        ask = phrase
        with tempfile.NamedTemporaryFile() as temporary_file:
            async for i in communicate.run(ask, voice="Microsoft Server Speech Text to Speech Voice (en-US, GuyNeural)"):
                if i[2] is not None:
                    temporary_file.write(i[2])
            playsound(temporary_file.name)
        print("worked")

    
    def publish_status(self, isSpeaking):
        # Make the status true if it is speaking and false if it is not
        if isSpeaking == True:
            self.pubStatus.publish(False)
            rospy.logdebug("Started Speaking!")
        else:
            self.pubStatus.publish(True)
            rospy.logdebug("Finished Speaking..")
    
    def app(self, phrase):
        
        rospy.loginfo("The robot says: " + phrase)
        self.pubStatus.publish(False)
        self.asynci.run_until_complete(tts_engine.main(phrase))
        if phrase.lower() == "speak to you soon":
            self.pubStatus.publish(False)
        else:
            self.pubStatus.publish(True)
    


if __name__ == '__main__':
    try:
        rospy.init_node('tts_engine', anonymous=True)
        tts = tts_engine()
        rospy.spin() 
        
    except KeyboardInterrupt:
        rospy.loginfo("Stopping tts engine...")
        rospy.sleep(1)
        print("node terminated")