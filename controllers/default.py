# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
from gluon.dal import Rows, Row
import json
import time

def index():
    return dict()

def add_cat():
    form = SQLFORM(db.cat)
    if form.process().accepted:
        session.flash = T('Your cat was add!')
        redirect(URL('default', 'listings'))
    elif form.errors:
        session.flash = T('Meow website is not working, please try again!')

    return dict(form=form)

def cat_details():
    row = db(db.cat.id == request.args(0)).select()
    return dict(details=row)

def rent_cat():
    print request.args(0)
    db(db.cat.id == request.args(0)).update(Rented=True)
    redirect(URL('default', 'listings'))
    return ""

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

def user_profile():
    loggedIn = True
    if auth.user_id is None:
        loggedIn = False
    return dict(loggedIn=loggedIn, user_id=auth.user_id)

def user_cats():
    id = auth.user_id
    info = db(db.auth_user.id==id).select()
    sqlArray = []

    search = "id='"+str(id)+"' "
    sqlArray.append(search)

    place = str(request.vars.Place)
    breed = str(request.vars.Breed)
    age = str(request.vars.Age)
    #str rating = request.vars.Rating
    price = str(request.vars.Price)

    if place == "All States":
        place = ""
    else:
        place = "Place="+"'"+place+"'"
        sqlArray.append(place)

    if age == "All Ages":
        age = ""
    else:
        age = "Age="+"'"+age+"'"
        sqlArray.append(age)

    # if Rating = "All Ratings":
    #     Rating = ''
    # else:
    #     Rating = Rating + ' and '
    #
    if breed == "All Breeds":
        breed = ""
    else:
        breed = "Breed="+"'"+breed+"'"
        sqlArray.append(breed)

    if price == "All Prices":
         price = ''
    elif price != ">100":
        range = price.split("-")
        lower = range[0]
        higher = range[1]
        price = "Price BETWEEN "+lower+" AND "+ higher
        sqlArray.append(price)
    else:
        price = "Price>100"
        sqlArray.append(price)

    s = ""
    for val in sqlArray:
        if sqlArray.index(val) != len(sqlArray)-1:
            s = s + val + " and "
        else:
            s = s + val

    # print str
    #
    # sql = place + Age + breed

    #print "SELECT * FROM cat WHERE " + s +";"

    if s == "":
        rows = db(db.cat).select(orderby=db.cat.Name)
        d = {r.id: {'Name': r.Name, 'Human': r.Human, 'Breed':r.Breed, 'Place': r.Place, 'Age': r.Age, 'Bio': r.Bio, 'Price': r.Price, 'Image': r.Image, 'Created_On': r.Created_On}
            for r in rows}
    else:
        rows = db.executesql("SELECT * FROM cat WHERE " + s +";", as_dict=True)
        d = {r['id']: {'Name': r['Name'], 'Human': r['Human'], 'Breed': r['Breed'], 'Place': r['Place'], 'Age': r['Age'], 'Bio': r['Bio'], 'Price': r['Price'], 'Image': r['Image'], 'Created_On': r['Created_On']}
             for r in rows}

        print d
    return response.json(dict(cat_dict=d))

def load_cats():
    """Loads all messages for the user."""
    rows = db(db.cat).select()

    place = str(request.vars.Place)
    breed = str(request.vars.Breed)
    age = str(request.vars.Age)
    #str rating = request.vars.Rating
    price = str(request.vars.Price)

    sqlArray = []
    if place == "All States":
        place = ""
    else:
        place = "Place="+"'"+place+"'"
        sqlArray.append(place)

    if age == "All Ages":
        age = ""
    else:
        age = "Age="+"'"+age+"'"
        sqlArray.append(age)

    # if Rating = "All Ratings":
    #     Rating = ''
    # else:
    #     Rating = Rating + ' and '
    #
    if breed == "All Breeds":
        breed = ""
    else:
        breed = "Breed="+"'"+breed+"'"
        sqlArray.append(breed)

    if price == "All Prices":
         price = ''
    elif price != ">100":
        range = price.split("-")
        lower = range[0]
        higher = range[1]
        price = "Price BETWEEN "+lower+" AND "+ higher
        sqlArray.append(price)
    else:
        price = "Price>100"
        sqlArray.append(price)

    s = ""
    for val in sqlArray:
        if sqlArray.index(val) != len(sqlArray)-1:
            s = s + val + " and "
        else:
            s = s + val

    # print str
    #
    # sql = place + Age + breed

    #print "SELECT * FROM cat WHERE " + s +";"
    if s == "":
        rows = db(db.cat).select()
        d = {r.id: {'Name': r.Name, 'Human': r.Human, 'Breed':r.Breed, 'Place': r.Place, 'Age': r.Age, 'Bio': r.Bio, 'Price': r.Price, 'Image': r.Image, 'Created_On': r.Created_On}
            for r in rows}
    else:
        rows = db.executesql("SELECT * FROM cat WHERE " + s +";", as_dict=True)
        print rows
        d = {r['id']: {'Name': r['Name'], 'Human': r['Human'], 'Breed': r['Breed'], 'Place': r['Place'], 'Age': r['Age'], 'Bio': r['Bio'], 'Price': r['Price'], 'Image': r['Image'], 'Created_On': r['Created_On']}
             for r in rows}

    return response.json(dict(cat_dict=d))

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
    # auth.settings.registration_requires_verification = True
    # auth.settings.login_after_registration = True
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
