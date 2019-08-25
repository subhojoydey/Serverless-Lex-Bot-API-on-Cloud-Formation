# Serverless-Lex-Bot-API-on-Cloud-Formation

## AIM OF PROJECT:
To span out an User Interface to make the fast interaction between the user and the json data file containing the large set of amazon IPs’. This aims to mitigate the users’ time taken to search through a database and verify if a supplied IP is based on the data set and send a valid user understandable response.
https://ip-ranges.amazonaws.com/ip-ranges.json

## WORK FLOW:
The process includes traversing through a variety of amazon services to achieve a serverless architecture through coding in Lambda, API Gateway, Amazon Lex and CloudFormation. A back integration of the model mentioned below has been applied to be traced back to the requirements of the project.

<p align="center">
<img src="/images/AWS.jpg" "Architecture">
</p>

• Lambda function to call on the json file http link and perform verification and then return true or false depending on the value specified.
• Link the Lambda to an API Gateway which performs a GET request on the Lambda for API and the gets back the Boolean value for confirmation. The API does not have proxy integration and so needs a template to send values through the API URL
https://guqdku9qt0.execute-api.us-east-1.amazonaws.com/api_get/api-ip?ip=3.3.3.3 and then add the input parameters according to the template placed at the end of the API GET link as shown for testing.
• Make a Lex Lambda to call on the API Gateway through GET function and then get the output from the validation of API Lambda.
• LEX bot to make a user interface to access the Lex Lambda function. However, this changes the format of the code to fit the format of the Lex input/output json formats and control all use cases.
• Piece all these together and then introduce a CloudFormation on the Lex Bot.

## Targets Reached: Time Limitations
• Lambda_API: Perfect Run
• Lambda_Lex_Validation_&_Fulfillment: Cons,
  o Fails to run without a starting prompt (Does amazon own)
  o Fails to pass user credentials for login
  o Syntax and prompts not ideal
  o Could not extract slot value from invocation
• Lambda_Lex_Validation_&_Fulfillment: Pros,
  o Able to accept free text input from user and turns into slot values
  o Is able to avoid error handling Lex fails
  o Will solve for all types of IP inputs
  o Will extract IP from a line and then serve the purpose
• CloudFormation:
  o Perfectly working but not integrating active user and identity pool

## CHALLENGES & SOLUTIONS:
• Challenge Faced: Understanding which service to start with and understand the process of thinking as a developer
o Solution: Traceback the services so that I can test the finished services
• Challenge Faced: Understand Lambda Code in Python (First experience)
o Solution: Understanding the test end and event parameters. Understanding the response variables and the json format to pass during triggers. The types of json field values like type, intent, etc.
• Challenge Faced: Using the API gateway in the reverse way using GET method to invoke it from a lambda function
o Solution: Changing the script to fit my needs and a complete understanding of the lambda code to the thin details.
  ▪ Use of response.get instead of os.environ.get which inspite of many tries yielded no results.
  ▪ Passing arguments during GET API call of API gateway from endpoint
  ▪ Receiving data from the call, in appropriate format and then using string manipulation to extract the Boolean value from the dict[]
  ▪ How to check API logs and function logs to see errors and fix them
  ▪ Integrated API without Lambda Proxy Integration and then set mapping templates to accept the variables in GET method
• Challenge Faced: Lex Integration with Lambda
  ▪ Lex integration with a variable slot value was the biggest challenge since the Amazon.Literal
o Solution: I had to understand the complete workflow of Lex and how the format of the json files work in alignment with Lex.
  ▪ Accepting the Intent when passed from the Lex Bot
  ▪ How the flow of event work in Lex: invocationSource, inputTranscript, currentIntent, slots, messages, ElicitSlot
  ▪ How message is passed from Lambda to Lex and in what format
  ▪ Understanding which part of the code Validates and the part which helps in Fulfillement
  ▪ Validation try catch block knowledge and understanding how it gets accessed for which part of the bot commands
  ▪ Fulfillment block understanding of how the ip is verified from the slots predefined and then passing the result as Boolean to make a
  decision message
  ▪ This flow worked however was inefficient as it required the user to pass all the IP values in slots
  ▪ Editing the lambda function to accept free texts and then extract the IP from the string and search the query without Lambda
  Unhandled Error.
  ▪ Understanding that after fulfillment slots cannot be passed back as response back to Lex
• Challenge Faced: CloudFormation creation:
o Solution: The permission problem was solved when I created the cognito bucket separately and let AWS create its own role.

## Scope Of Project:
Updating the bot to meet the bonus requirements. Making sure the syntax and the UI messages are on point.
OUTPUT:
<p align="center">
<img src="/images/AWS1.jpg" "Working example1">
</p>

<p align="center">
<img src="/images/AWS2.jpg" "Working example2">
</p>

<p align="center">
<img src="/images/AWS3.jpg" "Error examples">
</p>

## CODES:

### LAMBDA LEX VALIDATION:
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
#Fill in this object with the appropriate key and value pairs to return to the Lex service.
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
#Fill in this object (python dictionary) with the appropriate key and value pairs to return to the Lex service. It may require more than two key value pairs.
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
#Fill in this object (python dictionary) with the appropriate key and value pairs to return to the Lex service. It may require more than two key value pairs.
response = {
"sessionAttributes":session_attributes,
"dialogAction": dialog_action
}
return response

### LAMBDA API:
import ipaddress
import json
from botocore.vendored import requests
json_url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
#Retrieves the JSON file from the public location.
get_json_response = requests.get(json_url)
prefix_list = get_json_response.json()['prefixes']
def get_all_prefixes():
"""
Gathers all the prefixes (e.g. 0.0.0.0/32) from the JSON file in to a set.
Returns
-------
prefixes: set
"""
prefixes = set()
for prefix in prefix_list:
prefixes.add(prefix['ip_prefix'])
return prefixes
def is_aws_ip(ip):
"""
Checks each prefix in a set of all AWS prefixes to see if the IP address
is included in the prefix. If so, returns True, otherwise returns False
Parameters
----------
ip: ipaddress.IPv4Address The IP address to check.
Returns
-------
aws_ip: boolean
"""
print("aaaaaa")
if not isinstance(ip, ipaddress.IPv4Address) or not isinstance(ip, ipaddress.IPv6Address):
ip = ipaddress.ip_address(ip)
print("aaaaa")
print("ip value: ",ip)
aws_ip = False
prefixes = get_all_prefixes()
for prefix in prefixes:
prefix = ipaddress.ip_network(prefix)
if prefix.__contains__(ip):
aws_ip = True
return aws_ip
def handler(event, context):
"""
Checks an Amazon IP Address against the public JSON file at
https://ip-ranges.amazonaws.com/ip-ranges.json
"""
user_ip = event['queryStringParameters']['ip']
print("the ip is ",user_ip)
response_body = {
"amazonOwned": is_aws_ip(user_ip),
}
#Fill in this object (python dictionary) with the appropriate key and value pairs to return to the Lex service. It may require more than two key value pairs.
return {
"type": "Close",
"message": json.dumps(response_body) # Do not replace this value; it needs to be in the response like this, but you'dd need to find the right key it belongs to.
}
LINKS:
S3 Static Website: https://lex-web-ui-codebuilddeploy-1lt0x69va-webappbucket-u2vfrytwwp5r.s3.amazonaws.com/index.html
URL WEB APP- http://lex-web-ui-codebuilddeploy-1lt0x69va-webappbucket-u2vfrytwwp5r.s3-website-us-east-1.amazonaws.com
API Gateway: https://guqdku9qt0.execute-api.us-east-1.amazonaws.com/api_get/api-ip
