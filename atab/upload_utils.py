import os, json, uuid, datetime
from py4web import action, request, response, abort, redirect, URL, Field
from .common import db, session, T, cache, authenticated, unauthenticated, auth
from py4web.utils.form import Form, FormStyleBulma, FormStyleDefault
from .settings import APP_NAME, UPLOAD_FOLDER
from pydal.validators import IS_NOT_EMPTY, IS_INT_IN_RANGE, IS_IN_SET, IS_IN_DB


def get_unique_name(orig_name='', default_len=10):
    if orig_name:
       orig_name =  orig_name[:default_len] + '_'
    suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_")
    return "_".join(['at', suffix]) +orig_name + str(uuid.uuid4())

def data2file( data, fnm, mode = 'wb' ):
    with open(fnm, mode) as f:
        f.write( data )
    return fnm

@action("p4wdownload_file", method=["GET", "POST"])
@action.uses(session, db, auth, "p4wdownload_file.html")
def p4wdownload_file():
    tbl = dict(request.query).get('t_', '') 
    if not tbl in db.tables:
        return f"bad table: {tbl}"
    id_ = dict(request.query).get('id_', 1)
    try:
        id = int(id_)
    except:
        id = 1

    import mimetypes
    mimetypes.init()

    r = db[tbl](id)
    if r is None:
        return f"bad id: {id}"

    file_content = '';
    file_path = os.path.join( UPLOAD_FOLDER , r.uniq_file_name )

    try:
         with open(file_path, 'rb') as f:
           file_content= f.read()
    except IOError:
           file_content = f"Error: File {r.orig_file_name} {file_path} does not appear to exist"

    ext = os.path.splitext( r.orig_file_name  )
    tru_ext = ext[1].lower() if len(ext) and len(ext[1]) else ''

    file_type = mimetypes.types_map.get(tru_ext, None)
    view_in_browser =('.pdf','.jpeg','.txt','.jpg','.jpe','.png','.gif','.tif','.tiff','.bmp','.svg','.ico')

    response.headers['Content-Type'] = 'application/octet-stream' if file_type is None else file_type

    response.headers['Content-disposition'] = 'inline; filename=\"%s"' % ( r.orig_file_name)  \
                           if not file_type is None and tru_ext.endswith( view_in_browser  ) \
                           else 'attachment; filename=\"%s"' % ( r.orig_file_name)
    return file_content

@action("p4wdelete_file", method=["GET", "POST"])
@action.uses(session, db, auth, )
#@action.uses(session, db, auth, "p4wdelete_file.html")
def p4wdelete_file():
    tbl = dict(request.query).get('t_', '')
    if not tbl in db.tables:
        return f"bad table: {tbl}"
    id_ = dict(request.query).get('id_', 1)
    try:
        id = int(id_)
    except:
        return f"bad id: {id_}"
    #return f"{tbl} {id}"

    r = db[tbl](id)
    if r is None:
        return f"bad id: {id}"

    file_path = os.path.join( UPLOAD_FOLDER , r.uniq_file_name )

    if os.path.isfile( file_path  ):
         os.remove( file_path  )

    db(db[tbl].id == id  ).delete()
    db.commit()
    redirect(URL('p4wupload_file'))
   

