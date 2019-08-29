import unittest
import datetime
from tests.myTestCase import MyTestCase

from api.db import Session
from api.models import (Diver, DiveSite, Library, Permit,
                        SampleType, ScreenPlate)

class TestHeartBeatApi(MyTestCase):
    
    def setUp(self):
            # Set up test client
            self.client = self.app.test_client()

    def test_heartbeat(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json, {})
    

d1 = Diver(first_name='Jeff', last_name='van Santen')
d2 = Diver(first_name='Roger',last_name='Linington',
    institution='SFU',email='rliningt@sfu.ca',notes='PI')
class TestDiverApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        Session.add_all([d1,d2])
        Session.commit()

    def test_get_all(self):
        r = self.client.get('/divers')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/divers/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        data = r.json[0]
        self.assertEqual(data.get('first_name'), d1.first_name)

    def test_get_one_second(self):
        r = self.client.get('/divers/2')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        data = r.json[0]
        self.assertEqual(data.get('first_name'), d2.first_name)
        self.assertEqual(data.get('email'), d2.email)
    
    def test_get_one_invalid(self):
        r = self.client.get('/divers/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/divers/ABC')
        self.assertEqual(r.status_code, 404)


ds1 = DiveSite(name='test site 1', lat=1.1, lon=0.0)
ds2 = DiveSite(name='test site 2', lat=2.2, lon=0.0, 
    notes='This is a test site')
class TestDiveSiteApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        Session.add_all([ds1,ds2])
        Session.commit()

    def test_get_all(self):
        r = self.client.get('/divesites')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/divesites/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        data = r.json[0]
        self.assertEqual(data.get('name'), ds1.name)

    def test_get_one_second(self):
        r = self.client.get('/divesites/2')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        data = r.json[0]
        self.assertEqual(data.get('name'), ds2.name)
        self.assertEqual(data.get('notes'), ds2.notes)
    
    def test_get_one_invalid(self):
        r = self.client.get('/divesites/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/divesites/ABC')
        self.assertEqual(r.status_code, 404)


lib1 = Library(name='test library 1', abbrev='tl1')
lib2 = Library(name='test library 2', abbrev='tl2',
    description='Test library', notes='Test')
class TestLibraryApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        Session.add_all([lib1,lib2])
        Session.commit()

    def test_get_all(self):
        r = self.client.get('/libraries')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/libraries/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        data = r.json[0]
        self.assertEqual(data.get('name'), lib1.name)

    def test_get_one_second(self):
        r = self.client.get('/libraries/2')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        data = r.json[0]
        self.assertEqual(data.get('name'), lib2.name)
        self.assertEqual(data.get('notes'), lib2.notes)
    
    def test_get_one_invalid(self):
        r = self.client.get('/libraries/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/libraries/ABC')
        self.assertEqual(r.status_code, 404)


p1 = Permit(name='Permit 1', iss_auth='JVANSAN')
p2 = Permit(
    name='Permit 2', iss_auth='RLININGT', start_date=datetime.date.today(),
    end_date=datetime.date.today()+datetime.timedelta(days=365),
    notes='This is a note', file_dir='PERM_DIR', file_name='PERM_FILE'
)
class TestPermitApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        Session.add_all([p1,p2])
        Session.commit()

    def test_get_all(self):
        r = self.client.get('/permits')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/permits/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        data = r.json[0]
        self.assertEqual(data.get('name'), p1.name)

    def test_get_one_second(self):
        r = self.client.get('/permits/2')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        data = r.json[0]
        self.assertEqual(data.get('name'), p2.name)
        self.assertEqual(data.get('notes'), p2.notes)
    
    def test_get_one_invalid(self):
        r = self.client.get('/permits/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/permits/ABC')
        self.assertEqual(r.status_code, 404)


sp1 = ScreenPlate(name='ScreenPlate 1')
sp2 = ScreenPlate(name='ScreenPlate 2', notes='This is a note')
class TestScreenPlateApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        Session.add_all([sp1,sp2])
        Session.commit()

    def test_get_all(self):
        r = self.client.get('/screenplates')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/screenplates/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        data = r.json[0]
        self.assertEqual(data.get('name'), sp1.name)

    def test_get_one_second(self):
        r = self.client.get('/screenplates/2')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        data = r.json[0]
        self.assertEqual(data.get('name'), sp2.name)
        self.assertEqual(data.get('notes'), sp2.notes)
    
    def test_get_one_invalid(self):
        r = self.client.get('/screenplates/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/screenplates/ABC')
        self.assertEqual(r.status_code, 404)