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


@unauthenticated("index", "index.html")
def index():
    user = auth.get_user()
    message = T("Hello {first_name}".format(**user) if user else "Hello")
    menu = DIV(
               P( "test-demo for sql2table ( SQLTABLE from web2py)"),
               A( "sqltable_grid", _role="button", _href=URL('mytab_grid', ),) ,
               A( "p4wupload_file", _role="button", _href=URL('p4wupload_file', ),) ,
              )
    return dict(message=message, menu=menu)
