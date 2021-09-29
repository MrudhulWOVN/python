from __future__ import print_function
from botocore.vendored import requests
from boto3 import session, client
from logging import getLogger, INFO
from datetime import datetime
import json
#import os
import boto3
logger = getLogger()
logger.setLevel(INFO)

def lambda_handler(event, context):
    if "detail-type" not in event:
        raise ValueError("ERROR: event object is not a valid CloudWatch Logs event")
    else:
        if event["detail-type"] == "ECS Task State Change":
            detail = event["detail"]
            print(detail)
            if detail["lastStatus"] == "STOPPED":
                Message=json.dumps(detail)
                messagedata = json.loads(Message)

                stoppedReason = messagedata['stoppedReason']
                exitCode = messagedata['containers'][0]['exitCode']
                
                print(Message)
                print(messagedata)
                print(stoppedReason)
                print(exitCode)

                if stoppedReason == "Task stopped by user" \
                        and exitCode != 0 :

                    # Send an error status message.
                    serviceName = messagedata['containers'][0]['name']
                    #env = os.environ['aws.ecs']
                    #region = os.environ['us-west-2']
                    env = 'aws.ecs'
                    region = 'us-west-2'


                    taskArn = messagedata['taskArn']
                    clusterArn = messagedata['clusterArn']
                    taskDefinitionArn = messagedata['taskDefinitionArn']
                    lastStatus = messagedata['lastStatus']
                    stoppedAt = messagedata['stoppedAt']
                    #desiredStatus = messagedata['desiredStatus']
                    
                    #print(taskArn)
                    #print(clusterArn)

                    payload = {
                        #'channel': os.environ['slackChannel'],
                        'channel': 'My_Slack_channal_name',
                        
                        'attachments': [
                            {
                                'title': 'ECS Task failure detected for container',
                                'fields': [
                            {
                                'title': 'Service',
                                'value': serviceName
                            },
                            {
                                'title': 'Stopped Reason',
                                'value': stoppedReason,
                                'short': 'true'
                            },
                            {
                                'title': 'Exit Code',
                                'value': exitCode,
                                'short': 'true'
                            },
                            {
                                'title': 'Region',
                                'value': region,
                                'short': 'true'
                            },
                            {
                                'title': 'Stopped At',
                                'value': stoppedAt
                            },
                            {
                                'title': 'Task ARN',
                                'value': taskArn
                            },
                            {
                                'title': 'Task DefinitionArn',
                                'value': taskDefinitionArn
                            },
                            {   
                                'title': 'Last Status',
                                'value': lastStatus
                            },
                            {
                                'title': 'Cluster ARN',
                                'value': clusterArn
                            }
                            ],
                            'color': '#F35A00'
                            }
                        ]
                    }
                    url = 'https://hooks.slack.com/services/xxxxxxxxxxx' # Set destination URL here
                    #print(url)
                    
                    headers = {"content-type": "application/json" }
                    response = requests.put(url, data=json.dumps(payload), headers=headers)

                    # print(json.dumps(messagedata))
                    print(response.status_code)
                    print(response.content)
                    
