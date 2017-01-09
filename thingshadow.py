from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import json

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


# Custom Shadow callback
def customCallback(payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
	if responseStatus == "timeout":
		print("Update request " + token + " time out!")
	if responseStatus == "accepted":
		payloadDict = json.loads(payload)
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Update request with token: " + token + " accepted!")
		print("property: " + str(payloadDict["state"]["desired"]["property"]))
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Update request " + token + " rejected!")



# For certificate based connection
myShadowClient = AWSIoTMQTTShadowClient("pi")
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myShadowClient.configureEndpoint("a16h9u0dkdtqab.iot.ap-southeast-1.amazonaws.com", 8883)
# For Websocket
# myShadowClient.configureEndpoint("YOUR.ENDPOINT", 443)
myShadowClient.configureCredentials("/home/pi/awsCertificate/root-CA.crt", "/home/pi/awsCertificate/1f452c99e4-private.pem.key", "/home/pi/awsCertificate/1f452c99e4-certificate.pem.crt")
# For Websocket, we only need to configure the root CA
# myShadowClient.configureCredentials("YOUR/ROOT/CA/PATH")
myShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myShadowClient.configureMQTTOperationTimeout(5)  # 5 sec


myShadowClient.connect()
# Create a device shadow instance using persistent subscription


# Retrieve the AWS IoT MQTT Client used in the AWS IoT MQTT Shadow Client,naming the shadow as "raspberrypi"
# note that createshadowhandlerwithname() return a deviceshadow object which expose to device shadow interface
# Users can perform shadow operations on this instance to retrieve and modify the corresponding shadow JSON document in AWS IOT Cloud
myDeviceShadow = myShadowClient.createShadowHandlerWithName("raspberrypi", True)

# send payload to device shadow by specifying topic on the first parameter with the standardized value based by Device Shadow MQTT Topics
# myDeviceShadow.publish("$aws/things/raspberrypi/shadow/update","payload",1)

# Shadow operations
#myDeviceShadow.shadowGet(customCallback, 5)
myJSONPayload = '{"state":{"desired":{"property": "meow" }}}'
myDeviceShadow.shadowUpdate(myJSONPayload, customCallback, 5)
#myDeviceShadow.shadowDelete(customCallback, 5)
#myDeviceShadow.shadowRegisterDeltaCallback(customCallback)
#myDeviceShadow.shadowUnregisterDeltaCallback()
