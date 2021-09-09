from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

#instead of declarative_base, we use automap_base to reflect an existing db
Base = automap_base()
engine = create_engine('sqlite:///Chinook_Sqlite.sqlite')

#reflect the database referenced by the engine
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

#objects referencing tables in the Base
Artist = Base.classes.Artist
Album = Base.classes.Album

#create a session
session = Session(engine)
#and start querying
for artist in session.query(Artist).limit(10):
    print(artist.ArtistId, artist.Name)

#get the first artist
artist = session.query(Artist).first()
#artist's relation to album is in the album_collection method
#.*_collection is what's needed to acccess a table object's relations
#for each album that the first artist is related to,
for album in artist.album_collection:
    #print the artist name and album title
    print('{} - {}'.format(artist.Name, album.Title))