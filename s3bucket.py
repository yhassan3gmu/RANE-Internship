import boto3
import json
import configparser
from datetime import datetime, timedelta

class Bucket:
    def __init__(self, full_path_to_file=None):
        '''
        accesses config.ini which contains the region name, AWS access key ID, and the AWS Secret Access Key ID under the AWS_CONFIG category.
        I used the config.ini because I can't share this information with anyone due to work.
        '''
        try:
            self.config = configparser.ConfigParser()
            self.config.read(full_path_to_file)
            #print(self.config)
            boto3.setup_default_session(region_name=self.config['AWS_CONFIG']['region_name'])
            self.client = boto3.client('s3',
                                       aws_access_key_id=self.config['AWS_CONFIG']['aws_access_key_id'],
                                       aws_secret_access_key=self.config['AWS_CONFIG']['aws_secret_access_key'])
            self.resource = boto3.resource('s3',
                                           aws_access_key_id=self.config['AWS_CONFIG']['aws_access_key_id'],
                                           aws_secret_access_key=self.config['AWS_CONFIG']['aws_secret_access_key']
                                           )
            self.client2 = boto3.client('logs',
                                       aws_access_key_id=self.config['AWS_CONFIG']['aws_access_key_id'],
                                       aws_secret_access_key=self.config['AWS_CONFIG']['aws_secret_access_key'])
        except Exception as e:
            print('failed to open file')
            self.config = None
            self.client = None
            self.resource = None

    def create_bucket(self, bucket_name):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """

        if self.resource is None:
            return None
        else:
            if self.resource.Bucket(bucket_name) not in self.resource.buckets.all():
                self.resource.create_bucket(Bucket=bucket_name)
                return self.resource.Bucket(bucket_name)
            else:
                return self.resource.Bucket(bucket_name)

    def create_folder(self, new_bucket):
        '''
        creates a new folder
        :param new_bucket: bucket created from create_bucket function
        :return: New folder in bucket
        '''
        if self.client is None:
            return None
        else:
            year = datetime.today().strftime('%Y')
            month = datetime.today().strftime('%m')
            day = datetime.today().strftime('%d')

            folder_list = new_bucket.objects.all()
            if self.resource.Object(new_bucket, '{}/{}/{}/'.format(year,month,day)) not in folder_list:
                self.client.put_object(Bucket = new_bucket.name, Key = '{}/{}/{}/'.format(year,month,day))

                return self.resource.Object(new_bucket, '{}/{}/{}/'.format(year, month, day))
            else:

                return self.resource.Object(new_bucket, '{}/{}/{}/'.format(year,month,day))

    def filter_events(self, startTime, endTime):
        '''
        filters the log events from AWS CloudWatch
        :param startTime: startTime
        :param endTime: endTime
        :return: None
        '''
        if self.client is None:
            return None
        else:
            kwargs = {
                'logGroupName': self.config['AWS_CONFIG']['log_group'],
                'limit': 10000,
                'filterPattern': '{ $.msg = "access-log"}'
            }

            if startTime is not None:
                kwargs['startTime'] = startTime
            if endTime is not None:
                kwargs['endTime'] = endTime

            while True:
                resp = self.client2.filter_log_events(**kwargs)
                yield from resp['events']
                try:
                    kwargs['nextToken'] = resp['nextToken']
                except KeyError:
                    break

    def create_json(self, startTime, endTime, bucket, folder):
        '''
        creates a new json file with the filtered log events
        :param startTime: startTime
        :param endTime: endTime
        :param bucket: bucket previously created
        :param folder: folder previously created
        :return: None
        '''
        if self.client is None:
            return None
        else:
            access_logs = []
            log_events = self.filter_events(startTime, endTime)

            hour = datetime.now().hour
            minute = datetime.now().minute
            filename = '{}-{}.json'.format(hour, minute)

            for event in log_events:
                #event["message"] contains the information that we need, so we only select that
                event["message"] = json.loads(event["message"])
                access_logs.append(event)


            print(access_logs)

            with open(filename, "a") as file:
                #to ensure json line is on its own line to start if access logs is not empty
                if len(access_logs) != 0:
                    file.write('\n')
                file.write('\n'.join(json.dumps(log) for log in access_logs))



                #this will concatenate the logs into a newline

            self.client.upload_file(filename, bucket.name, folder.key + filename)

            #return filename





obj = Bucket('config.ini')
bucket = obj.create_bucket('log-accumulation')
folder = obj.create_folder(bucket)


datetime_start = datetime.today() - timedelta(days = 7)

while int(datetime_start.timestamp()) < int(datetime.now().timestamp()):
    data = obj.create_json(
        # startTime = int((datetime.today() - timedelta(days = 7)).timestamp() * 1000),
        # endTime = int(datetime.now().timestamp() * 1000),
        startTime=int(datetime_start.timestamp() * 1000),
        endTime=int((datetime_start + timedelta(minutes=30)).timestamp() * 1000),
        bucket=bucket,
        folder=folder
    )
    datetime_start += timedelta(minutes=30)




#References
#"Add 30 Minutes in Time Object in Python" (n.d.) Stack Overflow. Retrieved August 23, 2021 from https://stackoverflow.com/questions/59277517/how-to-add-30-minutes-in-time-object-in-python-3
#"Creating Buckets" (n.d.). AWS Amazon. Retrieved August 3, 2021 from https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
#"Deleting a Folder" (2018, November 30). Edureka. Retrieved August 3, 2021 from https://www.edureka.co/community/31907/how-to-delete-a-folder-in-s3-bucket-using-boto3-using-python
#"Getting keys" (n.d.). AWS Amazon. Retrieved August 3, 2021 from https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object
#"How to Create a Folder" (n.d.). Stack Overflow. Retrieved August 3, 2021 https://stackoverflow.com/questions/1939743/amazon-s3-boto-how-to-create-a-folder
#"How to Get Hours and Minutes" (n.d.). Stack Overflow. Retrieved August 3, 2021 from https://stackoverflow.com/questions/51271937/how-to-get-just-the-hours-and-minutes-from-a-datetime-object
#"How to Get Last Modified Date of Latest File from S3 with Boto Python" (n.d.) Stack Overflow. Retrieved August 22, 2021 from https://stackoverflow.com/questions/60331144/how-to-get-last-modified-date-of-latest-file-from-s3-with-boto-python
#"How to Push a Single File to Subdirectory" (n.d.). Stack Overflow. Retrieved August 3, 2021 from https://stackoverflow.com/questions/13479763/how-to-push-a-single-file-in-a-subdirectory-to-github-not-master
#"How to Write File or Data to S3" (n.d.). Stack Overflow. Retrieved August 3, 2021 from https://stackoverflow.com/questions/40336918/how-to-write-a-file-or-data-to-an-s3-object-using-boto3
#"JSON list of Dictionaries Querying in AWS Athena Glue vs Quicksight" (n.d.) Stack Overflow. Retrieved August 20, 2021 from https://stackoverflow.com/questions/56227324/json-list-of-dictionaries-querying-in-aws-athena-glue-vs-quicksight
#"List S3 Folders" (n.d.). Stack Overflow. Retrieved August 3, 2021 from https://stackoverflow.com/questions/62463725/list-aws-s3-folders-with-boto3
#"Reading and Writing to JSON File" (n.d.). Stack Overflow. Retrieved August 3, 2021 from https://stackabuse.com/reading-and-writing-json-to-a-file-in-python
#Retrieving Subfolder Names" (n.d.). Stack Overflow. Retrieved August 3, 2021 from https://stackoverflow.com/questions/35803027/retrieving-subfolders-names-in-s3-bucket-from-boto3
#"Timestamp to Datetime" (n.d.) Programiz. Retrieved August 23, 2021 from https://www.programiz.com/python-programming/datetime/timestamp-datetime
#"Today's Date in YYYY-MM-DD" (n.d.). Stack Overflow. Retrieved August 3, 2021 from https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python
#"Writing JSON Files in One Txt File with Each JSON Data On Its Own Line" (n.d.). Stack Overflow. Retrieved August 20, 2021 from https://stackoverflow.com/questions/56281842/writing-json-files-in-one-txt-file-with-each-json-data-on-its-own-line










