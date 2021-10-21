import unittest
from python_dictionary_manipulation6 import DictionaryManipulator
import python_dictionary_manipulation6
import builtins
from unittest.mock import patch
#from python_dictionary_manipulation6 import user_id
from hamcrest import *
#https://stackoverflow.com/questions/14491164/python-unittest-asserting-dictionary-with-lists
#https://docs.python.org/3/library/unittest.html
#https://stackoverflow.com/questions/8866652/determine-if-2-lists-have-the-same-elements-regardless-of-order
#https://stackoverflow.com/questions/56340243/testing-user-input-python
class TestDictionaryManipulator(unittest.TestCase):
    def setUp(self):
        self.dm = DictionaryManipulator('sample_logs.json')
        self.vm = DictionaryManipulator()
        self.sample_dictionary = {'712910': ['/enterprise/geopolitical/search/', '/enterprise/geopolitical/',
                                    '/enterprise/geopolitical/region/eurasia'],
                         '713910': ['/enterprise/geopolitical/search/', '/enterprise/geopolitical/',
                                    '/enterprise/geopolitical/forecastquestions/',
                                    '/enterprise/geopolitical/components/content/',
                                    '/enterprise/geopolitical/forecast/',
                                    '/enterprise/geopolitical/theme/science-and-technology',
                                    '/enterprise/geopolitical/user/preference/'],
                         '712807': ['/enterprise/geopolitical/forecastquestions/detail/333790/333793',
                                    '/enterprise/geopolitical/country-risk/',
                                    '/enterprise/geopolitical/forecast/detail/332129',
                                    '/enterprise/geopolitical/forecastquestions/',
                                    '/enterprise/geopolitical/theme/science-and-technology',
                                    '/enterprise/geopolitical/region/europe',
                                    '/enterprise/geopolitical/theme/economics'],
                         '723910': ['/enterprise/geopolitical/forecastquestions/', '/enterprise/geopolitical/',
                                    '/enterprise/geopolitical/situation-report/japan-government-declare-covid-19-emergencies-tokyo-osaka',
                                    '/enterprise/geopolitical/forecastquestions/detail/333790/333793'],
                         '725910': ['/enterprise/geopolitical/forecastquestions/detail/333790/333793',
                                    '/enterprise/geopolitical/situation-report/japan-government-declare-covid-19-emergencies-tokyo-osaka',
                                    '/enterprise/geopolitical/region/europe'],
                         '712819': ['/enterprise/geopolitical/forecast/detail/332129',
                                    '/enterprise/geopolitical/forecastquestions/',
                                    '/enterprise/geopolitical/country-risk/'],
                         '708210': ['/enterprise/geopolitical/forecastquestions/',
                                    '/enterprise/geopolitical/theme/politics',
                                    '/enterprise/geopolitical/user/profile/',
                                    '/enterprise/geopolitical/region/sub-saharan-africa']}
        self.sample_dictionary_date = {'712910': {'31-05-21': ['/enterprise/geopolitical/region/eurasia', '/enterprise/geopolitical/search/', '/enterprise/geopolitical/']}, '713910': {'31-05-21': ['/enterprise/geopolitical/forecastquestions/', '/enterprise/geopolitical/search/', '/enterprise/geopolitical/forecast/', '/enterprise/geopolitical/theme/science-and-technology'], '01-06-21': ['/enterprise/geopolitical/user/preference/', '/enterprise/geopolitical/components/content/']}, '712807': {'31-05-21': ['/enterprise/geopolitical/theme/economics', '/enterprise/geopolitical/forecastquestions/detail/333790/333793', '/enterprise/geopolitical/forecast/detail/332129', '/enterprise/geopolitical/forecastquestions/', '/enterprise/geopolitical/country-risk/', '/enterprise/geopolitical/region/europe']}, '723910': {'31-05-21': ['/enterprise/geopolitical/forecastquestions/', '/enterprise/geopolitical/situation-report/japan-government-declare-covid-19-emergencies-tokyo-osaka', '/enterprise/geopolitical/forecastquestions/detail/333790/333793', '/enterprise/geopolitical/']}, '725910': {'31-05-21': ['/enterprise/geopolitical/situation-report/japan-government-declare-covid-19-emergencies-tokyo-osaka', '/enterprise/geopolitical/forecastquestions/detail/333790/333793', '/enterprise/geopolitical/region/europe']}, '712819': {'31-05-21': ['/enterprise/geopolitical/forecast/detail/332129', '/enterprise/geopolitical/country-risk/', '/enterprise/geopolitical/forecastquestions/']}, '708210': {'31-05-21': [], '01-06-21': ['/enterprise/geopolitical/region/sub-saharan-africa', '/enterprise/geopolitical/theme/politics', '/enterprise/geopolitical/user/profile/']}}
        self.sample_dictionary_duration = {'/enterprise/geopolitical/': 2.716975258983439, '/enterprise/geopolitical/search/': 1.296049644666103, '/enterprise/geopolitical/region/eurasia': 2.6388568629821143, '/enterprise/geopolitical/theme/science-and-technology': 4.432117980322801, '/enterprise/geopolitical/forecast/': 4.610198409684624, '/enterprise/geopolitical/forecastquestions/': 3.598553336763871, '/enterprise/geopolitical/situation-report/japan-government-declare-covid-19-emergencies-tokyo-osaka': 0.9668719970155507, '/enterprise/geopolitical/forecastquestions/detail/333790/333793': 2.9322941033169627, '/enterprise/geopolitical/region/europe': 2.7323795491829515, '/enterprise/geopolitical/country-risk/': 1.8974838887370424, '/enterprise/geopolitical/theme/economics': 2.3742166492156684, '/enterprise/geopolitical/forecast/detail/332129': 1.4091182124102488, '/enterprise/geopolitical/region/sub-saharan-africa': 3.532708836020902, '/enterprise/geopolitical/user/preference/': 0.9358140089316294, '/enterprise/geopolitical/user/profile/': 0.5825790609233081, '/enterprise/geopolitical/theme/politics': 2.3608193369582295, '/enterprise/geopolitical/components/content/': 0.4091331879608333}
    def test_get_unique_urls_for_users(self):
        #self.assert_that(self.dm.get_unique_urls_for_users(), has_entries(self.sample_dictionary))
        #self.assertDictEqual(self.dm.get_unique_urls_for_users(), self.sample_dictionary)
        self.assertEqual(set(self.dm.get_unique_urls_for_users().keys()), set(self.sample_dictionary.keys()))
        for i in self.dm.get_unique_urls_for_users().keys():
            self.assertEqual(set(self.dm.get_unique_urls_for_users()[i]), set(self.sample_dictionary[i]))
        self.assertDictEqual(self.vm.get_unique_urls_for_users(), {})

    @patch('python_dictionary_manipulation6.input', create=True)
    def test_get_unique_urls_for_given_user(self, user_id):
        #user_id = input('Enter id:')
        #user_id.side_effect
        for id in self.sample_dictionary.keys():
            self.assertEqual(set(self.dm.get_unique_urls_for_given_user(id)), set(self.sample_dictionary[id]))

        #with 'builtins.input' as user_id:
        if user_id not in self.sample_dictionary.keys():
            self.assertEqual(self.dm.get_unique_urls_for_given_user(user_id), [])
        else:
            self.assertEqual(set(self.dm.get_unique_urls_for_given_user(user_id)),
                                set(self.sample_dictionary[user_id]))

            self.assertEqual(self.vm.get_unique_urls_for_given_user(user_id), [])
        # self.assertEqual(self.vm.get_unique_urls_for_given_user(other_dm_input), [])

    def test_unique_urls_by_date(self):
        self.assertEqual(set(self.dm.unique_urls_by_date().keys()), set(self.sample_dictionary_date.keys()))
        for user in self.dm.unique_urls_by_date().keys():
            self.assertEqual(set(self.dm.unique_urls_by_date()[user].keys()), set(self.sample_dictionary_date[user].keys()))

            for date in self.dm.unique_urls_by_date()[user].keys():
                self.assertEqual(set(self.dm.unique_urls_by_date()[user][date]), set(self.sample_dictionary_date[user][date]))

        self.assertDictEqual(self.vm.unique_urls_by_date(), {})

    def test_avg_load_time(self):
        self.assertDictEqual(self.dm.avg_load_time(), self.sample_dictionary_duration)
        self.assertDictEqual(self.vm.avg_load_time(), {})
        #self.assertEqual(self.dm.avg_load_time(), self.sample_dictionary_duration)
        #self.assertEqual(self.vm.avg_load_time(), {})
        #why does this work for assert equa







