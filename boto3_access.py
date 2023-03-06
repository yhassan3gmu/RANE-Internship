import csv
import json
import boto3
import configparser
from datetime import datetime, timedelta
import time

'''
This file grabs CloudWatch data by using the information in a config.ini file to access the data.
'''

class CloudWatchLogs:
    def __init__(self, full_path_to_file=None):
        try:
            self.config = configparser.ConfigParser()
            self.config.read(full_path_to_file)
            #print(self.config)
            boto3.setup_default_session(region_name=self.config['AWS_CONFIG']['region_name'])
            self.client = boto3.client('logs', 
                                       aws_access_key_id=self.config['AWS_CONFIG']['aws_access_key_id'], 
                                       aws_secret_access_key=self.config['AWS_CONFIG']['aws_secret_access_key'])
        except Exception as e:
            print('failed to open file')
            self.config = None
            self.client = None


    def filter_worldview_logs(self, startTime, endTime):
        '''
        filters logs by worldview
        :return: filtered logs
        '''

        if self.client is None:
            return None
        else:
            #access_logs = []
            kwargs = {
                'logGroupName' : self.config['AWS_CONFIG']['log_group'],
                'limit': 10000,
                'filterPattern': '{ $.msg = "access-log"}'
            }

            if startTime is not None:
                kwargs['startTime'] = startTime
            if endTime is not None:
                kwargs['endTime'] = endTime
            access_logs = []
            while True:
                resp = self.client.filter_log_events(**kwargs)
                yield from resp['events']
                try:
                    kwargs['nextToken'] = resp['nextToken']
                except KeyError:
                    break

    def log_list(self, starttime, endtime):

        if self.client is None:
            return None
        else:
            access_logs = []
            log_events = self.filter_worldview_logs(starttime, endtime)
            for event in log_events:
                access_logs.append(event)
            return access_logs


result = CloudWatchLogs('config.ini')


log_event = result.log_list(
    starttime = int((datetime.today() - timedelta(days = 7)).timestamp() * 1000),
    endtime = int(datetime.now().timestamp() * 1000)
)
for event in log_event:
    print(event)

#print(access_logs)



#https://docs.python.org/3/library/configparser.html
#https://stackoverflow.com/questions/59240107/how-to-query-cloudwatch-logs-using-boto3-in-python
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.filter_log_events
