from flask import Flask 
from flask import render_template
from flask import request, redirect

from twilio.rest import TwilioRestClient 

app = Flask(__name__) # Creating the Flask app
client = TwilioRestClient ('ACd009eb10fcf125279953be2d919d68dc', 'db602d472d2a0ed222f3423f4900c895') # Paste in your AccountSID and AuthToken here
twilio_number = "+15104661788" # Replace with your Twilio number

@app.route("/") # When you go to top page of app, this is what it will execute
def main():
    return render_template('form.html')
  
@app.route("/submit-form/", methods = ['POST']) 
def submit_number():
    number = request.form['number']
    formatted_number = "+1" + number # Switch to your country code of choice
    client.messages.create(to=formatted_number, from_ = twilio_number, body = "Thank you, we have received your request for a demo with Apsalar! Please reply to this SMS with the best time and method to connect with you. After replying you can confirm your message was received here http://apsalar.me/appointments/") # Replace body with your message of choice
    return redirect('/')
  
@app.route("/appointments/")
def list_messages():
    messages = client.messages.list(to=twilio_number)
    return render_template('messages.html', messages = messages)
    
    
if __name__ == '__main__': # If we're executing this app from the command line
    app.run("0.0.0.0", port = 3000, debug = True)
