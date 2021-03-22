from py4web import action, request, abort, redirect, URL
from yatl.helpers import A, IMG, DIV, SPAN, XML, P
from py4web.core import Template  # , Reloader

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


@unauthenticated("index", "index.html")
def index():
    user = auth.get_user()
    message = T("Hello {first_name}".format(**user) if user else "Hello")
    menu = DIV(
               P( "test-demo for sql2table ( SQLTABLE from web2py)"),
               A( "sqltable_grid", _role="button", _href=URL('mytab_grid', ),) ,
               A( "sqltable", _role="button", _href=URL('mytab', ),) ,
               A( "myupload_file", _role="button", _href=URL('myupload_file', ),) ,
              )
    return dict(message=message, menu=menu)


@action("mytab", method=["GET", "POST"])
@action.uses(Template("mytab.html", delimiters="[[ ]]"), db, session, T)
def mytab():

    mytab = sql2table("test_table", db, caller="mytab", pg_dict=dict(request.query))

    return dict(message="test sql2table", mytab=mytab)

@action("myupload_file", method=["GET", "POST"])
@action.uses(Template("myupload_file.html", delimiters="[[ ]]"), db, session, T)
def myupload_file():

    mytab = sql2table("test_table", db, caller="myupload_file", pg_dict=dict(request.query))

    #return dict(message="test sql2table", mytab=mytab)

@action("mytab_grid", method=["GET", "POST"])
@action.uses(Template("mytab_grid.html", delimiters="[[ ]]"), db, session, T)
def mytab_grid():
    def xfunc(tt, rr_id):
        return f"{tt}:{rr_id}-ok"

    hlinks = ["+img", "+f_id", "+xfunc"]
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
        1: lambda tx, xx, r_id: A(
            yfunc(xx, r_id),
            _title= title_func( xx, r_id ), 
            _href=URL(f"some4_func", vars=dict(t_=tx, x_=xx, id_=r_id)),
        ),
        3: lambda tx, xx, r_id: A(
            zfunc(xx, r_id),
            _title= title_func( xx, r_id ), 
            _href=URL(f"some4_func", vars=dict(t_=tx, x_=xx, id_=r_id)),
        ),
    }

    mytab = sql2table_grid(
        "test_table",
        db,
        pg_dict=dict(request.query),
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
