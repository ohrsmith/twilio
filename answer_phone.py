from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)


@app.route("/answer", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Start our <Gather> verb
    gather = Gather(num_digits=1, action='/gather')
    gather.say('Hello and welcome to St Mellons Baptist Church. '
               'To speak to an elder, press 1. '
               'To speak to the treasurer, press 2. '
               'Or to speak to someone concerning the chapel building, press 3.')

    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/answer')

    return str(resp)


@app.route('/gather', methods=['GET', 'POST'])
def gather():
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            resp.dial('+447790011472')
            resp.hangup()
            return str(resp)
        elif choice == '2':
            resp.dial('+447989745456')
            resp.hangup()
            return str(resp)
        elif choice == '3':
            resp.dial('+447989745456')
            resp.hangup()
            return str(resp)
        #elif choice == '4':
            #resp.say('There may be a short delay of up to 30 seconds before the recording starts.')
            #resp.play('https://docs.google.com/uc?expoer=download&id=1DmH-OXgA7mwowL9fR2FhPaVcaH7VYdG4')
            #resp.hangup()
            #return str(resp)
        else:
            # If the caller didn't choose 1, 2, 3, or 4, apologize and ask them again
            resp.say("Sorry, I don't understand that choice.")

    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    resp.redirect('/answer')

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
