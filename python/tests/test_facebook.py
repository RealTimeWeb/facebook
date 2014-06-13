import unittest

import sys
sys.path.append("../src")

try:
    import facebook
except ImportError:
    from python.src import facebook

# Remove these lines; we just do this for our own simplicity
with open('../src/secrets.txt', 'r') as secrets:
    ACCESS_TOKEN = secrets.readline()


class TestFacebook(unittest.TestCase):

    def test_get_facebook_information(self):
        facebook.connect()
        facebook._start_editing()

        keys = ['id', 'name', 'likes', 'statuses']

        user_dict = facebook.get_facebook_information(ACCESS_TOKEN)
        facebook._save_cache()
        self.assertTrue(isinstance(user_dict, dict))
        intersection = set(keys).intersection(user_dict)
        self.assertEqual(4, len(intersection))

        # Assure that the list of like dicts contain the following keys
        like_keys = ['name', 'category']

        likes = user_dict['likes']
        self.assertTrue(isinstance(like_keys, list))
        for like in likes:
            self.assertTrue(isinstance(like, dict))
            intersection = set(like_keys).intersection(like)
            self.assertEqual(2, len(intersection))

        # Assure that the list of status dicts contain the following keys
        status_keys = ['message', 'from', 'id', 'updated_time']

        statuses = user_dict['statuses']
        self.assertTrue(isinstance(status_keys, list))
        for status in statuses:
            self.assertTrue(isinstance(status, dict))
            intersection = set(status_keys).intersection(status)
            self.assertEqual(4, len(intersection))

    def test_offline_get_facebook_information(self):
        facebook.disconnect('./cache.json')
        keys = ['id', 'name', 'likes', 'statuses']

        user_dict = facebook.get_facebook_information(ACCESS_TOKEN)
        self.assertTrue(isinstance(user_dict, dict))
        intersection = set(keys).intersection(user_dict)
        self.assertEqual(4, len(intersection))

        # Assure that the list of like dicts contain the following keys
        like_keys = ['name', 'category']

        likes = user_dict['likes']
        self.assertTrue(isinstance(like_keys, list))
        for like in likes:
            self.assertTrue(isinstance(like, dict))
            intersection = set(like_keys).intersection(like)
            self.assertEqual(2, len(intersection))

        # Assure that the list of status dicts contain the following keys
        status_keys = ['message', 'from', 'id', 'updated_time']

        statuses = user_dict['statuses']
        self.assertTrue(isinstance(status_keys, list))
        for status in statuses:
            self.assertTrue(isinstance(status, dict))
            intersection = set(status_keys).intersection(status)
            self.assertEqual(4, len(intersection))


    def test_get_others_facebook_information(self):
        facebook.connect()
        facebook._start_editing()

        keys = ['id', 'name', 'statuses']

        user_dict = facebook.get_facebook_information(ACCESS_TOKEN, fb_id="660855297")
        facebook._save_cache()
        self.assertTrue(isinstance(user_dict, dict))
        intersection = set(keys).intersection(user_dict)
        self.assertEqual(3, len(intersection))

        # Assure that the list of status dicts contain the following keys
        status_keys = ['message', 'from', 'id', 'updated_time']

        statuses = user_dict['statuses']
        self.assertTrue(isinstance(status_keys, list))
        for status in statuses:
            self.assertTrue(isinstance(status, dict))
            intersection = set(status_keys).intersection(status)
            self.assertEqual(4, len(intersection))


    def test_offline_get_others_facebook_information(self):
        facebook.disconnect('./cache.json')
        keys = ['id', 'name', 'likes', 'statuses']

        user_dict = facebook.get_facebook_information(ACCESS_TOKEN, fb_id="660855297")
        self.assertTrue(isinstance(user_dict, dict))
        intersection = set(keys).intersection(user_dict)
        self.assertEqual(4, len(intersection))

        # Assure that the list of like dicts contain the following keys
        like_keys = ['name', 'category']

        likes = user_dict['likes']
        self.assertTrue(isinstance(like_keys, list))
        for like in likes:
            self.assertTrue(isinstance(like, dict))
            intersection = set(like_keys).intersection(like)
            self.assertEqual(2, len(intersection))

        # Assure that the list of status dicts contain the following keys
        status_keys = ['message', 'from', 'id', 'updated_time']

        statuses = user_dict['statuses']
        self.assertTrue(isinstance(status_keys, list))
        for status in statuses:
            self.assertTrue(isinstance(status, dict))
            intersection = set(status_keys).intersection(status)
            self.assertEqual(4, len(intersection))



    #
    # def test_get_stock_offline(self):
    #     src.disconnect("../src/cache.json")
    #
    #     keys = ['change_number', 'change_percentage', 'exchange_name',
    #             'last_trade_date_and_time', 'last_trade_price', 'ticker_name']
    #
    #     # Test getting one stock
    #     stock = src.get_stock_information("AAPL")
    #     self.assertTrue(isinstance(stock, dict))
    #
    #     # Assert all of the keys are in the stock
    #     intersection = set(keys).intersection(stock)
    #     self.assertEqual(6, len(intersection))
    #
    # def test_throw_exception(self):
    #     src.connect()
    #
    #     with self.assertRaises(src.FacebookException) as context:
    #         src.get_stock_information(["AAPL"])
    #
    #     self.assertEqual('Please enter a string of Stock Tickers', context.exception.args[0])
    #
    #     with self.assertRaises(src.FacebookException) as context:
    #         src.get_stock_information(1)
    #
    #     self.assertEqual('Please enter a string of Stock Tickers', context.exception.args[0])
    #
    #     with self.assertRaises(src.FacebookException) as context:
    #         src.get_stock_information("INVALID_STOCK")
    #
    #     self.assertEqual('Make sure you entered a valid stock', context.exception.args[0])
    #
    # def test_get_json(self):
    #
    #     appl = src.Stock(-1.16, -0.19, 'NASDAQ', 603.55, 'May 21, 11:26AM EDT','AAPL')
    #     appl_dict = appl._to_dict()
    #
    #     src.disconnect("../src/cache.json")
    #     json_res = src._fetch_stock_info({'q': 'AAPL'})
    #     cache_stock = src.Stock._from_json(json_res)
    #     cache_dict = cache_stock._to_dict()
    #
    #     self.assertDictEqual(cache_dict, appl_dict)
    #

if __name__ == "__main__":
    unittest.main()
