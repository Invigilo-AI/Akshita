### This documentation is for whatsapp bot to download images locally from whatsapp

#### Steps to run
1)Make an account on Twilio, which provides an api for whatsapp.<br>
2)Configure the twilio whatsapp sandbox. Follow this link <a href="https://www.twilio.com/console/sms/whatsapp/learn">Twilio sandbox</a><br>
3)Run the script file bot.py after installing the dependencies
```
python3 bot.py
```
4)Flask application will start running.<br>
5)Download ngrok.exe,executable file.<br>
6)In a new window run this command where ngrok.exe is saved.
```
This command is connecting your local port 5000 with a temporary external URL.
./ngrok http 5000
```
7)Copy the https:// address from “Forwarding”. The address looks like this: 'https://dea8-2405-201-4011-1136-6997-15bb-ac03-1e9e.in.ngrok.io' <br>
8)Go to Twilio’s console > Programmable SMS > WhatsApp and in the field “When a message comes in” <br>
add this URL followed by your endpoint resource (“/reply”).<br>
9)Save the changes.<br>
10)Now send a picture to the bot on whatsapp.The image will be saved in the local directory.
