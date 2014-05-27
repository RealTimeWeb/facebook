import unittest
from python.facebook import facebook

# Embed your own keys for simplicity
ACCESS_TOKEN = "your key goes here"
# Remove these lines; we just do this for our own simplicity
with open('../facebook/secrets.txt', 'r') as secrets:
    ACCESS_TOKEN = secrets.readline()


class TestFacebook(unittest.TestCase):

    def test_get_facebook_information(self):
        facebook.connect()

        keys = ['albums', 'feed', 'friendslist', 'likes', 'name', 'notifications',
                'photos', 'statuses']

        # Test getting one stock
        user_dict = facebook.get_facebook_information(ACCESS_TOKEN)
        print(user_dict)
        # self.assertTrue(isinstance(stock, dict))
        #
        # # Assert all of the keys are in the stock
        # intersection = set(keys).intersection(stock)
        # self.assertEqual(6, len(intersection))
    #
    # def test_get_stock_offline(self):
    #     facebook.disconnect("../facebook/cache.json")
    #
    #     keys = ['change_number', 'change_percentage', 'exchange_name',
    #             'last_trade_date_and_time', 'last_trade_price', 'ticker_name']
    #
    #     # Test getting one stock
    #     stock = facebook.get_stock_information("AAPL")
    #     self.assertTrue(isinstance(stock, dict))
    #
    #     # Assert all of the keys are in the stock
    #     intersection = set(keys).intersection(stock)
    #     self.assertEqual(6, len(intersection))
    #
    # def test_throw_exception(self):
    #     facebook.connect()
    #
    #     with self.assertRaises(facebook.FacebookException) as context:
    #         facebook.get_stock_information(["AAPL"])
    #
    #     self.assertEqual('Please enter a string of Stock Tickers', context.exception.args[0])
    #
    #     with self.assertRaises(facebook.FacebookException) as context:
    #         facebook.get_stock_information(1)
    #
    #     self.assertEqual('Please enter a string of Stock Tickers', context.exception.args[0])
    #
    #     with self.assertRaises(facebook.FacebookException) as context:
    #         facebook.get_stock_information("INVALID_STOCK")
    #
    #     self.assertEqual('Make sure you entered a valid stock', context.exception.args[0])
    #
    # def test_get_json(self):
    #
    #     appl = facebook.Stock(-1.16, -0.19, 'NASDAQ', 603.55, 'May 21, 11:26AM EDT','AAPL')
    #     appl_dict = appl._to_dict()
    #
    #     facebook.disconnect("../facebook/cache.json")
    #     json_res = facebook._fetch_stock_info({'q': 'AAPL'})
    #     cache_stock = facebook.Stock._from_json(json_res)
    #     cache_dict = cache_stock._to_dict()
    #
    #     self.assertDictEqual(cache_dict, appl_dict)
    #
