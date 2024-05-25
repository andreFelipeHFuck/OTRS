#include "Mqtt.h"

WiFiClient espClient;
PubSubClient client(espClient);

bool mqttState = false;

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
    mqttState = true;
}

Mqtt::Mqtt(
            //LedRGB led,

            const char* wifi_ssid,
            const char* wifi_password,

            const char* mqtt_host,
            uint16_t port,
            const char* username,
            const char* password,
            const char* sub_topic_pic,
            const char* pub_topic_pic
):
//led(led),
wifi_ssid(wifi_ssid),
wifi_password(wifi_password),
mqtt_host(mqtt_host),
port(port),
username(username),
password(password),
sub_topic_pic(sub_topic_pic),
pub_topic_pic(pub_topic_pic){
}

void Mqtt::setup(void){
    setup_wifi(wifi_ssid, wifi_password);
    setup_mqtt();

    /*if(client.connect("esp32cam", username, password)){
        client.publish("imagem","hello world");
    }*/

    
}

void Mqtt::pub_topic(const uint8_t* pic_buf, size_t length){
    pub_topic_encode64(pic_buf, length);
}

void Mqtt::pub_topic_write(const uint8_t* pic_buf, size_t length){
    Serial.println("Send mensage");
    Serial.println("Leng: " + String(length) + "bytes");

    if(client.beginPublish(pub_topic_pic, length, false)){

        //led.rgbColor(BLUE);

        for(int i=0; i < length; i++){
            client.write(pic_buf[i]);
        }

        //led.rgbColor(OFF);
        
        if(!client.endPublish()){
            DBG("Sending Failed!");
            //led.rgbColor(RED);
        }else{
            DBG("MQTT Publish succesful");
            //led.rgbColor(GREEN);
        }

        //led.rgbColor(OFF);

    }else{
        DBG("Sending Failed!");
    }

    mqttState = false;
}

void Mqtt::pub_topic_P(const uint8_t* pic_buf, size_t length){
    Serial.println("Send mensage");
    Serial.println("Leng: " + String(length) + "bytes");

    if(!client.publish_P(pub_topic_pic, (const byte *) pic_buf, length, 0 )){
        DBG("Sending Failed!");
        //led.rgbColor(RED);
    }else{
        DBG("MQTT Publish succesful");
        DBG("buffer is " + String(length) + " bytes");
        //led.rgbColor(GREEN);
    }

    //led.rgbColor(OFF);

    mqttState = false;
}

void Mqtt::pub_topic_encode64(const uint8_t* pic_buf, size_t length){
    String encoded = base64::encode(pic_buf, length);

    Serial.println("Send mensage");
    Serial.println("Leng: " + String(length) + "bytes");

    if(!client.publish_P(pub_topic_pic, encoded.c_str(), 0)){
        DBG("Sending Failed!");
        //led.rgbColor(RED);
    }else{
        DBG("MQTT Publish succesful");
        DBG("buffer is " + String(length) + " bytes");
        //led.rgbColor(GREEN);
    }

    //led.rgbColor(OFF);

    mqttState = false;
}


void Mqtt::reconnect(){
    while(!client.connected()) {
        Serial.print("Attempting MQTT connection...");

        String clientId = "ESP32";
        clientId += String(random(0xffff), HEX);

        if(client.connect(clientId.c_str())) {
            //led.rgbColor(GREEN);

            Serial.println("connected");

            client.subscribe(sub_topic_pic);

            delay(1000);
            //led.rgbColor(OFF);
        }else{
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");

            //led.rgbColor(YELLOW);
            delay(5000);
            //led.rgbColor(OFF);
        }
    }
}

void Mqtt::teste_topic(void){
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
}

bool Mqtt::getState(){
    return mqttState;
}


void Mqtt::deep_sleep(void){
    DBG("Going to sleep after: " + String( millis()) + "ms");
    Serial.flush();

    esp_deep_sleep_start();
}

void Mqtt::setup_mqtt(void){
    client.setServer(mqtt_host, port);
    client.setBufferSize(1000000);
    client.setCallback(callback);
}

void Mqtt::setup_wifi( const char* wifi_ssid, const char* wifi_password){
    delay(10);

    Serial.println();
    Serial.print("Connecting to");
    Serial.println(wifi_ssid);

    WiFi.mode(WIFI_STA);
    WiFi.begin(wifi_ssid, wifi_password);

    while (WiFi.status() != WL_CONNECTED){
        //led.rgbColor(RED);
        delay(500);
        Serial.print(".");
        //led.rgbColor(OFF);
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIPv6());
}

