import datetime
import unittest

from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm.exc import NoResultFound
from tests.myTestCase import MyTestCase

from api.db import Session
from api.models import (Diver, DiveSite, Extract, Fraction,
                        FractionScreenPlate, Isolate, IsolateStock, Library,
                        Media, MediaRecipe, Permit, Sample, SampleType,
                        ScreenPlate, get_all, get_one)

#########################################
# Tests for entities without foreign keys
#########################################

# Define Test Divers
diver_1 = Diver(first_name='Test', last_name='Case1')
diver_2 = Diver(first_name='Test', last_name='Case2')
# Diver is allowed to be empty...

class TestDiverModel(MyTestCase):

    def test_get_all_empty(self):
        res = get_all(Diver)
        self.assertEqual(res, [])

    def test_get_one_empty(self):
        with self.assertRaises(NoResultFound):
            get_one(Diver, 1)
    
    def test_add_one(self):
        Session.add(diver_1)
        res = get_one(Diver, 1)
        self.assertIsInstance(res, Diver)

    def test_add_multiple(self):
        Session.add_all([diver_1, diver_2])
        res = get_all(Diver)
        self.assertEqual(len(res), 2)

    def test_get_one(self):
        Session.add(diver_1)
        res = get_one(Diver, 1)
        self.assertEqual(res, diver_1)

    def test_get_all(self):
        Session.add_all([diver_1, diver_2])
        res = get_all(Diver)
        self.assertListEqual(res, [diver_1, diver_2])


# Define Test DiveSites
divesite_1 = DiveSite(name='test site 1', lat=1.1, lon=0.0)
divesite_2 = DiveSite(name='test site 2', lat=2.2, lon=0.0)
divesite_bad_lat = DiveSite(name='bad lat', lon=0.0)
divesite_bad_lon = DiveSite(name='bad lon', lat=0.0)

class TestDiveSiteModel(MyTestCase):

    def test_get_all_empty(self):
        res = get_all(DiveSite)
        self.assertEqual(res, [])

    def test_get_one_empty(self):
        with self.assertRaises(NoResultFound):
            get_one(DiveSite, 1)
    
    def test_add_one(self):
        Session.add(divesite_1)
        res = get_one(DiveSite, 1)
        self.assertIsInstance(res, DiveSite)

    def test_add_multiple(self):
        Session.add_all([divesite_1, divesite_2])
        res = get_all(DiveSite)
        self.assertEqual(len(res), 2)

    def test_get_one(self):
        Session.add(divesite_1)
        res = get_one(DiveSite, 1)
        self.assertEqual(res, divesite_1)

    def test_get_all(self):
        Session.add_all([divesite_1, divesite_2])
        res = get_all(DiveSite)
        self.assertListEqual(res, [divesite_1, divesite_2])

    def test_bad_lat(self):
        with self.assertRaises(IntegrityError):
            Session.add(divesite_bad_lat)
            _ = get_one(DiveSite, 1)

    def test_bad_lon(self):
        with self.assertRaises(IntegrityError):
            Session.add(divesite_bad_lon)
            _ = get_one(DiveSite, 1)


# Define Test Library
library_1 = Library(name='library 1', abbrev='l1')
library_2 = Library(name='library 2', abbrev='l2')
library_bad_abbrev = Library(name='bad abbrev')
library_bad_name = Library(abbrev='bn')

class TestLibrary(MyTestCase):

    def test_get_all_empty(self):
        res = get_all(Library)
        self.assertEqual(res, [])

    def test_get_one_empty(self):
        with self.assertRaises(NoResultFound):
            get_one(Library, 1)
    
    def test_add_one(self):
        Session.add(library_1)
        res = get_one(Library, 1)
        self.assertIsInstance(res, Library)

    def test_add_multiple(self):
        Session.add_all([library_1, library_2])
        res = get_all(Library)
        self.assertEqual(len(res), 2)

    def test_get_one(self):
        Session.add(library_1)
        res = get_one(Library, 1)
        self.assertEqual(res, library_1)

    def test_get_all(self):
        Session.add_all([library_1, library_2])
        res = get_all(Library)
        self.assertListEqual(res, [library_1, library_2])

    def test_bad_name(self):
        with self.assertRaises(IntegrityError):
            Session.add(library_bad_name)
            _ = get_one(Library, 1)

    def test_bad_abbrev(self):
        with self.assertRaises(IntegrityError):
            Session.add(library_bad_abbrev)
            _ = get_one(Library, 1)


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
permit_noname = Permit(iss_auth='jvansan')
permit_noissauth = Permit(name='No Issuing Auth')
permit_datetime = Permit(name='Datetime permit', iss_auth='jvansan',
                            start_date=datetime.datetime.today())
permit_string_datetime = Permit(name='Datetime permit', iss_auth='jvansan',
                                   start_date="2019-08-27")

class TestPermitModel(MyTestCase):

    def test_get_all_empty(self):
        res = get_all(Permit)
        self.assertEqual(res, [])

    def test_get_one_empty(self):
        with self.assertRaises(NoResultFound):
            get_one(Permit, 1)

    def test_add_one(self):
        Session.add(permit_1)
        res = get_one(Permit, 1)
        self.assertIsInstance(res, Permit)

    def test_add_multiple(self):
        Session.add_all([permit_1, permit_2])
        res = get_all(Permit)
        self.assertEqual(len(res), 2)

    def test_get_one(self):
        Session.add(permit_1)
        res = get_one(Permit, 1)
        self.assertEqual(res, permit_1)

    def test_get_all(self):
        Session.add_all([permit_1, permit_2])
        res = get_all(Permit)
        self.assertListEqual(res, [permit_1, permit_2])

    def test_bad_name(self):
        with self.assertRaises(IntegrityError):
            Session.add(permit_noname)
            _ = get_one(Permit, 1)

    def test_bad_issauth(self):
        with self.assertRaises(IntegrityError):
            Session.add(permit_noissauth)
            _ = get_one(Permit, 1)

    def test_datetime_string(self):
        if Session.bind.dialect.name == 'mysql':
            with self.assertRaises(NoResultFound):
                with self.assertWarns(Warning):
                    Session.add(permit_string_datetime)
                    _ = get_one(Permit, 1)
        elif Session.bind.dialect.name == 'sqlite':
            with self.assertRaises(StatementError):
                Session.add(permit_string_datetime)
                res = get_one(Permit, 1)
                # self.assertEqual(len(res), 1)



# Define Test SampleType
sampletype_1 = SampleType(name='sample type 1')
sampletype_2 = SampleType(name='sample type 2')
sampletype_bad_name = SampleType()

class TestSampleTypeModel(MyTestCase):

    def test_get_all_empty(self):
        res = get_all(SampleType)
        self.assertEqual(res, [])

    def test_get_one_empty(self):
        with self.assertRaises(NoResultFound):
            get_one(SampleType, 1)
    
    def test_add_one(self):
        Session.add(sampletype_1)
        res = get_one(SampleType, 1)
        self.assertIsInstance(res, SampleType)

    def test_add_multiple(self):
        Session.add_all([sampletype_1, sampletype_2])
        res = get_all(SampleType)
        self.assertEqual(len(res), 2)

    def test_get_one(self):
        Session.add(sampletype_1)
        res = get_one(SampleType, 1)
        self.assertEqual(res, sampletype_1)

    def test_get_all(self):
        Session.add_all([sampletype_1, sampletype_2])
        res = get_all(SampleType)
        self.assertListEqual(res, [sampletype_1, sampletype_2])

    def test_bad_name(self):
        with self.assertRaises(IntegrityError):
            Session.add(sampletype_bad_name)
            _ = get_one(SampleType, 1)


# Define Test ScreenPlate
screenplate_1 = ScreenPlate(name='screenplate 1')
screenplate_2 = ScreenPlate(name='screenplate 2')
# Can have empty screenplate...

class TestScreenPlateModel(MyTestCase):

    def test_get_all_empty(self):
        res = get_all(ScreenPlate)
        self.assertEqual(res, [])

    def test_get_one_empty(self):
        with self.assertRaises(NoResultFound):
            get_one(ScreenPlate, 1)
    
    def test_add_one(self):
        Session.add(screenplate_1)
        res = get_one(ScreenPlate, 1)
        self.assertIsInstance(res, ScreenPlate)

    def test_add_multiple(self):
        Session.add_all([screenplate_1, screenplate_2])
        res = get_all(ScreenPlate)
        self.assertEqual(len(res), 2)

    def test_get_one(self):
        Session.add(screenplate_1)
        res = get_one(ScreenPlate, 1)
        self.assertEqual(res, screenplate_1)

    def test_get_all(self):
        Session.add_all([screenplate_1, screenplate_2])
        res = get_all(ScreenPlate)
        self.assertListEqual(res, [screenplate_1, screenplate_2])


#########################################
# Tests for entities with foreign keys
#########################################
# Define Test SampleType
# And associated relationships
sample_dive_site=DiveSite(name='Sample diversite', lat=1.1, lon=0.0)
diver_s1=Diver(first_name='Test', last_name='Diver1')
diver_s2=Diver(first_name='Test', last_name='Diver2')
sample_sample_type=SampleType(name='Sample sample type')
sample_permit=Permit(name='sample permit', iss_auth='jvansan')
sample_isolate=Isolate(name='sample isolate')
sample_1 = Sample(name='RL01-001', collection_number=1, collection_year=1)
# sample 2 get all attributes for testing
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

    def test_get_all_empty(self):
        res = get_all(Sample)
        self.assertEqual(res, [])

    def test_get_one_empty(self):
        with self.assertRaises(NoResultFound):
            get_one(Sample, 1)
    
    def test_add_one(self):
        Session.add(sample_1)
        res = get_one(Sample, 1)
        self.assertIsInstance(res, Sample)

    def test_add_multiple(self):
        Session.add_all([sample_1, sample_2])
        res = get_all(Sample)
        self.assertEqual(len(res), 2)

    def test_get_one(self):
        Session.add(sample_1)
        res = get_one(Sample, 1)
        self.assertEqual(res, sample_1)

    def test_get_all(self):
        Session.add_all([sample_1, sample_2])
        res = get_all(Sample)
        self.assertListEqual(res, [sample_1, sample_2])

    def test_bad_name(self):
        with self.assertRaises(IntegrityError):
            Session.add(sample_bad_name)
            _ = get_one(Sample, 1)

    def test_bad_num(self):
        with self.assertRaises(IntegrityError):
            Session.add(sample_bad_number)
            _ = get_one(Sample, 1)

    def test_bad_year(self):
        with self.assertRaises(IntegrityError):
            Session.add(sample_bad_year)
            _ = get_one(Sample, 1)


# isolate_1=Isolate(name='test isolate 1')
# isolatestock_1=IsolateStock(box=1)
# extract_1=Extract(number=1)
# fraction_1=Fraction(code='A')
# media_1=Media()
# mediarecipe_1=MediaRecipe()
# fractionscreenplate_1=FractionScreenPlate()

if __name__ == '__main__':
    unittest.main()
