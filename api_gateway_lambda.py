import ipaddress
import json
from botocore.vendored import requests

json_url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'

# Retrieves the JSON file from the public location. 
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
    
    # Fill in this object (python dictionary) with the appropriate key and value pairs to return to the Lex service. It may require more than two key value pairs.
    return {
        "type": "Close",
        "message": json.dumps(response_body) # Do not replace this value; it needs to be in the response like this, but you'dd need to find the right key it belongs to.
    }