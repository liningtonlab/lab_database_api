import datetime
import unittest

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tests.myTestCase import MyTestCase

from api.db import Session
from api.models import (Diver, DiveSite, Extract, Fraction,
                        FractionScreenPlate, Isolate, IsolateStock, Library,
                        Media, MediaRecipe, Permit, Sample, SampleType,
                        ScreenPlate, get_all, get_one, session_scope)
"""
Cannot currently catch SQLite errors through Python
https://bugs.python.org/issue16379

This means cannot test exception handling with SQLite database.
For this reason, all testing should be done with a MySQL database.
This is fine because the production system uses MySQL.
"""


# Define Test Divers
diver_1 = Diver(id=1, first_name='Test', last_name='Case1')
diver_2 = Diver(id=2, first_name='Test', last_name='Case2')
diver_empty = Diver()
diver_sample = Sample(name='Diver Sample', collection_number=1, collection_year=1,
    divers=[diver_2]
)
# Diver is allowed to be empty...

class TestDiverModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([diver_1, diver_2, diver_empty])
    
    def test_get_one(self):
        res = get_one(Diver, 1)
        self.assertIsInstance(res, Diver)
        self.assertEqual(res.id, 1)

    def test_get_all(self):
        res = get_all(Diver)
        self.assertEqual(len(res), 3)
        for r in res:
            self.assertIsInstance(r, Diver)
    
    def test_get_third_empty_attributes(self):
        res = get_one(Diver, 3)
        self.assertEqual(res.first_name, None)
        self.assertEqual(res.last_name, None)

    def test_relationship(self):
        res = get_one(Diver, 2)
        self.assertIsInstance(res, Diver)
        self.assertIsInstance(res.samples[0], Sample)

    def test_bad_relationship(self):
        res = get_one(Diver, 2)
        self.assertIsInstance(res, Diver)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.sample



# Define Test DiveSites
divesite_1 = DiveSite(name='test site 1', lat=1.1, lon=0.0)
divesite_2 = DiveSite(name='test site 2', lat=2.2, lon=0.0)
divesite_bad_lat = DiveSite(name='bad lat', lon=0.0)
divesite_bad_lon = DiveSite(name='bad lon', lat=0.0)
diversite_sample = Sample(name='DiveSite Sample', collection_number=1, collection_year=1,
    dive_site=divesite_2
)

class TestDiveSiteModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([divesite_1, divesite_2])

    def test_get_one(self):
        res = get_one(DiveSite, 1)
        self.assertIsInstance(res, DiveSite)

    def test_get_all(self):
        res = get_all(DiveSite)
        self.assertEqual(len(res), 2)
        for r in res:
            self.assertIsInstance(r, DiveSite)

    def test_bad_lat(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(divesite_bad_lat)

    def test_bad_lon(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(divesite_bad_lon)

    def test_relationship(self):
        res = get_one(DiveSite, 2)
        self.assertIsInstance(res, DiveSite)
        self.assertIsInstance(res.samples[0], Sample)

    def test_bad_relationship(self):
        res = get_one(DiveSite, 2)
        self.assertIsInstance(res, DiveSite)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.sample


# Define Test Library
library_1 = Library(name='library 1', abbrev='l1')
library_2 = Library(name='library 2', abbrev='l2')
library_extract = Extract(number=1, library=library_2)
library_bad_abbrev = Library(name='bad abbrev')
library_bad_name = Library(abbrev='bn')

class TestLibraryModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([library_1, library_2])

    def test_get_one(self):
        res = get_one(Library, 1)
        self.assertIsInstance(res, Library)

    def test_get_all(self):
        res = get_all(Library)
        self.assertEqual(len(res), 2)
        for r in res:
            self.assertIsInstance(r, Library)

    def test_bad_name(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(library_bad_name)

    def test_bad_abbrev(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(library_bad_abbrev)

    def test_relationship(self):
        res = get_one(Library, 2)
        self.assertIsInstance(res, Library)
        self.assertIsInstance(res.extracts[0], Extract)

    def test_bad_relationship(self):
        res = get_one(Library, 2)
        self.assertIsInstance(res, Library)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.sample


# Define Test Permits
permit_1 = Permit(
    name='Test permit',
    iss_auth='jvansan'
)
permit_2 = Permit(
    name='Test permit 2',
    iss_auth='jvansan',
    start_date=datetime.date.today(),
    end_date=datetime.date.today()+datetime.timedelta(weeks=50)
)
permit_sample = Sample(name='Permit Sample', collection_number=1, collection_year=1,
    permit=permit_2
)
# MySQL accepts datetime string...
permit_string_date = Permit(name='Datetime permit', iss_auth='jvansan',
                                   start_date="2019-08-27")
permit_noname = Permit(iss_auth='jvansan')
permit_noissauth = Permit(name='No Issuing Auth')

class TestPermitModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([permit_1, permit_2, permit_string_date])

    def test_get_one(self):
        res = get_one(Permit, 1)
        self.assertIsInstance(res, Permit)

    def test_get_all(self):
        res = get_all(Permit)
        self.assertEqual(len(res), 3)
        for r in res:
            self.assertIsInstance(r, Permit)

    def test_bad_name(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(permit_noname)

    def test_bad_iss_auth(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(permit_noissauth)

    def test_string_date(self):
        res = get_one(Permit, 3)
        self.assertEqual(datetime.date(year=2019, month=8, day=27), res.start_date)

    def test_relationship(self):
        res = get_one(Permit, 2)
        self.assertIsInstance(res, Permit)
        self.assertIsInstance(res.samples[0], Sample)

    def test_bad_relationship(self):
        res = get_one(Permit, 2)
        self.assertIsInstance(res, Permit)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.sample


# Define Test SampleType
sampletype_1 = SampleType(name='sample type 1')
sampletype_2 = SampleType(name='sample type 2')
sampletype_sample = Sample(name='SampleType Sample', collection_number=1, collection_year=1,
    sample_type=sampletype_2
)
sampletype_bad_name = SampleType()

class TestSampleTypeModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([sampletype_1, sampletype_2])

    def test_get_one(self):
        res = get_one(SampleType, 1)
        self.assertIsInstance(res, SampleType)

    def test_get_all(self):
        res = get_all(SampleType)
        self.assertEqual(len(res), 2)
        for r in res:
            self.assertIsInstance(r, SampleType)

    def test_bad_name(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(sampletype_bad_name)

    def test_relationship(self):
        res = get_one(SampleType, 2)
        self.assertIsInstance(res, SampleType)
        self.assertIsInstance(res.samples[0], Sample)

    def test_bad_relationship(self):
        res = get_one(SampleType, 2)
        self.assertIsInstance(res, SampleType)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.sample


# Define Test ScreenPlate
screenplate_1 = ScreenPlate(name='screenplate 1')
screenplate_2 = ScreenPlate(name='screenplate 2')
screenplate_empty = ScreenPlate()
# Diver is allowed to be empty...

class TestScreenPlateModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([screenplate_1, screenplate_2, screenplate_empty])

    def test_get_one(self):
        res = get_one(ScreenPlate, 1)
        self.assertIsInstance(res, ScreenPlate)

    def test_get_all(self):
        res = get_all(ScreenPlate)
        self.assertEqual(len(res), 3)
        for r in res:
            self.assertIsInstance(r, ScreenPlate)

    def test_get_third_empty_attributes(self):
        res = get_one(ScreenPlate, 3)
        self.assertEqual(res.name, None)
        self.assertEqual(res.notes, None)


# Define Test Samples
# and associated relationships
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
sample_bad_name = Sample(collection_number=2, collection_year=2)
sample_bad_number = Sample(name='RL03-003', collection_year=3)
sample_bad_year = Sample(name='RL03-003', collection_number=3)

class TestSampleModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([sample_1, sample_2])

    def test_get_one(self):
        res = get_one(Sample, 1)
        self.assertIsInstance(res, Sample)

    def test_get_all(self):
        res = get_all(Sample)
        self.assertEqual(len(res), 2)
        for r in res:
            self.assertIsInstance(r, Sample)

    def test_bad_name(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(sample_bad_name)

    def test_bad_number(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(sample_bad_number)

    def test_bad_year(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(sample_bad_year)

    def test_relationship(self):
        res = get_one(Sample, 2)
        self.assertIsInstance(res, Sample)
        self.assertIsInstance(res.dive_site, DiveSite)
        self.assertIsInstance(res.divers[0], Diver)
        self.assertIsInstance(res.sample_type, SampleType)
        self.assertIsInstance(res.permit, Permit)
        self.assertIsInstance(res.isolates[0], Isolate)

    def test_bad_relationship(self):
        res = get_one(Sample, 2)
        self.assertIsInstance(res, Sample)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.sample


# Define Test Isolates
# and associated relationships
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
isolate_bad_name = Isolate(color='badname')
isolate_duplicate_name = Isolate(name='isolate 1')
class TestIsolateModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([isolate_1, isolate_2])

    def test_get_one(self):
        res = get_one(Isolate, 1)
        self.assertIsInstance(res, Isolate)

    def test_get_all(self):
        res = get_all(Isolate)
        self.assertEqual(len(res), 2)
        for r in res:
            self.assertIsInstance(r, Isolate)

    def test_bad_name(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(isolate_bad_name)

    def test_duplicate_name(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(isolate_duplicate_name)

    def test_relationship(self):
        res = get_one(Isolate, 2)
        self.assertIsInstance(res, Isolate)
        self.assertIsInstance(res.media, Media)
        self.assertIsInstance(res.sample, Sample)
        self.assertIsInstance(res.extracts[0], Extract)
        self.assertIsInstance(res.stocks[0], IsolateStock)

    def test_bad_relationship(self):
        res = get_one(Isolate, 2)
        self.assertIsInstance(res, Isolate)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.samples


# Define Test Isolates
# and associated relationship
isolate_stock_isolate = Isolate(name='isolate stock isolate')
isolate_stock_1 = IsolateStock(box=1)
isolate_stock_2 = IsolateStock(
    box=2, box_position=1, num_in_stock=1,
    date_added=datetime.date.today(),
    freezethaw=0, volume_ul=1000,
    insert_by=1, insert_date=datetime.datetime.now(),
    isolate=isolate_stock_isolate
)

class TestIsolateStockModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([isolate_stock_1, isolate_stock_2])

    def test_get_one(self):
        res = get_one(IsolateStock, 1)
        self.assertIsInstance(res, IsolateStock)

    def test_get_all(self):
        res = get_all(IsolateStock)
        self.assertEqual(len(res), 2)
        for r in res:
            self.assertIsInstance(r, IsolateStock)

    def test_relationship(self):
        res = get_one(IsolateStock, 2)
        self.assertIsInstance(res, IsolateStock)
        self.assertIsInstance(res.isolate, Isolate)

    def test_bad_relationship(self):
        res = get_one(IsolateStock, 2)
        self.assertIsInstance(res, IsolateStock)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.samples


# Define Test Extracts
# and associated relationship
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
extract_empty = Extract()
# Extract can be empty...

class TestExtractModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([extract_1, extract_2, extract_empty])

    def test_get_one(self):
        res = get_one(Extract, 1)
        self.assertIsInstance(res, Extract)

    def test_get_all(self):
        res = get_all(Extract)
        self.assertEqual(len(res), 3)
        for r in res:
            self.assertIsInstance(r, Extract)

    def test_get_third_empty_attributes(self):
        res = get_one(Extract, 3)
        self.assertEqual(res.number, None)
        self.assertEqual(res.temp, None)

    def test_emprty_name_property(self):
        # Requires extract with library attached
        res = get_one(Extract, 1)
        self.assertIsInstance(res, Extract)
        self.assertEqual(res.name, None)

    def test_name_property(self):
        # Requires extract with library attached
        res = get_one(Extract, 2)
        self.assertIsInstance(res, Extract)
        self.assertEqual(res.name, "RLJVS-0002")

    def test_relationship(self):
        res = get_one(Extract, 2)
        self.assertIsInstance(res, Extract)
        self.assertIsInstance(res.isolate, Isolate)
        self.assertIsInstance(res.media, Media)
        self.assertIsInstance(res.library, Library)
        self.assertIsInstance(res.fractions[0], Fraction)

    def test_bad_relationship(self):
        res = get_one(Extract, 2)
        self.assertIsInstance(res, Extract)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.samples


# Define Test Fractions
# and associated relationship
fraction_extract = Extract(number=1, library=Library(name="TEST", abbrev="TE"))
fraction_1 = Fraction(code="A")
fraction_2 = Fraction(code="B", extract=fraction_extract)
fraction_empty = Fraction()

class TestFractionModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([fraction_1, fraction_2, fraction_empty])

    def test_get_one(self):
        res = get_one(Fraction, 1)
        self.assertIsInstance(res, Fraction)

    def test_get_all(self):
        res = get_all(Fraction)
        self.assertEqual(len(res), 3)
        for r in res:
            self.assertIsInstance(r, Fraction)

    def test_get_third_empty_attributes(self):
        res = get_one(Fraction, 3)
        self.assertIsInstance(res, Fraction)
        self.assertEqual(res.code, None)

    def test_relationship(self):
        res = get_one(Fraction, 2)
        self.assertIsInstance(res, Fraction)
        self.assertIsInstance(res.extract, Extract)

    def test_emprty_name_property(self):
        # Requires extract with library attached
        res = get_one(Fraction, 1)
        self.assertIsInstance(res, Fraction)
        self.assertEqual(res.name, None)

    def test_name_property(self):
        # Requires extract with library attached
        res = get_one(Fraction, 2)
        self.assertIsInstance(res, Fraction)
        self.assertEqual(res.name, "RLTE-0001B")

    def test_bad_relationship(self):
        res = get_one(Fraction, 2)
        self.assertIsInstance(res, Fraction)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.samples


# Define Test Media
# and associated relationship
media_media_recipe = MediaRecipe(ingredient="test", amount=10., unit="mL")
media_1 = Media(name="media 1")
media_2 = Media(name="media 2", notes="test", recipe=[media_media_recipe])
media_bad_name = Media(notes='bad name')

class TestMediaModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([media_1, media_2])

    def test_get_one(self):
        res = get_one(Media, 1)
        self.assertIsInstance(res, Media)

    def test_get_all(self):
        res = get_all(Media)
        self.assertEqual(len(res), 2)
        for r in res:
            self.assertIsInstance(r, Media)

    def test_relationship(self):
        res = get_one(Media, 2)
        self.assertIsInstance(res, Media)
        self.assertIsInstance(res.recipe[0], MediaRecipe)

    def test_bad_relationship(self):
        res = get_one(Media, 2)
        self.assertIsInstance(res, Media)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.samples

    def test_bad_name(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(media_bad_name)


# Define Test MediaRecipe
# and associated relationship
# MediaRecipe REQUIRES Media
mr_media = Media(name="media recipe media")
mediarecipe_1 = MediaRecipe(ingredient="test 1", amount=10., unit="mL", 
    media=mr_media)
mediarecipe_2 = MediaRecipe(ingredient="test 2", amount=10., 
    notes="test", unit="mL", media=mr_media)
mediarecipe_bad = MediaRecipe()

class TestMediaRecipeModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([mediarecipe_1, mediarecipe_1])

    def test_get_one(self):
        res = get_one(MediaRecipe, 1)
        self.assertIsInstance(res, MediaRecipe)

    def test_get_all(self):
        res = get_all(MediaRecipe)
        self.assertEqual(len(res), 2)
        for r in res:
            self.assertIsInstance(r, MediaRecipe)

    def test_relationship(self):
        res = get_one(MediaRecipe, 2)
        self.assertIsInstance(res, MediaRecipe)
        self.assertIsInstance(res.media, Media)

    def test_bad_relationship(self):
        res = get_one(MediaRecipe, 2)
        self.assertIsInstance(res, MediaRecipe)
        # Test a relationship that doesn't exist
        with self.assertRaises(AttributeError):
            res.samples

    def test_bad_media(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(mediarecipe_bad)


# Define Test FractionScreenPlate
# and associated relationship
# FractionScreenPlate REQUIRES Fraction and ScreenPlate
fsp_fraction = Fraction(id=1)
fsp_screenplate = ScreenPlate(id=1,name='fraction screen plate screen plate')
fsp_1 = FractionScreenPlate(id=1, fraction=fsp_fraction, 
                screen_plate=fsp_screenplate, well='1')
fsp_bad_fraction = FractionScreenPlate(screen_plate=fsp_screenplate)
fsp_bad_sp = FractionScreenPlate(fraction=fsp_fraction)

class TestFractionScreenPlateModel(MyTestCase):

    def setUp(self):
        with session_scope() as sess:
            sess.add_all([fsp_1])

    def test_get_one(self):
        res = get_one(FractionScreenPlate, 1)
        self.assertIsInstance(res, FractionScreenPlate)

    def test_get_all(self):
        res = get_all(FractionScreenPlate)
        self.assertEqual(len(res), 1)
        for r in res:
            self.assertIsInstance(r, FractionScreenPlate)

    def test_relationship(self):
        res = get_one(FractionScreenPlate, 1)
        self.assertIsInstance(res, FractionScreenPlate)
        self.assertIsInstance(res.fraction, Fraction)
        self.assertIsInstance(res.screen_plate, ScreenPlate)

    def test_bad_fraction(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(fsp_bad_fraction)

    def test_bad_screenplate(self):
        with self.assertRaises(IntegrityError):
            with session_scope() as sess:
                sess.add(fsp_bad_sp)


if __name__ == '__main__':
    unittest.main()
