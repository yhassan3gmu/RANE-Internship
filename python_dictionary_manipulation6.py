import json
from datetime import datetime
'''
This file uses boto3 to create Simple Storage Service (S3) objects (multiple folder names with JSON file name), 
upload filtered Amazon Web Services (AWS) CloudWatch log data to those objects, and then insert these objects to an AWS S3 bucket.
Object names follow a date format, bucket-name/year/month/day/hour-minute.json. New objects created will not overwrite or replace any previous objects or folders. 
Log data starts collecting 7 days before the run date of my program. Python program filters and collects logs for every half-hour interval. 
If the process takes more than a minute, whatever data isn’t added in the first JSON file goes to the next JSON file.

We will also use SQL in AWS Athena to query the JSON files.
▪	SQL will split columns with Python dictionaries into smaller columns.

'''

class DictionaryManipulator:
    def __init__(self, full_path_to_file = None):
        '''

        :param full_path_to_file:
        '''
        try:
            with open(full_path_to_file) as f:
                self.logdata = json.load(f)
        except Exception as e:
            print('failed to open file')
            self.logdata = None

    def get_unique_urls_for_users(self, logdata = None):
        '''
        unique urls by users
        :param logdata:
        :return: {user1: [unique_urls], user2: [unique_urls]}
        '''

        if not logdata:
            if not self.logdata:
                return {}
            else:
                logdata = self.logdata
        unique_urls = {}
        for log in logdata:
            if unique_urls.get(log.get('user', None).get('id'), None):
                unique_urls[log.get('user', None).get('id')] = list(set(unique_urls[log.get('user').get('id')] + [log.get('path', None)]))
            else:
                unique_urls.update({log.get('user', None).get('id'): [log.get('path', None)]})
        return unique_urls

    def get_unique_urls_for_given_user(self, user_id):
        '''
        unique urls for
        :return: [urls]
        '''
        if not self.logdata:
            return []
        #filter data for given user
        filter_log_data = list(filter(lambda x: x.get('user').get('id', None) == user_id, self.logdata))

        #if date is available, build info by reunising generic function
        if filter_log_data:
            #return only value for key from return type from generic function
            return self.get_unique_urls_for_users(filter_log_data).get(user_id, [])
        return [] #why

    def unique_urls_by_date(self, logdata = None):
        '''
        display Urls visited by user (attribute:   ) by date (attribute: timestamp),
        :param logdata: sample_logs.json list
        :param urls_by_date: empty dictionary to fill
        :return: {user 1: {date1: [urls], date2: [urls]}, user 2: {date1: [urls], date2: [urls]}}
        '''
        if not logdata:
            if not self.logdata:
                return {}
            else:
                logdata = self.logdata
        urls_by_date = {}
        for log in logdata:
            date = datetime.fromtimestamp(log['timestamp']).strftime('%d-%m-%y')
            #print(date)
            if urls_by_date.get(log.get('user', None).get('id')):
                #urls_by_date[log['user']['id']][date].append(log['path'])

                if urls_by_date.get(log.get('user', None).get('id')).get(date):
                    #urls_by_date[log['user']['id']][date] = list(set(urls_by_date[log['user']['id']][date] + log.get('path', None)))
                    urls_by_date[log['user']['id']][date].append(log['path'])
                else:
                    urls_by_date[log['user']['id']].update({date: [log.get('path', None)]})

            else:
                urls_by_date.update({log.get('user', None).get('id'): {date: []}})
            urls_by_date[log['user']['id']][date] = list(set(urls_by_date[log['user']['id']][date]))
            #urls_by_date[log['user']['id']] = list(set(urls_by_date[log['user']['id']]))
        return urls_by_date

    def avg_load_time(self, logdata = None):
        '''
        return average load time for each unique url
        :param logs:
        :param average_duration: empty dictionary
        :return: {url1: avg_load_time, url2: avg_load_time}
        '''
        if not logdata:
            if not self.logdata:
                return {}
            else:
                logdata = self.logdata
        average_duration = {}
        total_duration = {}
        tally_dict = {}
        for log in logdata:
            if total_duration.get(log['path'], None):
                #tally += 1
                total_duration[log['path']] += log['duration']
                tally_dict[log['path']] += 1
            else:
                total_duration.update({log.get('path', None): log.get('duration', None)})
                tally_dict[log['path']] = 1

        average_duration.update({k: float(total_duration[k])/tally_dict[k] for k in total_duration.keys()})
        return average_duration

if __name__ == '__main__':
    dm = DictionaryManipulator('sample_logs.json')
    op = dm.get_unique_urls_for_users()
    print(op)
    user_id = input('user_id ::')
    op_u = dm.get_unique_urls_for_given_user(user_id)
    print(op_u)
    vm = DictionaryManipulator()
    vp = vm.get_unique_urls_for_users()
    print(vp)
    user_id_again = input('user_id_again ::')
    vp_u = vm.get_unique_urls_for_given_user(user_id_again)
    print(vp_u)
    mp = dm.unique_urls_by_date()
    np = vm.unique_urls_by_date()
    print(mp)
    print(vp)
    x = dm.avg_load_time()
    y = vm.avg_load_time()
    print(x)
    print(y)
