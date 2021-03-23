from yatl.helpers import A, IMG, DIV, SPAN, XML, P
from py4web.core import Template  # , Reloader
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

from .atab_utils import sql2table, sql2table_grid
from .upload_utils import get_unique_name, data2file, p4wdownload_file, p4wdelete_file


@unauthenticated("index", "index.html")
def index():
    user = auth.get_user()
    message = T("Hello {first_name}".format(**user) if user else "Hello")
    menu = DIV(
               P( "test-demo for sql2table ( SQLTABLE from web2py)"),
               A( "sqltable_grid", _role="button", _href=URL('mytab_grid', ),) ,
               A( "sqltable", _role="button", _href=URL('mytab', ),) ,
               A( "p4wupload_file", _role="button", _href=URL('p4wupload_file', ),) ,
              )
    return dict(message=message, menu=menu)


#---------------------------------------------------------------------------------------------------------

from py4web.utils.form import Form, FormStyleBulma, FormStyleDefault
from .settings import APP_NAME, UPLOAD_FOLDER
from pydal.validators import IS_NOT_EMPTY, IS_INT_IN_RANGE, IS_IN_SET, IS_IN_DB

@action("p4wupload_file", method=["GET", "POST"])
@action.uses("p4wupload_file.html", session, db, T)
def p4wupload_file():

    if not os.path.isdir(UPLOAD_FOLDER):
         return f"bad upload path: {UPLOAD_FOLDER}"

    messages= []
    tbl = 'uploaded_files'
    upload_field = 'image'
    upload_form = Form(
        [
            Field( upload_field, 'upload', requires=IS_NOT_EMPTY(),),
            Field("remark", default='some comment' ),
        ],
        formstyle=FormStyleDefault,
    )

    if upload_form.accepted and hasattr(request, 'files')  :
        bottle_class=request.files.get( upload_field, None)
        if bottle_class:
             image_file = bottle_class.raw_filename
             image_content = bottle_class.file.read()
             uniq_file_name = get_unique_name( )
             fnm2 = os.path.join( UPLOAD_FOLDER , uniq_file_name )
             with open(fnm2, 'wb') as f:
                  f.write( image_content )
             row = dict( orig_file_name = image_file, uniq_file_name=uniq_file_name, remark=upload_form.vars['remark']  )
             if db[tbl].insert(**db[tbl]._filter_fields(row)):
                   db.commit()

    elif upload_form.errors:
        messages.append( f"upload_form has errors: {upload_form.errors}")


    hlinks = ["save", "del"]

    links = [
        lambda tx, r_id: A(
            f"save:[{r_id}]",
            _title='save file to disk',
            _href=URL(f"p4wdownload_file", vars=dict(t_=tx, id_=r_id)),
        ),

        lambda tx, r_id: A(
            f"del:[{r_id}]",
            _title="run p4wdelete_file",
            _href=URL(f"p4wdelete_file", vars=dict(t_=tx, id_=r_id)),
        ),


    ]

    fld_links = {
      #  'id': lambda tx, xx, r_id: A(
      #      f'save[{r_id}]',
      #      _title='save file to disk',
      #      _href=URL(f"p4wdownload_file", vars=dict(t_=tx, x_=xx, id_=r_id)),
      #  ),
        'time': lambda tx, xx, r_id: xx.strftime("%d.%m.%Y %H:%M:%S"), 
    }

    mygrid = sql2table_grid( tbl, db, links=links, hlinks=hlinks, fld_links=fld_links, items_on_page = 2, caller="p4wupload_file", page_d=dict(request.query))
    #mygrid = sql2table( tbl, db, items_on_page = 2, caller="p4wupload_file", page_d=dict(request.query))
    return dict( messages=messages,  upload_form=upload_form, mygrid=mygrid   ) 

#---------------------------------------------------------------------------------------------------------



@action("mytab_grid", method=["GET", "POST"])
@action.uses(Template("mytab_grid.html", delimiters="[[ ]]"), db, session, T)
def mytab_grid():
    def xfunc(tt, rr_id):
        return f"{tt}:{rr_id}-ok"

    hlinks = ["+img", "+r_id", "+xfunc"]
    links = [
        lambda tx, r_id: A(
            IMG(_width="30px", _height="30px", _src=URL("static/favicon.ico")),
            _title="run some_func",
            _href=URL(f"some_func", vars=dict(t_=tx, id_=r_id)),
        ),
        lambda tx, r_id: A(
            f"myf2-id:[{r_id}]",
            _title="run some3_func",
            _href=URL(f"some3_func", vars=dict(t_=tx, id_=r_id)),
        ),
        lambda tx, r_id: A(
            xfunc(tx, r_id),
            _title="run some3_func",
            _href=URL(f"some3_func", vars=dict(t_=tx, id_=r_id)),
        ),
    ]

    def yfunc(xx, rr_id):
        xx = xx[:10]
        if rr_id % 2 == 0:
            return SPAN(xx, _style="color:red")
        else:
            return SPAN(xx, _style="color:green")

    def zfunc(xx, rr_id):
        xx = xx[:10]
        if rr_id % 2 == 0:
            return SPAN(xx, _style="color:blue")
        else:
            return SPAN(xx, _style="color:brown")

    def title_func( xx, rr_id  ):
        return xx

    fld_links = {
        # by field num
        1: lambda tx, xx, r_id: A(
            yfunc(xx, r_id),
            _title= title_func( xx, r_id ), 
            _href=URL(f"some4_func", vars=dict(t_=tx, x_=xx, id_=r_id)),
        ),
        # by field name 
        'f2': lambda tx, xx, r_id: A(
            zfunc(xx, r_id),
            _title= title_func( xx, r_id ), 
            _href=URL(f"some4_func", vars=dict(t_=tx, x_=xx, id_=r_id)),
        ),
    }

    mytab = sql2table_grid(
        "test_table",
        db,
        page_d=dict(request.query),
        caller="mytab_grid",
        links=links,
        hlinks=hlinks,
        fld_links=fld_links,
        csv = False,
    )

    return dict(message="test sql2table_grid", mytab=mytab)


@action("some_func", method=["GET", "POST"])
def some_func():
    args = repr(dict(request.query))
    return f"some_func: {args}"


@action("some2_func", method=["GET", "POST"])
def some_func():
    args = repr(dict(request.query))
    return f"some2_func: {args}"


@action("some3_func", method=["GET", "POST"])
def some_func():
    args = repr(dict(request.query))
    return f"some3_func: {args}"


@action("some4_func", method=["GET", "POST"])
def some_func():
    args = repr(dict(request.query))
    return f"some4_func: {args}"
