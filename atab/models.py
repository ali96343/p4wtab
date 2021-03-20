from .common import db, Field
from pydal.validators import *
from py4web.utils.populate import populate
from yatl.helpers import SPAN, H6
import datetime

#
# py4web app, AI-biorex ported 07.01.2021 03:54:13 UTC+3, src: https://github.com/tailwindadmin/admin

#

#import pydal

#from py4web import *
#from apps.myapp.models import db

#if not len( db().select(db.auth_user.id) ):
if not db(db.auth_user).count():
    u1 = {
        "username": "nil",
        "email": "nil@nil.com",
        "password": str(CRYPT()("xyz12345")[0]),
        "first_name": "Nil_first",
        "last_name": "Nil_Last",
    }
 
    u2 = {
        "username": "anil",
        "email": "anil@nil.com",
        "password": str(CRYPT()("xyz12345")[0]),
        "first_name": "Anil_first",
        "last_name": "Anil_Last",
    }


    for e in [u1, u2]: db.auth_user.insert(**db.auth_user._filter_fields(e) )
    db.commit()

db.define_table(
    'test_table',
    Field( 'f0', 'string', label='l0'),
    Field( 'f1', 'string', label='l1'),
    Field( 'f2', 'string', label='l2'),
    )
db.commit()

if not db(db.test_table).count():
    populate(db.test_table, n=50)
    db.commit()

