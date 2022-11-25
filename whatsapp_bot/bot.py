from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pprint import pprint
import requests

app = Flask(__name__)

@app.route('/reply', methods=['POST'])
def reply():
    c=0
    num_media = int(request.values['NumMedia'])
    media = request.values.get('MediaContentType0', '')
    user_phone_number = request.values['From']

    if user_phone_number.startswith('whatsapp'):
        # from format: 'whatsapp:+490001112223'
        user_phone_number = user_phone_number.split(':')[1]
    pprint(request.values)
    resp = MessagingResponse()
    reply = f"I didn't get it 😕"  # default message

    if num_media > 0:
        c+=1
        if media.startswith('image/'):
            file_url = request.values['MediaUrl0']
            extension = media.split('/')[1]
            print(file_url)
            r = requests.get(file_url, allow_redirects=True).content
            
            with open(f"img{c}.jpg","wb+") as f:
                      f.write(r)
            #save_on_dropbox(user_phone_number, file_url, extension)
            reply = 'Your pic is safe and sound!'
        else:
            reply = 'Sorry, only pictures are allowed.'
    else:
        user_message = request.values['Body'].lower()
        if 'save' in user_message:
            reply = (
                f"Let's get started! From now on, I'll save the pics you send to me.\n"
                "To see your pics, just send me a message with the word *see*."
                )
        elif 'see' in user_message:
            # all_pics_url = dropbox_folder_from(user_phone_number)
            # reply = f'Here you go: {all_pics_url}'
            print("see")
    resp.message(reply)
    
    return str(resp)



if __name__=="__main__":
    app.run()
