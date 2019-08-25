# Serverless-Lex-Bot-API-on-Cloud-Formation

## AIM OF PROJECT:
To span out an User Interface to make the fast interaction between the user and the json data file containing the large set of amazon IPs’. This aims to mitigate the users’ time taken to search through a database and verify if a supplied IP is based on the data set and send a valid user understandable response.
https://ip-ranges.amazonaws.com/ip-ranges.json

## WORK FLOW:
The process includes traversing through a variety of amazon services to achieve a serverless architecture through coding in Lambda, API Gateway, Amazon Lex and CloudFormation. A back integration of the model mentioned below has been applied to be traced back to the requirements of the project.

<p align="center">
<img src="/images/AWS.jpg" "Architecture">
</p>

* Lambda function to call on the json file http link and perform verification and then return true or false depending on the value specified.
* Link the Lambda to an API Gateway which performs a GET request on the Lambda for API and the gets back the Boolean value for confirmation. The API does not have proxy integration and so needs a template to send values through the API URL
https://guqdku9qt0.execute-api.us-east-1.amazonaws.com/api_get/api-ip?ip=3.3.3.3 and then add the input parameters according to the template placed at the end of the API GET link as shown for testing.
* Make a Lex Lambda to call on the API Gateway through GET function and then get the output from the validation of API Lambda.
* LEX bot to make a user interface to access the Lex Lambda function. However, this changes the format of the code to fit the format of the Lex input/output json formats and control all use cases.
* Piece all these together and then introduce a CloudFormation on the Lex Bot.

## Targets Reached: Time Limitations
* Lambda_API: Perfect Run
* Lambda_Lex_Validation_&_Fulfillment: Cons,
  * Fails to run without a starting prompt (Does amazon own)
  * Fails to pass user credentials for login
  * Syntax and prompts not ideal
  * Could not extract slot value from invocation
* Lambda_Lex_Validation_&_Fulfillment: Pros,
  * Able to accept free text input from user and turns into slot values
  * Is able to avoid error handling Lex fails
  * Will solve for all types of IP inputs
  * Will extract IP from a line and then serve the purpose
* CloudFormation:
  * Perfectly working but not integrating active user and identity pool

## CHALLENGES & SOLUTIONS:
* Challenge Faced: Understanding which service to start with and understand the process of thinking as a developer
* Solution: Traceback the services so that I can test the finished services
* Challenge Faced: Understand Lambda Code in Python (First experience)
* Solution: Understanding the test end and event parameters. Understanding the response variables and the json format to pass during triggers. The types of json field values like type, intent, etc.
* Challenge Faced: Using the API gateway in the reverse way using GET method to invoke it from a lambda function
* Solution: Changing the script to fit my needs and a complete understanding of the lambda code to the thin details.
  * Use of response.get instead of os.environ.get which inspite of many tries yielded no results.
  * Passing arguments during GET API call of API gateway from endpoint
  * Receiving data from the call, in appropriate format and then using string manipulation to extract the Boolean value from the dict[]
  * How to check API logs and function logs to see errors and fix them
  * Integrated API without Lambda Proxy Integration and then set mapping templates to accept the variables in GET method
* Challenge Faced: Lex Integration with Lambda
  * Lex integration with a variable slot value was the biggest challenge since the Amazon.Literal
* Solution: I had to understand the complete workflow of Lex and how the format of the json files work in alignment with Lex.
  * Accepting the Intent when passed from the Lex Bot
  * How the flow of event work in Lex: invocationSource, inputTranscript, currentIntent, slots, messages, ElicitSlot
  * How message is passed from Lambda to Lex and in what format
  * Understanding which part of the code Validates and the part which helps in Fulfillement
  * Validation try catch block knowledge and understanding how it gets accessed for which part of the bot commands
  * Fulfillment block understanding of how the ip is verified from the slots predefined and then passing the result as Boolean to make a
  decision message
  * This flow worked however was inefficient as it required the user to pass all the IP values in slots
  * Editing the lambda function to accept free texts and then extract the IP from the string and search the query without Lambda
  Unhandled Error.
  * Understanding that after fulfillment slots cannot be passed back as response back to Lex
* Challenge Faced: CloudFormation creation:
* Solution: The permission problem was solved when I created the cognito bucket separately and let AWS create its own role.

## Scope Of Project:
Updating the bot to meet the bonus requirements. Making sure the syntax and the UI messages are on point.

OUTPUT:

Working example1
<p align="center">
<img src="/images/AWS1.jpg" "Working example1">
</p>

Working example2
<p align="center">
<img src="/images/AWS2.jpg" "Working example2">
</p>

Error ecxamples
<p align="center">
<img src="/images/AWS3.jpg" "Error examples">
</p>

## LINKS:
S3 Static Website: https://lex-web-ui-codebuilddeploy-1lt0x69va-webappbucket-u2vfrytwwp5r.s3.amazonaws.com/index.html
URL WEB APP- http://lex-web-ui-codebuilddeploy-1lt0x69va-webappbucket-u2vfrytwwp5r.s3-website-us-east-1.amazonaws.com
API Gateway: https://guqdku9qt0.execute-api.us-east-1.amazonaws.com/api_get/api-ip
