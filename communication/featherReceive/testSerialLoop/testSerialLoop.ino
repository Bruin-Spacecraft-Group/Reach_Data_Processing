int n = 0;

void setup() 
{
  while (!Serial);
  Serial.begin(9600);
  delay(100);
  
 
  Serial.println("Arduino LoRa RX Test!");
}
 
void loop()
{
   Serial.println(n);
   n++;
   delay(100);
}

