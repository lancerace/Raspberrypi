import RPi.GPIO as GPIO #controlling GPIO Pin for raspberry pi
from lib_nrf24 import NRF24
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time
#download spidev library from wget https://github.com/Gadgettoid/py-spidev/archive/master.zip
import spidev
import json
import logging


'''
set up GPIO numbering system in the format of BCM. 2 format available.
GPIO.Board & GPIO.BCM
'''

# Use GPIO numbers not pin numbers 
GPIO.setmode(GPIO.BCM)

#setup addresses for transceiver

#there is 2 addresses. 1 for send address,another one for recieve address
pipes = [[ 0xE8, 0xE8, 0xF0, 0xF0, 0xE1],[0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]


#set up radio and activate
radio = NRF24(GPIO, spidev.SpiDev())
#(CSN, CE) .CSN =CE_0(GPIO8)
radio.begin(0, 25)
#maximum size is actually 32byte
radio.setPayloadSize(32)
radio.setChannel(0x76)
#consider slower and more secure data rate. slower actually give better range
radio.setDataRate(NRF24.BR_1MBPS)
#set power level. since arduino and raspberry pi is near each other. min power will do.
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

#input 2nd address for reading pipe. This is for receiving data
radio.openReadingPipe(1, pipes[1])
radio.startListening()
radio.stopListening()
radio.printDetails()
radio.startListening()
while True:

#check if radio is available, if no. put in sleep mode
    while not radio.available(0):
#time.sleep(10)
        time.sleep(1000/1000000.0)

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))

    print("Translating our received Message into unicode character..*");
    translatedMessage = ""

#range of unicode character
    for n in receivedMessage:
        if (n >= 32 and n <= 126):
            translatedMessage += chr(n)
#chr(i)  = Return a string of one character whose ASCII code is the integer i
                
    print("received decoded message is: {}".format(translatedMessage))

    if not translatedMessage:
        #handle empty data received from arduino because data tranmission might not receive anything every sec to solve index out of bound on array variable (dataArray)
        print("string is empty")
    else:    
        print(translatedMessage)
        dataArray = translatedMessage.split()
        
        data= {'temperature': dataArray[0],
               'humidity': dataArray[1],
               'lux' : dataArray[2]
               }
        print(data)

#clean up previous pin configuration
GPIO.cleanup() 





