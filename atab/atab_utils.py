from yatl.helpers import A, I, SPAN, XML, DIV, P, TABLE, THEAD, TR, TD, TBODY, H6, IMG
from py4web import URL


def sql2table(tbl, db, pg_dict={}, items_on_page=5, caller="index"):
    # caller = 'sql2table'
    if not tbl in db.tables:
        return f"unknown tbl: {tbl}"

    try:
        pg = int(pg_dict.get("page", 1))
    except ValueError:
        pg = 1

    table_items = len(db(db[tbl].id > 0).select())
    if items_on_page > table_items:
        items_on_page = table_items

    max_pages, rem = divmod( table_items, items_on_page  )
    if rem : max_pages += 1

    limitby = (pg - 1) * items_on_page, pg * items_on_page
    rows = db(db[tbl].id > 0).select(orderby=db[tbl].id, limitby=limitby)

    headers = [db[tbl][f].label for f in db[tbl].fields]


    return DIV(
        SPAN(f"{tbl}", _style="color:red"),
        SPAN(f"; {table_items} rows, {items_on_page} items_on_page"),
        DIV(
            A(
                "prev",
                _role="button",
                _href=URL(caller, vars=dict(page=pg - 1 if pg > 1 else pg)),
            ) if pg > 1 else A( '!', _role = 'button',  _style="background-color:lightgray;color:black;" ),
            A(
                "next",
                _role="button",
                _href=URL(caller, vars=dict(page=pg + 1 if pg < max_pages else pg)),
            ) if pg < max_pages else A( '!', _role = 'button', _style="background-color:lightgray;color:black;" ),
        ),
        TABLE(
            THEAD(TR(*[TD(H6(header)) for header in headers])),
            TBODY(*[TR(*[TD(row[field]) for field in rows.colnames]) for row in rows]),
        ),
    )


def sql2table_grid(
    tbl,
    db,
    pg_dict={},
    items_on_page=13,
    caller="index",
    csv=False,
    links=[],
    hlinks=[],
    fld_links={},
):

    if not tbl in db.tables:
        return f"unknown tbl: {tbl}"

    try:
        pg = int(pg_dict.get("page", 1))
    except ValueError:
        pg = 1

    table_items = len(db(db[tbl].id > 0).select())
    if items_on_page > table_items:
        items_on_page = table_items

    max_pages, rem = divmod( table_items, items_on_page  )
    if rem : max_pages += 1

    limitby = (pg - 1) * items_on_page, pg * items_on_page
    rows = db(db[tbl].id > 0).select(orderby=db[tbl].id, limitby=limitby)


    ij_start = -len(links)
    ff = [f for f in db[tbl].fields]
    hh = [db[tbl][f].label for f in ff]

    def h_func(x, jj):
        if jj < 0:
            if len(hlinks) >= -jj:
                return hlinks[len(hlinks) + jj]
            return "act"
        return f"{x}"

    def r_func(x, ii, r, t):
        if ii < 0:
            if len(links) >= -ii:
                return links[len(links) + ii](t, r.id)
            return "unk"
        if ii in fld_links:
            return fld_links[ii](t, x, r.id)
        return f"{x}"

    return DIV(
        SPAN(f"{tbl}", _style="color:red"),
        SPAN(f"; {table_items} rows, {items_on_page} items_on_page"),
        DIV(
            A(
                "csv",
                _role="button",
                _title="table to csv file",
                _href=URL("some_func", vars=dict(t_=tbl, c="a")),
            ),
            A(
                "xls",
                _role="button",
                _title="table to xls file",
                _href=URL("some_func", vars=dict(t_=tbl, c="b")),
            ),
        )
        if csv
        else "",
        DIV(
            A(
                "prev",
                _role="button",
                _href=URL(caller, vars=dict(page=pg - 1 if pg > 1 else pg)),
            ) if pg > 1 else A( '!', _role = 'button', _style="background-color:lightgray;color:black;" ) ,
            A(
                "next",
                _role="button",
                _href=URL(caller, vars=dict(page=pg + 1 if pg < max_pages else pg)),
            ) if pg < max_pages else A( '!', _role = 'button', _style="background-color:lightgray;color:black;"  ) ,
        ),
        TABLE(
            THEAD(TR(*[TD(H6(h_func(hh[j], j))) for j in range(ij_start, len(hh))])),
            TBODY( *[ TR( *[ TD(r_func(row[ff[i]], i, row, tbl)) for i in range(ij_start, len(ff)) ])
                    for row in rows ]
            ),
        ),
    )

# ----------------------------------------------------------------------

