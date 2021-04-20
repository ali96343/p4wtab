from py4web.core import Template  # , Reloader
from yatl.helpers import A, I, SPAN, XML, DIV, P
from py4web import action, request, response, abort, redirect, URL, Field


import os, json, uuid, datetime
from py4web.core import bottle

from .common import (
    db,
    session,
    T,
    cache,
    auth,
    logger,
    authenticated,
    unauthenticated,
    flash,
)

from .atab_utils import mytab_grid
from .upload_utils import p4wupload_file
from .tlist_utils import tlist 

from yatl.helpers import A
from . common import db, session, T, cache, auth , url_signer 





@unauthenticated("index", "index.html")
def index():
    user = auth.get_user()
    message = T("Hello {first_name}".format(**user) if user else "Hello")
    menu = DIV(
               P( "test-demo for sql2table ( SQLTABLE from web2py)"),
               A( "sql2table", _role="button", _href=URL('mytab_grid', signer=url_signer   ),) ,
               A( "p4wupload_file", _role="button", _href=URL('p4wupload_file', signer=url_signer ),) ,
               A( "tlist", _role="button", _href=URL('tlist', signer=url_signer ),) ,
              )
    return dict(message=message, menu=menu)

#from yatl.helpers import UL, LI
#def MENU(items):
#      return UL(*[LI(name,, _href=link) if not other else LI(MENU(other)) for name, link, other in items])

