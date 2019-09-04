import unittest
import datetime
from tests.myTestCase import MyTestCase

from api.db import Session
from api.models import (Diver, DiveSite, Extract, Fraction,
                        FractionScreenPlate, Isolate, IsolateStock, Library,
                        Media, MediaRecipe, Permit, Sample, SampleType,
                        ScreenPlate, session_scope)


class TestHeartBeatApi(MyTestCase):

    def setUp(self):
            # Set up test client
            self.client = self.app.test_client()

    def test_heartbeat(self):
        r = self.client.get('/api/v1/')
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json, {})


d1 = Diver(first_name='Jeff', last_name='van Santen')
d2 = Diver(first_name='Roger',last_name='Linington',
    institution='SFU',email='rliningt@sfu.ca',notes='PI')
d_s = Sample(name='Diver Sample', collection_number=1, collection_year=1,
    divers=[d1,d2]
)
class TestDiverApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        with session_scope() as sess:
            sess.add_all([d1,d2, d_s])

    def test_get_all(self):
        r = self.client.get('/api/v1/divers')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2)

    def test_get_one_first(self):
        r = self.client.get('/api/v1/divers/1')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('first_name'), "Jeff")

    def test_get_one_second(self):
        r = self.client.get('/api/v1/divers/2')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('first_name'), "Roger")
        self.assertEqual(data.get('email'), "rliningt@sfu.ca")

    def test_get_one_invalid(self):
        r = self.client.get('/api/v1/divers/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/api/v1/divers/ABC')
        self.assertEqual(r.status_code, 404)

    def test_get_one_good_embed_samples(self):
        r = self.client.get('/api/v1/divers/1?embed=samples')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('samples').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_bad_embed(self):
        r = self.client.get('/api/v1/divers/1?embed=BAD')
        self.assertEqual(r.status_code, 404)


ds1 = DiveSite(name='test site 1', lat=1.1, lon=0.0)
ds2 = DiveSite(name='test site 2', lat=2.2, lon=0.0,
    notes='This is a test site')
ds_s = Sample(name='DiveSite Sample', collection_number=1, collection_year=1,
    dive_site=ds1
)
class TestDiveSiteApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        with session_scope() as sess:
            sess.add_all([ds1,ds2])

    def test_get_all(self):
        r = self.client.get('/api/v1/divesites')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/api/v1/divesites/1')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "test site 1")

    def test_get_one_second(self):
        r = self.client.get('/api/v1/divesites/2')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "test site 2")
        self.assertEqual(data.get('notes'), "This is a test site")

    def test_get_one_invalid(self):
        r = self.client.get('/api/v1/divesites/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/api/v1/divesites/ABC')
        self.assertEqual(r.status_code, 404)

    def test_get_one_good_embed_samples(self):
        r = self.client.get('/api/v1/divesites/1?embed=samples')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('samples').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_bad_embed(self):
        r = self.client.get('/api/v1/divesites/1?embed=BAD')
        self.assertEqual(r.status_code, 404)


lib1 = Library(name='test library 1', abbrev='tl1')
lib2 = Library(name='test library 2', abbrev='tl2',
    description='Test library', notes='Test')
lib_extract = Extract(number=1, library=lib1)
class TestLibraryApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        with session_scope() as sess:
            sess.add_all([lib1,lib2])

    def test_get_all(self):
        r = self.client.get('/api/v1/libraries')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/api/v1/libraries/1')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "test library 1")

    def test_get_one_second(self):
        r = self.client.get('/api/v1/libraries/2')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "test library 2")
        self.assertEqual(data.get('notes'), "Test")

    def test_get_one_invalid(self):
        r = self.client.get('/api/v1/libraries/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/api/v1/libraries/ABC')
        self.assertEqual(r.status_code, 404)

    def test_get_one_good_embed_samples(self):
        r = self.client.get('/api/v1/libraries/1?embed=extracts')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('extracts').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_bad_embed(self):
        r = self.client.get('/api/v1/libraries/1?embed=BAD')
        self.assertEqual(r.status_code, 404)


p1 = Permit(name='Permit 1', iss_auth='JVANSAN')
p2 = Permit(
    name='Permit 2', iss_auth='RLININGT', start_date=datetime.date.today(),
    end_date=datetime.date.today()+datetime.timedelta(days=365),
    notes='This is a note', file_dir='PERM_DIR', file_name='PERM_FILE'
)
p_s = Sample(name='Permit Sample', collection_number=1, collection_year=1,
    permit=p1
)

class TestPermitApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        with session_scope() as sess:
            sess.add_all([p1,p2])

    def test_get_all(self):
        r = self.client.get('/api/v1/permits')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/api/v1/permits/1')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "Permit 1")

    def test_get_one_second(self):
        r = self.client.get('/api/v1/permits/2')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "Permit 2")
        self.assertEqual(data.get('notes'), "This is a note")

    def test_get_one_invalid(self):
        r = self.client.get('/api/v1/permits/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/api/v1/permits/ABC')
        self.assertEqual(r.status_code, 404)

    def test_get_one_good_embed_samples(self):
        r = self.client.get('/api/v1/permits/1?embed=samples')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('samples').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_bad_embed(self):
        r = self.client.get('/api/v1/permits/1?embed=BAD')
        self.assertEqual(r.status_code, 404)


sp1 = ScreenPlate(name='ScreenPlate 1')
sp2 = ScreenPlate(name='ScreenPlate 2', notes='This is a note')
class TestScreenPlateApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        with session_scope() as sess:
            sess.add_all([sp1,sp2])

    def test_get_all(self):
        r = self.client.get('/api/v1/screenplates')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/api/v1/screenplates/1')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "ScreenPlate 1")

    def test_get_one_second(self):
        r = self.client.get('/api/v1/screenplates/2')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "ScreenPlate 2")
        self.assertEqual(data.get('notes'), "This is a note")

    def test_get_one_invalid(self):
        r = self.client.get('/api/v1/screenplates/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/api/v1/screenplates/ABC')
        self.assertEqual(r.status_code, 404)


sample_dive_site=DiveSite(name='Sample diversite', lat=1.1, lon=0.0)
diver_s1=Diver(first_name='Test', last_name='Diver1')
diver_s2=Diver(first_name='Test', last_name='Diver2')
sample_sample_type=SampleType(name='Sample sample type')
sample_permit=Permit(name='sample permit', iss_auth='jvansan')
sample_isolate=Isolate(name='sample isolate')
sample_1 = Sample(name='RL01-001', collection_number=1, collection_year=1)
# sample 2 gets all attributes for testing
sample_2 = Sample(name='RL02-002', collection_number=2, collection_year=2,
    collection_date=datetime.date.today(),
    color='blue', depth_ft=2.0, genus_species='Test sp.',
    notes='This is my test', insert_by='1', 
    insert_date=datetime.datetime.today(),
    dive_site=sample_dive_site, divers=[diver_s1, diver_s2],
    sample_type=sample_sample_type,
    isolates=[sample_isolate],
    permit=sample_permit
)

class TestSampleApi(MyTestCase):
    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        with session_scope() as sess:
            sess.add_all([sample_1,sample_2])

    def test_get_all(self):
        r = self.client.get('/api/v1/samples')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/api/v1/samples/1')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "RL01-001")

    def test_get_one_second(self):
        r = self.client.get('/api/v1/samples/2')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "RL02-002")
        self.assertEqual(data.get('notes'), "This is my test")

    def test_get_one_invalid(self):
        r = self.client.get('/api/v1/samples/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/api/v1/samples/ABC')
        self.assertEqual(r.status_code, 404)

    def test_get_one_good_embed_divers(self):
        r = self.client.get('/api/v1/samples/2?embed=divers')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('divers').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 2)

    def test_get_one_good_embed_divesite(self):
        r = self.client.get('/api/v1/samples/2?embed=divesites')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('divesites').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_good_embed_sampletypes(self):
        r = self.client.get('/api/v1/samples/2?embed=sampletypes')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('sampletypes').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_good_embed_permits(self):
        r = self.client.get('/api/v1/samples/2?embed=permits')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('permits').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_good_embed_isolates(self):
        r = self.client.get('/api/v1/samples/2?embed=isolates')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('isolates').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_bad_embed(self):
        r = self.client.get('/api/v1/samples/1?embed=BAD')
        self.assertEqual(r.status_code, 404)


isolate_media = Media(name="TEST")
isolate_sample = Sample(name="isolate sample", 
    collection_number=1, collection_year=1)
isolate_extract = Extract(number=1)
isolate_isolate_stock = IsolateStock(box=0)
isolate_1 = Isolate(name='isolate 1')
isolate_2 = Isolate(
    name='isolate 2', media=isolate_media,
    sample=isolate_sample, extracts=[isolate_extract],
    stocks=[isolate_isolate_stock]
)

class TestIsolateApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        with session_scope() as sess:
            sess.add_all([isolate_1,isolate_2])

    def test_get_all(self):
        r = self.client.get('/api/v1/isolates')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/api/v1/isolates/1')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "isolate 1")

    def test_get_one_second(self):
        r = self.client.get('/api/v1/isolates/2')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "isolate 2")

    def test_get_one_invalid(self):
        r = self.client.get('/api/v1/isolates/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/api/v1/isolates/ABC')
        self.assertEqual(r.status_code, 404)

    def test_get_one_good_embed_samples(self):
        r = self.client.get('/api/v1/isolates/2?embed=samples')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('samples').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_good_embed_extracts(self):
        r = self.client.get('/api/v1/isolates/2?embed=extracts')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('extracts').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_good_embed_stocks(self):
        r = self.client.get('/api/v1/isolates/2?embed=stocks')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('stocks').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_good_embed_media(self):
        r = self.client.get('/api/v1/isolates/2?embed=media')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('media').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_bad_embed(self):
        r = self.client.get('/api/v1/isolates/1?embed=BAD')
        self.assertEqual(r.status_code, 404)


extract_isolate = Isolate(name='extract isolate')
extract_media = Media(name='TEST')
extract_library = Library(abbrev='JVS', name='Jeff Test')
extract_fraction = Fraction(code='A')
extract_1 = Extract(number=1)
extract_2 = Extract(
    number=2, temp=25, rpm=100., inoculation_date=datetime.date.today(),
    growth_time_h=12, volume_ml=1000., mass_g=100.,
    seal='Seal', percent_inoculum=50., spring=False, shaken=True,
    flask_type='Erlenmeyer', flask_capacity_l = 1.,
    resin_mass_g=10., notes="Test", insert_by=1, 
    insert_date=datetime.datetime.today(),
    isolate=extract_isolate,
    media=extract_media,
    library=extract_library,
    fractions=[extract_fraction]
)

class TestExtractApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        with session_scope() as sess:
            sess.add_all([extract_1,extract_2])

    def test_get_all(self):
        r = self.client.get('/api/v1/extracts')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/api/v1/extracts/1')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), None)

    def test_get_one_second(self):
        r = self.client.get('/api/v1/extracts/2')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "RLJVS-0002")

    def test_get_one_invalid(self):
        r = self.client.get('/api/v1/extracts/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/api/v1/extracts/ABC')
        self.assertEqual(r.status_code, 404)

    def test_get_one_good_embed_isolates(self):
        r = self.client.get('/api/v1/extracts/2?embed=isolates')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('isolates').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_good_embed_fractions(self):
        r = self.client.get('/api/v1/extracts/2?embed=fractions')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('fractions').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_good_embed_libraries(self):
        r = self.client.get('/api/v1/extracts/2?embed=libraries')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('libraries').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_good_embed_media(self):
        r = self.client.get('/api/v1/extracts/2?embed=media')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('media').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_bad_embed(self):
        r = self.client.get('/api/v1/extracts/1?embed=BAD')
        self.assertEqual(r.status_code, 404)


fraction_extract = Extract(number=1, library=Library(name="TEST", abbrev="JVS"))
fraction_1 = Fraction(code="A")
fraction_2 = Fraction(code="B", extract=fraction_extract)

class TextFractionApi(MyTestCase):

    def setUp(self):
        # Set up test client
        self.client = self.app.test_client()
        with session_scope() as sess:
            sess.add_all([fraction_1,fraction_2])

    def test_get_all(self):
        r = self.client.get('/api/v1/fractions')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data), 2, msg=f'{r}')

    def test_get_one_first(self):
        r = self.client.get('/api/v1/fractions/1')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), None)

    def test_get_one_second(self):
        r = self.client.get('/api/v1/fractions/2')
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('name'), "RLJVS-0001B")

    def test_get_one_invalid(self):
        r = self.client.get('/api/v1/fractions/3')
        self.assertEqual(r.status_code, 404)

    def test_get_one_bad_query(self):
        r = self.client.get('/api/v1/fractions/ABC')
        self.assertEqual(r.status_code, 404)

    def test_get_one_good_embed_extracts(self):
        r = self.client.get('/api/v1/fractions/2?embed=extracts')
        data = r.json
        self.assertIsInstance(data, dict)
        embedded = data.get('extracts').get('embedded')
        self.assertIsInstance(embedded, list)
        self.assertEqual(len(embedded), 1)

    def test_get_one_bad_embed(self):
        r = self.client.get('/api/v1/extracts/1?embed=BAD')
        self.assertEqual(r.status_code, 404)