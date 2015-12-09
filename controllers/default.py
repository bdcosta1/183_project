# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
from gluon.dal import Rows, Row
import json
import time
from datetime import datetime


def index():
    return dict()

def add_cat():
    form = SQLFORM(db.cat)
    if form.process().accepted:
        session.flash = T('Your cat was added!')
        redirect(URL('default', 'listings'))
    elif form.errors:
        session.flash = T('Meow website is not working, please try again!')

    return dict(form=form)

def cat_details():
    row = db(db.cat.id == request.args(0)).select().first()
    return dict(row=row)

def start_rental():
    print request.args(0)
    db(db.cat.id == request.args(0)).update(Rented=True, Requester=auth.user_id)
    redirect(URL('default', 'listings'))
    return ""

def your_cat_rentals():
    row = db((db.cat.Human == auth.user_id) & (db.cat.Rented == True)).select()
    print row
    return dict(row=row)

# rental accepted, current renter set and timestamped, returns cat id
def accept_cat_rental():
    print request.args(0)
    print request.args(1)
    db(db.cat.id == request.args(0)).update(Current_Renter=request.args(1), Rented_On=datetime.now())
    redirect(URL('default', 'your_cat_rentals', args=[request.args(0)]))
    return ""

# if rent declined, requestor becomes cat owner and rented set to false for cat
def decline_cat_rental():
    db(db.cat.id == request.args(0)).update(Rented=False, Requester=request.args(1))
    redirect(URL('default', 'your_cat_rentals'))
    return ""

def end_rental():
    # row = db(db.cat.id == request.args(0)).select()
    # print row
    # db.customer_rentals.insert(='John',birthplace='Chicago')
    db(db.cat.id == request.args(0)).update(Rented=False, Current_Renter=auth.user_id, Requester=auth.user_id)
    redirect(URL('default', 'your_cat_rentals'))
    return ""

                # Field('Place', requires=IS_IN_SET(states)),
                # Field('Breed', requires=IS_IN_SET(cat_breeds)),
                # Field('Name'),
                # Field('Bio', 'text'),
                # Field('Age', requires=IS_IN_SET(ages)),
                # Field('Price', 'integer'),
                # Field('Image', 'upload'),
                # Field('Renter', db.auth_user, readable=False, writable=False),
                # Field('Rental_Time', 'datetime', readable=False, writable=False),

def listings():
    loggedIn = True
    if auth.user_id is None:
        loggedIn = False
        user_name = "none"
    else:
        user_name = auth.user.first_name
    return dict(loggedIn=loggedIn, user_id=auth.user_id, user_name=user_name)

@auth.requires_signature()
def update_cat():
    row = db(db.cat.id == request.vars.loc).select().first()
    row.update_record(Name = request.vars.Name)
    return "ok"

def user_profile():
    loggedInId = -1
    loggedIn = True
    isProfile = 0
    loggedInName = ""

    if auth.user_id is None:
        loggedIn = False
    else:
        loggedInId = auth.user_id
        loggedInName = db(db.auth_user.id == auth.user_id).select().first().first_name

    if loggedInId == int(request.args(0)):
        isProfile = 1

    row = db(db.auth_user.id == request.args(0)).select().first()

    return dict(loggedIn=loggedIn, user_id=request.args(0), first_name=row.first_name, prof_email=row.email, loggedInId=loggedInId, isProfile=isProfile, loggedInName = loggedInName)

def user_cats():
    """Loads all messages for the user."""
    rows = db(db.cat.Human == request.vars.user_num).select()
    d = {r.id: {'Name': r.Name, 'Human': r.Human, 'Breed':r.Breed, 'Place': r.Place, 'Age': r.Age, 'Bio': r.Bio, 'Price': r.Price, 'Image': r.Image, 'Created_On': r.Created_On}
        for r in rows}
    return response.json(dict(cat_dict=d))

def profile_ratings():
    """Loads all messages for the user."""
    rows = db(db.ratings.reviewed_profile == request.vars.user_num).select()
    d = {r.id: {'reviewed_profile': r.reviewed_profile, 'reviewer_profile': r.reviewer_profile, 'rating': r.rating, 'description': r.description, 'reviewer_name': r.reviewer_name, 'updated_on': r.updated_on}
        for r in rows}
    print rows
    return response.json(dict(rating_dict=d))

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

def cat_edit():
    cat = db.cat(request.args(0))
    if cat is None:
        session.flash = T('No cat exists')
        redirect(URL('index'))
    form = SQLFORM(db.cat, record=cat)
    if form.process().accepted:
        session.flash = T('Cat Edited')
        redirect(URL('listings'))

    return dict(form=form)

@auth.requires_signature()
def deleteCat():
    db(db.cat.id == request.vars.key).delete()
    return "ok"

def updateReview():
    db.ratings.update_or_insert((db.ratings.reviewed_profile==request.vars.user_id) & (db.ratings.reviewer_profile == request.vars.loggedInId),reviewed_profile = request.vars.user_id, reviewer_profile = request.vars.loggedInId, rating= request.vars.rating, description = request.vars.description, reviewer_name = request.vars.reviewer_name, updated_on = datetime.now())
    return "ok"

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
