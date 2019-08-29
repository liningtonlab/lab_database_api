import unittest

from api.app import create_app
from api.common.sql_models import Base
from api.db import Session


class MyTestCase(unittest.TestCase):
    
    def tearDown(self):
        Session.rollback()

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')

    @classmethod
    def tearDownClass(cls):
        Session.remove()
        Base.metadata.drop_all(bind=cls.app.engine)