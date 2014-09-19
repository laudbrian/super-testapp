import os
from flask import Flask
from flask import render_template
from flask import request, redirect, send_from_directory

from twilio.rest import TwilioRestClient 

# initialization
app = Flask(__name__)
client = TwilioRestClient ('ACd009eb10fcf125279953be2d919d68dc', 'db602d472d2a0ed222f3423f4900c895') # Paste in your AccountSID and AuthToken here
twilio_number = "+18184854646" # Replace with your Twilio number
app.config.update(
    DEBUG = True,
)

# controllers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('form.html')

@app.route("/submit-form/", methods = ['POST']) 
def submit_number():
    number = request.form['number']
    formatted_number = "+1" + number # Switch to your country code of choice
    client.messages.create(to=formatted_number, from_ = twilio_number, body = "Thank you, we have received your request for a demo with! Please reply to this SMS with the best time and method to connect with you. After replying you can confirm your message was received here http://apsalar.me/appointments/") # Replace body with your message of choice
    return redirect('/')
  
@app.route("/appointments/")
def list_messages():
    messages = client.messages.list(to=twilio_number)
    return render_template('messages.html', messages = messages)

# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
