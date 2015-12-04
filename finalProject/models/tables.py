#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
from datetime import datetime

cat_breeds = ['Siamese', 'Persian', 'British Shorthair', 'Abyssinian', 'Maine Coon', 'American Shorthair', 'Bengal', 'Sphynx', 'Ragdoll', 'Exotic Shorthair', 'Burmese', 'Scottish Fold', 'Birman', 'Siberian','Russian Blue', 'Norwegian Forrest', 'Himalayan', 'Turkish Angora', 'Munchkin']
states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY','LA', 'ME', 'ME','MD','MA','MI','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']


db.define_table('cat',
                Field('Name'),
                Field('Breed', requires=IS_IN_SET(cat_breeds)),
                Field('Bio', 'text'),
                Field('Age', 'integer'),
                Field('place', requires=IS_IN_SET(states)),
                Field('Price', 'integer'),
                Field('rating', readable =False, writable=False),
                Field('image', 'upload'),
                Field('human', db.auth_user, default=auth.user_id, readable =False, writable=False)
                )
