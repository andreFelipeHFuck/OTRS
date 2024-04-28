#include "MqttPub.h"

WiFiClient espClient;
PubSubClient client(espClient);


void callback(char* topic, byte* payload, unsigned int length){
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("]");

    for(int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
    }

    if ((char)payload[0] == '1') {
        //digitalWrite(BUILTIN_LED, LOW); 
    } else {
        //digitalWrite(BUILTIN_LED, HIGH);  
    }

    Serial.println();
}

MqttPub::MqttPub(
            const char* wifi_ssid,
            const char* wifi_password,

            const char* mqtt_host,
            uint16_t port,
            const char* username,
            const char* password,
            const char* topic_pic
):
wifi_ssid(wifi_ssid),
wifi_password(wifi_password),
mqtt_host(mqtt_host),
port(port),
topic_pic(topic_pic){
}

void MqttPub::setup(void){
    setup_wifi(wifi_ssid, wifi_password);
    setup_mqtt();
}

void MqttPub::pub_topic(const uint8_t* pic_buf, size_t length){

    if(!client.publish(topic_pic, (const char*) pic_buf, length)){
        DBG("Sending Failed!");
    }else{
        DBG("MQTT Publish succesful");
        DBG("buffer is " + String(length) + " bytes");
    }

    deep_sleep();
}

void MqttPub::pub_topic(const char* msg){
    client.publish(topic_pic, msg);
}

void MqttPub::reconnect(){
    while(!client.connected()) {
        Serial.print("Attempting MQTT connection...");

        String clientId = "ESP32";
        clientId += String(random(0xffff), HEX);

        if(client.connect(clientId.c_str())) {
            Serial.println("connected");

            client.publish("test_topic", "reconnect");

            client.subscribe("inTopic");
        }else{
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");

            //digitalWrite(BUILTIN_LED, HIGH); 
            delay(5000);
            //digitalWrite(BUILTIN_LED, LOW); 
        }
    }
}

void MqttPub::teste_topic(void){
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
}

void MqttPub::deep_sleep(void){
    DBG("Going to sleep after: " + String( millis()) + "ms");
    Serial.flush();

    esp_deep_sleep_start();
}

void MqttPub::setup_mqtt(void){
    client.setServer(mqtt_host, port);
    client.setCallback(callback);
}

void MqttPub::setup_wifi( const char* wifi_ssid, const char* wifi_password){
    delay(10);

    Serial.println();
    Serial.print("Connecting to");
    Serial.println(wifi_ssid);

    WiFi.mode(WIFI_STA);
    WiFi.begin(wifi_ssid, wifi_password);

    while (WiFi.status() != WL_CONNECTED){
        //digitalWrite(BUILTIN_LED, HIGH); 
        delay(500);
        Serial.print(".");
        //digitalWrite(BUILTIN_LED, LOW); 
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIPv6());
}

