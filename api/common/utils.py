import datetime
import os
from decimal import Decimal

from flask import abort, jsonify

from api.common.exc import ValidationException
from api.common.sql_models import Base
from api.config import app_config
from api.models import (Diver, DiveSite, Library, Permit,
                        Sample, SampleType, ScreenPlate)

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
    # 'isolate': 
    # 'isolate_stock': 
    # 'extract': 
    # 'fraction': 
    # 'media': 
    # 'media_recipe': 
    'library': Library,
    'screen_plate': ScreenPlate,
    # 'fraction_screen_plate': 
}

TABLE_MAP = {v:k for k,v in ENDPOINT_MAP.items()}

CONF = app_config[os.getenv('FLASK_ENV', 'development')]
BASE_URL = f"http://{CONF.SERVER_NAME}"

def validate_embedding(embed, relationships, endpoint):
    if not embed:
        return []
    embed_split = embed.split(',')
    for e in embed_split:
        if e not in relationships:
            raise ValidationError(f'{e} - not related to {endpoint}')
    return embed_split

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
    return result


def serialize_row(row, embed):
    self_ = f"/{ENDPOINT_MAP[row.__table__.name]}/{row.id}"
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
        result[key] = {"links":[f"{BASE_URL+self_}/{key}/{x.id}" for x in r if x]}
        if key in embed:
            result[key]["embedded"] = [row2dict(x) for x in r if x]
        
    return result


# Simple serialization - deprecate in favour of JSON:API spec
def jsonify_sqlalchemy(res, embed=[]):
    # ensure result is list for consistent API consumption
    if not isinstance(res, list):
        res = [res]
    return [serialize_row(r, embed=embed) for r in res]
