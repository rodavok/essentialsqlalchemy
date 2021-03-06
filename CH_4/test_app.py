import unittest
from app import get_orders_by_customer
from db import dal  #, prep_db
from unittest import mock
from decimal import Decimal


class TestApp(unittest.TestCase):  # test classes must inherit from TestCase
    cookie_orders = [(u'wlk001', u'cookiemon', u'111-111-1111'),
                     (u'wlk002', u'cookiemon', u'111-111-1111', True)]
    cookie_details = [(u'wlk001', u'cookiemon', u'111-111-1111',
                       u'dark chocolate chip', 2, Decimal('1.00')),
                      (u'wlk001', u'cookiemon', u'111-111-1111',
                       u'oatmeal raisin', 12, Decimal('3.00'))]

    @mock.patch('app.dal.connection')
    def test_orders_by_customer(self, mock_conn):
        mock_conn.execute.return_value.fetchall.return_value = self.cookie_orders
        results = get_orders_by_customer('cookiemon')
        self.assertEqual(results, self.cookie_orders)

    @mock.patch('app.select')
    @mock.patch('app.dal.connection')
    def test_orders_by_customer_blank(self, mock_conn, mock_select):
        mock_select.return_value.select_from.return_value.\
            where.return_value = ''
        mock_conn.execute.return_value.fetchall.return_value = []
        results = get_orders_by_customer('')
        self.assertEqual(results, [])

    @mock.patch('app.select')
    @mock.patch('app.dal.connection')
    def test_orders_by_customer_blank_shipped(self, mock_conn, mock_select):
        mock_select.return_value.select_from.return_value = self.cookie_orders
        mock_conn.execute.return_value.fetchall.return_value = []
        results = get_orders_by_customer('', True)
        self.assertEqual(results, [])

    #def test_orders_by_customer_blank_notshipped(self):

    #def test_orders_by_customer_blank_details(self):

    #def test_orders_by_customer_unshipped_only(self):
    '''
    @classmethod
    def setUpClass(
            cls):  # class needs to be setup by initializing the database
        dal.db_init("sqlite:///:memory:")
        prep_db()

    """
    orders by customers takes three parameters
    cust_name, (string, invalid string, or none)
    columns, (true, false, none)
    joins (true, false)
    3*3*2 = 12, so 12 tests are required to fully test
    """

    # unittest expects every test function to start with 'test'

    def test_orders_by_customer_blank(self):
        results = get_orders_by_customer("")
        self.assertEqual(results, [])

    def test_orders_by_customer_blank_shipped(self):
        results = get_orders_by_customer("", True)
        self.assertEqual(results, [])

    def test_orders_by_customer_blank_notshipped(self):
        results = get_orders_by_customer("", False)
        self.assertEqual(results, [])

    def test_orders_by_customer_blank_details(self):
        results = get_orders_by_customer("", details=True)
        self.assertEqual(results, [])

    def test_orders_by_customer_blank_shipped_details(self):
        results = get_orders_by_customer("", True, True)
        self.assertEqual(results, [])

    def test_orders_by_customer_blank_notshipped_details(self):
        results = get_orders_by_customer("", False, True)
        self.assertEqual(results, [])

    # tests for valid and invalid strings

    def test_orders_by_customer(self):
        expected_results = [(u"wlk001", u"cookiemon", u"111-111-1111")]
        results = get_orders_by_customer("cookiemon")
        self.assertEqual(results, expected_results)

    def test_orders_by_customer_shipped_only(self):
        results = get_orders_by_customer("cookiemon", True)
        self.assertEqual(results, [])

    def test_orders_by_customer_unshipped_only(self):
        expected_results = [(u"wlk001", u"cookiemon", u"111-111-1111")]
        results = get_orders_by_customer("cookiemon", False)
        self.assertEqual(results, expected_results)

    def test_orders_by_customer_with_details(self):
        expected_results = [
            (
                u"wlk001",
                u"cookiemon",
                u"111-111-1111",
                u"dark chocolate chip",
                2,
                Decimal("1.00"),
            ),
            (
                u"wlk001",
                u"cookiemon",
                u"111-111-1111",
                u"oatmeal raisin",
                12,
                Decimal("3.00"),
            ),
        ]

        results = get_orders_by_customer("cookiemon", details=True)
        self.assertEqual(results, expected_results)

    def test_orders_by_customer_shipped_only_with_details(self):
        results = get_orders_by_customer("cookiemon", True, True)
        self.assertEqual(results, [])

    def test_orders_by_customer_unshipped_only_details(self):
        expected_results = [
            (
                u"wlk001",
                u"cookiemon",
                u"111-111-1111",
                u"dark chocolate chip",
                2,
                Decimal("1.00"),
            ),
            (
                u"wlk001",
                u"cookiemon",
                u"111-111-1111",
                u"oatmeal raisin",
                12,
                Decimal("3.00"),
            ),
        ]
        results = get_orders_by_customer("cookiemon", False, True)
        self.assertEqual(results, expected_results)

    def test_orders_by_customer_without_details(self):
        expected_results = [('ol001', 'cakeeater', '222-222-2222')]
        results = get_orders_by_customer('cakeeater', details=False)
        self.assertEqual(results, expected_results)

    def test_orders_by_customer_invalid_user(self):
        expected_results = []
        results = get_orders_by_customer('invalid_user', details=False)
        self.assertEqual(results, expected_results)
'''