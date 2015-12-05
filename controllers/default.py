# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
from gluon.dal import Rows, Row
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

def listings():
    loggedIn = True
    if auth.user_id is None:
        loggedIn = False
    return dict(loggedIn=loggedIn, user_id=auth.user_id)

@auth.requires_signature()
def update_cat():
    row = db(db.cat.id == request.vars.loc).select().first()
    row.update_record(Name = request.vars.Name)
    return "ok"

def load_cats():
    """Loads all messages for the user."""
    rows = db(db.cat).select()

    place = str(request.vars.Place)
    breed = str(request.vars.Breed)
    Age = str(request.vars.Age)
    #str Rating = request.vars.Rating
    Price = str(request.vars.Price)

    sqlArray = []
    if place == "All States":
        place = ""
    else:
        place = "Place="+"'"+place+"'"
        sqlArray.append(place)

    if Age == "All Ages":
        Age = ""
    else:
        Age = "Age="+"'"+Age+"'"
        sqlArray.append(Age)

    # if Rating = "All Ratings":
    #     Rating = ''
    # else:
    #     Rating = Rating + ' and '
    #
    #if Price = "All Prices":
    #     Price = ''
    #else:
    #     Price = Price + ' and '

    if breed == "All Breeds":
        breed = ""
    else:
        breed = "Breed="+"'"+breed+"'"
        sqlArray.append(breed)

    s = ""
    for val in sqlArray:
        if sqlArray.index(val) != len(sqlArray)-1:
            s = s + val + " and "
        else:
            s = s + val

    # print str
    #
    # sql = place + Age + breed

    print "SELECT * FROM cat WHERE " + s +";"
    if s == "":
        rows = db(db.cat).select()
        print rows
        print
        d = {r.id: {'Name': r.Name, 'Human': r.Human, 'Breed':r.Breed, 'Place': r.Place, 'Age': r.Age}
            for r in rows}
        print d
    else:
        rows = db.executesql("SELECT * FROM cat WHERE " + s +";", as_dict=True)
        print rows
        print
        d = {r['id']: {'Name': r['Name'], 'Human': r['human'], 'Breed': r['Breed'], 'Place': r['place'], 'Age': r['Age']}
             for r in rows}
        print d




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
