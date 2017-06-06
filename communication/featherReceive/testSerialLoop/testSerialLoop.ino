int n = 0;
int data[] = {5, 15, 20, 34, 17, 82, 79, 43, 50, 20};
void setup() 
{
  while (!Serial);
  Serial.begin(9600);
  delay(100);
  
 
  Serial.println("Arduino LoRa RX Test!");
}
 
void loop()
{  
   for(int i =0; i < 10; i++){
    Serial.print(data[i]);
    Serial.print(",");
    if(i%2 == 0){
      data[i] += 1;
    }
    else {
      data[i] -= 1;
    }
   }
   Serial.print('\n');
   //Serial.println(n);
   //n++;
   delay(100);
}
/*

   */
