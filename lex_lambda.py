"""
Lambda Function for validating user input and fulfilling intents for AwsIp 
"""
import ipaddress
import json
import os

import re

from botocore.vendored import requests

API_ENDPOINT='https://guqdku9qt0.execute-api.us-east-1.amazonaws.com/api_get/api-ip'

invalid_ip_message = {
    "contentType": "PlainText",
    "content": "It doesn't seem like that's a valid IP v4 "
               "address. What IP v4 address do you want me to "
               "check, again? "
}


def dialog_handler(event):
    """
    Handles the validation of user input for the Lex Bot.
    Parameter and Return Reference:
    https://docs.aws.amazon.com/lex/latest/dg/lambda-input-response-format.html
    Parameters
    ----------
    event: dict Event object from Lex

    Returns
    -------
    session_attributes, dialog_action: tuple[dict, dict] session attributes and dialog
    action that Lex is expecting.
    """
    session_attributes = event.get('sessionAttributes')
    slots = event.get('currentIntent').get('slots')
    
    
    if event['currentIntent']['slots']['ip'] is None:
        dialog_action = {
            "type": "ElicitSlot",
            "slots": slots,
            "message":
                {
                    'contentType': 'PlainText', 
                    'content': "Enter an IP address to search"
                },
            "intentName": event['currentIntent']['name'],
            "slotToElicit": "ip"
            }
    
    try:
        userInput=event["inputTranscript"]
        ip=re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', userInput)
        if not ip is None:
                ip=ip.group()
        ipaddress.ip_address(ip)
        slots['ip']=ip
        dialog_action = {
            "type": "Delegate",
            "slots": slots,
        }
    except ValueError:
        # Fill in this object with the appropriate key and value pairs to return to the Lex service.
        if userInput=="Does amazon own":
            message="Type IP"
        else:
            message="Wrong IP"
        dialog_action = {
            "type": "ElicitSlot",
            "slots": slots,
            "message":
                {
                    'contentType': 'PlainText', 
                    'content': message
                },
            "intentName": event['currentIntent']['name'],
            
            "slotToElicit": "ip"
        }

    return session_attributes, dialog_action


def fulfillment_handler(event):
    """
    Handles the fulfillment actions for the Lex Bot.
    Parameter and Return Reference:
    https://docs.aws.amazon.com/lex/latest/dg/lambda-input-response-format.html
    Parameters
    ----------
    event: dict Event object from Lex

    Returns
    -------
    session_attributes, dialog_action: tuple[dict, dict] session attributes and dialog
    action that Lex is expecting.
    """
    
    session_attributes = event.get('sessionAttributes')
    slots = event.get('currentIntent').get('slots')
    
    userInput=event["inputTranscript"]
    ip=re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', userInput)
    if not ip is None:
            ip=ip.group()
    slots['ip']=ip
    
    print ("ip ",ip)
    #payload = { "queryStringParameters":{"ip": ip }}
    ip_ownership_response = requests.get('https://guqdku9qt0.execute-api.us-east-1.amazonaws.com/api_get/api-ip', params={'ip':ip})

    print("RESPONSE HTTP ",ip_ownership_response)

    print("MYANSWER",ip_ownership_response.content)
    
    data1=ip_ownership_response.json()

    print("Type of data",type(data1))
    
    
    is_amazon_owned=data1["message"][16:-1]
    print("State of Validation", data1["message"][16:-1])
    
    if is_amazon_owned=="true":
        message = f"Amazon owns {slots.get('ip')}"
    else:
        message = f"Amazon does not own {slots.get('ip')}"
    
    # Fill in this object (python dictionary) with the appropriate key and value pairs to return to the Lex service. It may require more than two key value pairs.
    dialog_action = {
        "type": "Close",
        "fulfillmentState":"Fulfilled",
        "message":
                {
                    'contentType': 'PlainText', 
                    'content': message
                }
    }

    return session_attributes, dialog_action


def handler(event, context):
    """
    Validates and fulfills for AwsIpInfoBot
    Parameter and Return Reference:
    https://docs.aws.amazon.com/lex/latest/dg/lambda-input-response-format.html
    Context reference:
    https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    Parameters
    ----------
    event: dict Event object from Lex
    context: dict Context object
    
    Returns
    -------
    response: dict Full response to Lex service in the expected format.
    """

        
    invoke_source = event['invocationSource']

    if not event['currentIntent']['name']=='IPcheck':
       raise ValueError

    if invoke_source == 'DialogCodeHook':
        session_attributes, dialog_action = dialog_handler(event)

    elif invoke_source == 'FulfillmentCodeHook':
        session_attributes, dialog_action = fulfillment_handler(event)
    else:
        raise ValueError('Unknown invocationSource.')
    
    print(dialog_action["type"])
    
    # Fill in this object (python dictionary) with the appropriate key and value pairs to return to the Lex service. It may require more than two key value pairs.
    response = {
        "sessionAttributes":session_attributes,
        "dialogAction": dialog_action
    }
    return response