# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
import json
import time

#cat logo
IMAGE_URLS = [
    'https://bytebucket.org/snippets/asilva3/dRaMR/raw/5bfc5bd1022ac994124c34a96dab8b64c3c21d3f/cat.jpg?token=242a74d3b8bfad90400f1a8a5eac9ff7a0924d3a',
]

def index():
    image_list = []
    for i, img_url in enumerate(IMAGE_URLS):
        image_list.append(dict(
            url=img_url,
            id=i,
        ))
    return dict(image_list=image_list)

@auth.requires_signature()
def add_cat():
    db.cats.update_or_insert((db.cats.draft_id == request.vars.draft_id), name = request.vars.name, draft_id=request.vars.draft_id, cat_creator=auth.user_id)
    return "ok"

@auth.requires_signature()
def newCatHandle():
    db.cats.update_or_insert((db.cats.draft_id == request.vars.draft_id), name = request.vars.name, draft_id = request.vars.draft_id, cat_creator=auth.user_id)
    return "ok"

@auth.requires_signature()
def update_cat():
    row = db(db.cats.id == request.vars.loc).select().first()
    row.update_record(name = request.vars.name)
    return "ok"

def load_cats():
    """Loads all messages for the user."""
    rows = db(db.cats).select()
    d = {r.id: {'name': r.name, 'fromDB': r.fromDB, 'cat_creator': r.cat_creator, 'draft_id': r.draft_id}
         for r in rows}
    return response.json(dict(cat_dict=d))
    
def add_cat():
    form = SQLFORM(db.cat)

    if form.process().accepted:
        session.flash = T('The data was inserted')
        redirect(URL('default', 'index'))
    elif form.errors:
        session.flash = T('The data was not inserted')

    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
