#include <WiFi.h>
#include <PubSubClient.h>


void callback(char* subscribetopic, byte* payload, unsigned int payloadLength);


#define ORG "lrv63o"//IBM ORGANITION ID
#define DEVICE_TYPE "ESP32"
#define DEVICE_ID "IBM123"
#define TOKEN "(GgH2GfMqCHfAC&nRw"    
String data3;
float dist;

char server[] = ORG ".messaging.internetofthings.ibmcloud.com";

char publishTopic[] = "iot-2/evt/Data/fmt/json";

char subscribetopic[] = "iot-2/cmd/test/fmt/String";

char authMethod[] = "use-token-auth";
char token[] = TOKEN;
char clientId[] = "d:" ORG ":" DEVICE_TYPE ":" DEVICE_ID;//client id


WiFiClient wifiClient; t
PubSubClient client(server, 1883, callback ,wifiClient);

int alarm = 4;
int trig = 5;
int echo = 18;
void setup()
{
Serial.begin(115200);
pinMode(trig,OUTPUT);
pinMode(echo,INPUT);
pinMode(alarm, OUTPUT);
delay(10);
wificonnect();
mqttconnect();
}
void loop()
{

 digitalWrite(trig,LOW);
  digitalWrite(trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(trig,LOW);
  float dur = pulseIn(echo,HIGH);
  float dist = (dur * 0.0343)/2;
  Serial.print ("Distancein cm");
  Serial.println(dist);
 

  PublishData(dist);
  delay(1000);
  if (!client.loop()) {
    mqttconnect();
  }
}



void PublishData(float dist) {
  mqttconnect();
 
  String object;
  if (dist <100)
  {
    digitalWrite(LED,HIGH);
    Serial.println("object is near");
    object = "Near";
  }
  else
  {
    digitalWrite(LED,LOW);
    Serial.println("no object found");
    object = "No";
  }

  String payload = "{\"distance\":";
  payload += dist;
  payload += "," "\"object\":\"";
  payload += object;
  payload += "\"}";

 
  Serial.print("Sending payload: ");
  Serial.println(payload);

 

 
  if (client.publish(publishTopic, (char*) payload.c_str())) {
    Serial.println("Publish ok");

  }
else
{
    Serial.println("Publish failed");
  }
 
}
void mqttconnect() {
  if (!client.connected()) {
    Serial.print("Reconnecting client to ");
    Serial.println(server);
    while (!!!client.connect(clientId, authMethod, token)) {
      Serial.print(".");
      delay(500);
    }
     
     initManagedDevice();
     Serial.println();
  }
}
void wificonnect()
{
  Serial.println();
  Serial.print("Connecting to ");

  WiFi.begin("Wokwi-GUEST", "", 6);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void initManagedDevice() {
  if (client.subscribe(subscribetopic)) {
    Serial.println((subscribetopic));
    Serial.println("subscribe to cmd OK");
  } else {
    Serial.println("subscribe to cmd FAILED");
  }
}

void callback(char* subscribetopic, byte* payload, unsigned int payloadLength)
{
 
  Serial.print("callback invoked for topic: ");
  Serial.println(subscribetopic);
  for (int i = 0; i < payloadLength; i++) {
    Serial.print((char)payload[i]);
    data3 += (char)payload[i];
  }
    Serial.println("data: "+ data3);
 if(data3=="Near")
  {
 Serial.println(data3);
digitalWrite(alarm,HIGH);
 
   }

  else
   {
 Serial.println(data3);
 digitalWrite(alarm,LOW);

  }
data3="";

 
}
