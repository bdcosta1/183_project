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


cat_breeds = ['Abyssinian', 'American Bobtail','American Curl','American Shorthair','American Wirehair','Balinese','Bengal','Birman','Bombay',
'British Shorthair', 'Burmese','Charteux','Chausie','Colorpoint','Cornish Rex','Cymric','Devon Rex','Egyptian Mau','Exotic Shorthair',
'Havana Brown','Himalayan', 'Japanese Bobtail','Javanese','Korat','LaPerm','Maine Coon','Manx','Munchkin','Nebelung','Norwegian Forrest','Ocicat',
'Oriental Shorthair','Persian','Peterbald','Pixie-Bob','Ragamuffin','Ragdoll', 'Russian Blue','Savannah','Scottish Fold','Selkirk Rex','Siamese',
'Siberian','Singapura', 'Snowshoe','Somali','Sphynx','Tonkinese','Toyger', 'Turkish Angora','Turkish Van']
states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY','LA', 'ME', 'ME','MD','MA','MI','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
ages = ['less than 1','1','2','3','4','5','6','greater than 7']


db.define_table('cat',
                Field('Place', requires=IS_IN_SET(states)),
                Field('Breed', requires=IS_IN_SET(cat_breeds)),
                Field('Name', requires=IS_NOT_EMPTY()),
                Field('Bio', 'text', requires=IS_NOT_EMPTY()),
                Field('Age', requires=IS_IN_SET(ages)),
                Field('Price', 'integer', requires=IS_NOT_EMPTY()),
                Field('Rating', readable =False, writable=False),
                Field('Image', 'upload', requires=IS_NOT_EMPTY()),
                Field('Human', db.auth_user, default=auth.user_id, readable =False, writable=False),
                Field('Created_On', default=datetime.now().strftime("%m/%d"), readable=False, writable=False),
                Field('Rented', 'boolean', default=False, readable =False, writable=False),
                Field('Requester', db.auth_user, default=auth.user_id, readable=False, writable=False),
                Field('Current_Renter', db.auth_user, readable=False, writable=False),
                Field('Rented_On', 'datetime', readable=False, writable=False),
                )

# cats rented to owners
db.define_table('customer_rentals',
                Field('Place', requires=IS_IN_SET(states)),
                Field('Breed', requires=IS_IN_SET(cat_breeds)),
                Field('Name'),
                Field('Bio', 'text'),
                Field('Age', requires=IS_IN_SET(ages)),
                Field('Price', 'integer'),
                Field('Image', 'upload'),
                Field('Renter', db.auth_user, readable=False, writable=False),
                Field('Rental_Time', 'datetime', readable=False, writable=False),
                )

# cats rented from owners
db.define_table('your_rentals',
                )
