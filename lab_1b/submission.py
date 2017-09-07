# Author: Matthew Alpert
# Assignment: Lab 1B

from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT8, UINT32, BOOL
from time import sleep
import datetime, random

class ClientInitiate(PacketType):
     DEFINITION_IDENTIFIER = "lab_1b.student_alpert.ClientInitiate"
     DEFINITION_VERSION = "1.0"

     FIELDS = [
          ]

class ServerChallenge(PacketType):
     DEFINITION_IDENTIFIER = "lab_1b.student_alpert.ServerChallenge"
     DEFINITION_VERSION = "1.0"

     FIELDS = [
          ("Hour", UINT8),
          ("Minute", UINT8),
          ("ID", UINT32)
          ]

class ClientResponse(PacketType):
     DEFINITION_IDENTIFIER = "lab_1b.student_alpert.ClientResponse"
     DEFINITION_VERSION = "1.0"

     FIELDS = [
          ("Sum", UINT8),
          ("ID", UINT32)
          ]

class ServerAnswer(PacketType):
     DEFINITION_IDENTIFIER = "lab_1b.student_alpert.ServerAnswer"
     DEFINITION_VERSION = "1.0"

     FIELDS = [
          ("Result", BOOL),
          ("ID", UINT32)
          ]

def basicUnitTest():
     packet1 = ClientInitiate()
     packet1Bytes = packet1.__serialize__()
     packet1a = ClientInitiate.Deserialize(packet1Bytes)
     assert packet1 == packet1a #test if deserialized packet1 is the same

     packet11 = ClientInitiate()
     packet11Bytes = packet11.__serialize__()
     packet11a = ClientInitiate.Deserialize(packet11Bytes)
     assert packet1 == packet1a == packet11 == packet11a #all these packets should be the same, even if they are created at different times
     assert packet1Bytes == packet11Bytes #the serialized packets should be the same as well

     packet2 = ServerChallenge()
     packet2.Hour = datetime.datetime.now().hour
     packet2.Minute = datetime.datetime.now().minute
     print(datetime.datetime.now())
     packet2.ID = random.randint(0,4294967295)
     packet2Bytes = packet2.__serialize__()
     packet2a = ServerChallenge().Deserialize(packet2Bytes)
     assert packet2 == packet2a #test to see if deserialized packet2 is the same
     assert packet1a != packet2a #test to ensure that these 2 packets are different
     assert packet1Bytes != packet2Bytes #serialized packets should be different as well for different packets

     packet3 = ClientResponse()
     packet3.Sum = packet2.Hour + packet2.Minute
     packet3.ID = random.randint(0,4294967295)
     packet3Bytes = packet3.__serialize__()
     packet3a = ClientResponse().Deserialize(packet3Bytes)
     assert packet3 == packet3a #ensure deserialized packets are the same

     packet4 = ServerAnswer()
     if packet3.Sum == (packet2.Hour + packet2.Minute):
          packet4.Result = 1
     elif packet3.Sum != (packet2.Hour + packet2.Minute):
          packet4.Result = 0
     packet4.ID = random.randint(0,4294967295)
     packet4Bytes = packet4.__serialize__()
     packet4a = ServerAnswer().Deserialize(packet4Bytes)
     assert packet4 == packet4a

     packet22 = ServerChallenge()
     packet22.Hour = datetime.datetime.now().hour
     packet22.Minute = datetime.datetime.now().minute
     packet22.ID = random.randint(0,4294967295)
     packet22Bytes = packet22.__serialize__()
     packet22a = ServerChallenge().Deserialize(packet22Bytes)
     assert packet22 == packet22a
     assert packet2 != packet22 #since ServerChallenge has some element of randomness in it, it should be different

     sleep(60) #wait enough time to change the time, unit test moves too quickly
     packet5 = ServerChallenge()
     packet5.Hour = datetime.datetime.now().hour
     packet5.Minute = datetime.datetime.now().minute
     print(datetime.datetime.now())
     packet5.ID = packet2.ID #need to make sure that its not just the ID that is different, but the actual time is different
     packet5Bytes = packet5.__serialize__()
     packet5a = ServerChallenge().Deserialize(packet5Bytes)
     assert packet5 == packet5a
     assert packet2 != packet5 #different times should yield different packets


if __name__=="__main__":
     basicUnitTest()
