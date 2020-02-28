import datetime
import os
from decimal import Decimal

from flask import abort, jsonify

from api.common.exc import ValidationException
from api.common.sql_models import Base
from api.config import app_config
from api.common.sql_models import (Diver, DiveSite, Extract, Fraction,
                                   FractionScreenPlate, Isolate, IsolateStock,
                                   Library, Media, MediaRecipe, Permit, Sample,
                                   SampleType, ScreenPlate)

ENDPOINT_MAP = {
    'sample': 'samples',
    'sample_type': 'sampletypes',
    'dive_site': 'divesites',
    'diver': 'divers',
    'permit': 'permits',
    'isolate': 'isolates',
    'isolate_stock': 'isolatestocks',
    'extract': 'extracts',
    'fraction': 'fractions',
    'media': 'media',
    'media_recipe': 'mediarecipes',
    'library': 'libraries',
    'screen_plate': 'screenplates',
    'fraction_screen_plate': 'fractionscreenplates'
}

MODEL_MAP = {
    'sample': Sample,
    'sample_type': SampleType,
    'dive_site': DiveSite,
    'diver': Diver,
    'permit': Permit,
    'isolate': Isolate,
    'isolate_stock': IsolateStock,
    'extract': Extract,
    'fraction': Fraction,
    'media': Media,
    'media_recipe': MediaRecipe,
    'library': Library,
    'screen_plate': ScreenPlate,
    'fraction_screen_plate': FractionScreenPlate
}

TABLE_MAP = {v:k for k,v in ENDPOINT_MAP.items()}

CONF = app_config[os.getenv('FLASK_ENV', 'development')]
BASE_URL = f"http://{CONF.BASE_URL}:5000"


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_embedding(embed):
    if not embed:
        return []
    return embed.split(',')


def validate_embed(Doa, embed):
    relationships = get_relationships(Doa)
    for e in embed:
        if " " in e:
            e_split = e.split(' ')
            e1 = e_split[0]
            e2s = e_split[1:]
            sub_Doa = MODEL_MAP[TABLE_MAP[e1]]
            sub_relationships = get_relationships(sub_Doa)
            if e1 not in relationships or any(e2 not in sub_relationships for e2 in e2s):
                return False
            continue
        if e not in relationships:
            return False
    return True


def get_relationships(Doa):
    assert issubclass(Doa, Base)
    relationships = []
    keys = Doa.__mapper__.relationships.keys()
    for k in keys:
        try:
            key = ENDPOINT_MAP[k]
        except KeyError:
            key = k
        relationships.append(key)
    return relationships


def row2dict(row):
    result = {}
    if isinstance(row, Extract):
        extra = ['name']
    else:
        extra = []
    # Serialize table without foreign keys
    for c in row.__table__.columns:
        # Remove metadata fields
        if c.name in ['insert_by', 'insert_date']:
            continue
        r = getattr(row, c.name)
        # Handle all relationships separately
        if c.foreign_keys:
            continue
        elif isinstance(r, Decimal):
            result[c.name] = float(r)
        elif isinstance(r, datetime.date):
            result[c.name] = r.isoformat()
        else:
            result[c.name] = r
    for e in extra:
        r = getattr(row, e)
        result[e] = r
    return result


def media2dict(row):
    result = {}
    # Serialize table without foreign keys
    for c in row.__table__.columns:
        r = getattr(row, c.name)
        result[c.name] = r
    recipe=[]
    for i in row.recipe:
        recipe.append({
            "ingredient": i.ingredient,
            "amount": i.amount,
            "unit": i.unit,
            "notes": i.notes
        })
    result['recipe'] = recipe
    return result


def fraction2dict(row):
    result = {}
    # Serialize table without foreign keys
    for c in row.__table__.columns:
        r = getattr(row, c.name)
        result[c.name] = r
    # Extra name attribute
    result['name'] = row.name    
    screen_plates = []
    for i in row.fraction_screen_plates:
        screen_plates.append({
            "name": i.screen_plate.name,
            "htcb_name": i.screen_plate.htcb_name,
            "plate_format": i.screen_plate.well_format,
            "well": i.well,
            "notes": i.notes
        })
    result['screen_plates'] = screen_plates
    return result


def isolate2dict(row):
    result = row2dict(row)
    result['stocks'] = [row2dict(s) for s in row.stocks]
    return result


def serialize_row(row, embed):
    self_ = f"/{ENDPOINT_MAP[row.__table__.name]}/{row.id}"
    # Check for nested embedding
    nested_embed = {}
    parsed_embed = []
    for e in embed:
        if " " in e:
            e_split = e.split(' ')
            parsed_embed.append(e_split[0])
            nested_embed[e_split[0]] = e_split[1:]
        else:
            parsed_embed.append(e)

    # Separate media to serialize so that recipe is included
    if isinstance(row, Media):
        result = media2dict(row)
    else:
         # Separate fraction to serialize so that screen_plate data is included
        if isinstance(row, Fraction):
            result = fraction2dict(row)
        elif isinstance(row, Isolate):
            result = isolate2dict(row)
        else:
            result = row2dict(row)
        # Serialize relationships as lists of links
        for rel in row.__mapper__.relationships.keys():
            try:
                key = ENDPOINT_MAP[rel]
            except KeyError:
                key = rel
            # Pass over stocks
            if key == "stocks":
                continue
            r = getattr(row, rel)
            if not isinstance(r, list):
                r = [r]
            # result[key] = {"links":[f"{BASE_URL}/api/v1/{key}/{x.id}" for x in r if x]}
            result[key] = {"links":[f"/api/v1/{key}/{x.id}" for x in r if x]}
            if key in parsed_embed:
                if nested_embed.get(key):
                    result[key]["embedded"] = [serialize_row(x, embed=nested_embed.get(key)) for x in r if x]
                else:
                    if key == "fractions":
                        result[key]["embedded"] = [fraction2dict(x) for x in r if x]
                    elif key == "isolates":
                        result[key]["embedded"] = [isolate2dict(x) for x in r if x]
                    else:
                        result[key]["embedded"] = [row2dict(x) for x in r if x]
    return result


def jsonify_sqlalchemy(res, embed=[]):
    if not isinstance(res, list):
        return serialize_row(res, embed=embed) 
    return [serialize_row(r, embed=embed) for r in res]


def validate_input(Doa, data):
    columns = set([x.name for x in Doa.__table__.columns])
    required_columns = set([x.name for x in Doa.__table__.columns if not x.nullable])
    # Allow for tables without an id field
    required_columns.discard("id")
    if Doa == MediaRecipe:
        required_columns.discard("media_id")

    inputs = set(data.keys())
    # Check all inputs are registered kwargs
    # and that there are no missing required keys
    if (not inputs.issubset(columns) or 
        not inputs.issuperset(required_columns)):
        return False
    return True


def validate_isolate_input(data):
    """Isolate Data
    
    Args:
    {
        name: "STRING", # REQUIRED
        color: "STRING",
        morphology: "STRING",
        sequence: "STRING",
        sequence_dir: "STRING",
        sequence_file: "STRING",
        notes: "STRING",
        insert_by: INT,
        insert_date: "DATESTRING",
        media_id: INT,
        sample_id: INT,
        stock: {
            box: INT,
            box_position: INT,
            num_in_stock: INT,
            date_added: "DATESTRING"
        }
    }
    """
    data_copy = data.copy()
    stock = data_copy.pop("stock")
    if not stock:
        return False
    return validate_input(Isolate, data_copy)


def validate_sample_input(data):
    """
    Sample Data:
    {
        name: "STRING", # REQUIRED
        collection_number: INT, # REQUIRED
        collection_year: INT, # REQUIRED
        collection_date: "DATESTRING ex.'2014-07-09'",
        color: "STRING",
        depth_ft: FLOAT,
        genus_species: "STRING",
        notes: "STRING",
        insert_by: INT, 
        insert_date: "DATESTRING", # DEFAULT = UTC.now
        dive_site_id: INT, # REQUIRED
        diver_ids: [INT, INT, ...],
        sample_type_id: INT,
        permit_id: INT
    }
    """
    # Make copy of data so not actually popping real data
    data_copy = data.copy()
    diver_ids = data_copy.pop("diver_ids", [])
    if not isinstance(diver_ids, list):
        return False
    return validate_input(Sample, data_copy)

def validate_media_input(data):
    """
    Sample data:
    {
        "media": {
            "name": "TES" # REQUIRED,
            "notes: "Test media"
        },
        "recipe": [
            {
                "ingredient": "test1", # REQUIRED
                "amount": 1.0, # REQUIRED
                "unit": "amu", # REQUIRED
                "notes": "Test ingredient"
            }, ...
        ]
    }
    """
    media_data = data.get("media")
    recipe_data = data.get("recipe")
    print(media_data)
    print(recipe_data)
    # First check data was provided
    if not (media_data and recipe_data):
        return False
    return validate_input(Media, media_data) and all(validate_input(MediaRecipe, x) for x in recipe_data)

# Flat JSON string for testing
# '{"media":{"name":"TES","notes":"Test media"},"recipe":[{"ingredient":"test1","amount":1.0,"unit":"amu","notes":"Test ingredient"}]}'

def filter_empty_strings(data):
    def my_filter(d_tup):
        val = d_tup[1]
        if isinstance(val, str):
            return bool(val)
        else:
            return True
    return dict(filter(my_filter, data.items()))
