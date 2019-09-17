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
        else:
            result = row2dict(row)
        # Serialize relationships as lists of links
        for rel in row.__mapper__.relationships.keys():
            try:
                key = ENDPOINT_MAP[rel]
            except KeyError:
                key = rel
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
                    else:
                        result[key]["embedded"] = [row2dict(x) for x in r if x]
    return result


def jsonify_sqlalchemy(res, embed=[]):
    if not isinstance(res, list):
        return serialize_row(res, embed=embed) 
    return [serialize_row(r, embed=embed) for r in res]
