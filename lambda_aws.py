"""
ME 110 Smart Microwave Amazon Alexa Lambda Function Code
"""

from __future__ import print_function
import socket
import time


TCP_IP = '107.170.224.107'
TCP_PORT = 3678
BUFFER_SIZE = 1024

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

gpio_func = {
  'num0' : 24, 
  'num1' : 17, 
  'num2' : 4,  
  'num3' : 11, 
  'num4' : 6,  
  'num5' : 26, 
  'num6' : 10, 
  'num7' : 27, 
  'num8' : 14, 
  'num9' : 8,  
  'sec30orstart' : 16, 
  'reheat' : 19, 
  'kitchentimer' : 13, 
  'clearorstop' : 12, 
  'beverage' : 5, 
  'clock' : 7, 
  'frozen_vegetable' : 25, 
  'power' : 9, 
  'popcorn' : 23, 
  'timecook' : 22, 
  'potato' : 18, 
  'timedefrost' : 15, 
  'pizza' : 3, 
  'weightdefrost' : 2
}

number_dict = {
0 : 'num0',
1 : 'num1',
2 : 'num2',
3 : 'num3',
4 : 'num4',
5 : 'num5',
6 : 'num6',
7 : 'num7',
8 : 'num8',
9 : 'num9'
}

def send_command_to_tunnel(command):
    try:
        print(command)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(command + '|')
        s.close()
        return True
    except Exception as err:
        print(err.message)
        return False

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """Initialize the session attributes here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = " Hello, I'm your smart home kitchen microwave. " \
                    " You can ask me to cook your popcorn, bake a potato, or simply just cook for a specified time."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Tell me to cook for thirty seconds by saying, " \
                    "cook for thirty seconds."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thanks for using your smart home kitchen microwave."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def set_time_intent(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'seconds' in intent['slots'] or 'minutes' in intent['slots']:
        minutes = 0
        seconds = 0
        if 'value' in intent['slots']['minutes']:
            minutes = int(intent['slots']['minutes']['value'])
        if 'value' in intent['slots']['seconds']:
            seconds = int(intent['slots']['seconds']['value'])

        # Check if Inputs are Valid
        if (((seconds / 60) + minutes) > 10):
            speech_output = str(minutes) + " minutes " + str(seconds) + " seconds is too long. Try something shorter"
            reprompt_text = speech_output
        elif (seconds < 0)  or (minutes < 0):
            speech_output = str(minutes) + " minutes " + str(seconds) + " seconds is invalid. Try something else"
            reprompt_text = speech_output
        else:
            # Otherwise turn on microwave for set amount of time
            if send_command_to_tunnel('clear'):
                send_command_to_tunnel('timecook')
                send_command_to_tunnel(number_dict[minutes])
                if seconds == 0:
                    send_command_to_tunnel(number_dict[0])
                    send_command_to_tunnel(number_dict[0])
                else:
                    send_command_to_tunnel(number_dict[seconds / 10])
                    send_command_to_tunnel(number_dict[seconds % 10])
                send_command_to_tunnel('sec30orstart')

                speech_output = "Starting microwave for " + str(minutes) + " minutes " + str(seconds) + " seconds."
                reprompt_text = ""
            else:
                speech_output = "Failed to connect to microwave."
                reprompt_text = "Verify microwave is connected to internet."
    else:
        speech_output = "I'm not sure what you mean. Cook time invalid."
        reprompt_text = "I'm not sure what you mean. Please try again"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Just set cook time
def set_time_intent(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'seconds' in intent['slots'] or 'minutes' in intent['slots']:
        minutes = 0
        seconds = 0
        if 'value' in intent['slots']['minutes']:
            minutes = int(intent['slots']['minutes']['value'])
        if 'value' in intent['slots']['seconds']:
            seconds = int(intent['slots']['seconds']['value'])

        # Check if Inputs are Valid
        if (((seconds / 60) + minutes) > 10):
            speech_output = str(minutes) + " minutes " + str(seconds) + " seconds is too long. Try something shorter"
            reprompt_text = speech_output
        elif (seconds < 0)  or (minutes < 0):
            speech_output = str(minutes) + " minutes " + str(seconds) + " seconds is invalid. Try something else"
            reprompt_text = speech_output
        else:
            # Otherwise turn on microwave for set amount of time
            if send_command_to_tunnel('clear'):
                send_command_to_tunnel('timecook')
                send_command_to_tunnel(number_dict[minutes])
                if seconds == 0:
                    send_command_to_tunnel(number_dict[0])
                    send_command_to_tunnel(number_dict[0])
                else:
                    send_command_to_tunnel(number_dict[seconds / 10])
                    send_command_to_tunnel(number_dict[seconds % 10])
                send_command_to_tunnel('sec30orstart')

                speech_output = "Starting microwave for " + str(minutes) + " minutes " + str(seconds) + " seconds."
                reprompt_text = ""
            else:
                speech_output = "Failed to connect to microwave."
                reprompt_text = "Verify microwave is connected to internet."
    else:
        speech_output = "I'm not sure what you mean. Cook time invalid."
        reprompt_text = "I'm not sure what you mean. Please try again"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Cook Popcorn Intent
def cook_popcorn_intent(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    ounces = 1
    if 'value' in intent['slots']['ounces']:
        ounces = int(intent['slots']['ounces']['value'])

    # Check if Inputs are Valid
    if ( ounces > 4 or ounces < 1):
        speech_output = "Invalid number of ounces."
        reprompt_text = "Select a number between one and four."
    else:
        # Cook Pizza
        if send_command_to_tunnel('clear'):
            send_command_to_tunnel('popcorn')

            if ounces >= 2:
                send_command_to_tunnel('popcorn')
            if ounces > 3:
                send_command_to_tunnel('popcorn')
                send_command_to_tunnel('popcorn')

            send_command_to_tunnel('sec30orstart')

            if ounces == 1:
                speech_output = "Cooking popcorn."
            else:
                speech_output = "Cooking " + str(ounces) + " ounces of popcorn."
            reprompt_text = ""
        else:
            speech_output = "Failed to connect to microwave."
            reprompt_text = "Verify microwave is connected to internet."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Cook Potato
def cook_potato_intent(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    potatoes = 1
    if 'value' in intent['slots']['potatoes']:
        try:
            potatoes = int(intent['slots']['potatoes']['value'])
        except:
            speech_output = "I didn't understand how many potatoes you wanted to cook."
            reprompt_text = ""
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))


    # Check if Inputs are Valid
    if ( potatoes > 3 or potatoes < 1):
        speech_output = "Invalid number of potatoes."
        reprompt_text = "Select a number between one and three."
    else:
        # Cook Pizza
        if send_command_to_tunnel('clearorstop'):
            send_command_to_tunnel('potato')

            if potatoes == 2:
                send_command_to_tunnel('potato')
            if potatoes == 3:
                send_command_to_tunnel('potato')
                send_command_to_tunnel('potato')

            send_command_to_tunnel('sec30orstart')

            if potatoes == 1:
                speech_output = "Cooking potato."
            else:
                speech_output = "Cooking " + str(potatoes) + " potatoes."
            reprompt_text = ""
        else:
            speech_output = "Failed to connect to microwave."
            reprompt_text = "Verify microwave is connected to internet."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Cook Pizza
def cook_pizza_intent(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    slices = 1
    if 'value' in intent['slots']['slices']:
        try:
            slices = int(intent['slots']['slices']['value'])
        except:
            speech_output = "I didn't hear how many slices you wanted to cook."
            reprompt_text = ""
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        

    # Check if Inputs are Valid
    if ( slices > 3 or slices < 1):
        speech_output = "Invalid number of slices."
        reprompt_text = "Select a number between one and three."
    else:
        # Cook Pizza
        if send_command_to_tunnel('clearorstop'):
            send_command_to_tunnel('pizza')

            if slices == 2:
                send_command_to_tunnel('pizza')
            if slices == 3:
                send_command_to_tunnel('pizza')
                send_command_to_tunnel('pizza')

            send_command_to_tunnel('sec30orstart')

            speech_output = "Cooking " + str(slices) + " slices of pizza."
            reprompt_text = ""
        else:
            speech_output = "Failed to connect to microwave."
            reprompt_text = "Verify microwave is connected to internet."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Cook Pizza
def stop_microwave_intent(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    # Cook Pizza
    if send_command_to_tunnel('clearorstop'):
        speech_output = "Microwave stopped."
        reprompt_text = ""
    else:
        speech_output = "Failed to connect to microwave."
        reprompt_text = "Verify microwave is connected to internet."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SetTimeIntent":
        return set_time_intent(intent, session)
    elif intent_name == "CookPopcornIntent":
        return cook_popcorn_intent(intent, session)
    elif intent_name == "CookPotatoIntent":
        return cook_potato_intent(intent, session)
    elif intent_name == "CookPizzaIntent":
        return cook_pizza_intent(intent, session)
    elif intent_name == "StopMicrowaveIntent":
        return stop_microwave_intent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
