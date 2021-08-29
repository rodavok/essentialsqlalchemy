from sqlalchemy import MetaData, create_engine, Table, select, ForeignKeyConstraint
'''
reflect - build an sqlalchemy object from an existing database'''

metadata = MetaData()  #contains all schema objects associated with it
engine = create_engine('sqlite:///Chinook_Sqlite.sqlite')

#Table pulls a table from the database
#We gave it:
#   Table to pull from the database
#   metadata container
#   autoload - loads column names and other stuff ? found evidence this is depreciated in favor of:
#   autoload_wiith - supply engine to load from
artist = Table('Artist', metadata, autoload=True, autoload_with=engine)
album = Table('Album', metadata, autoload=True, autoload_with=engine)

#select 10 artists
s = select([artist]).limit(10)
engine.execute(s).fetchall()

#gets metadata from the Album table, similar to how tables are defined in sqlalchemy
#note, ArtistId does NOT reference @#(*@@_&@_#)*
#actually, the book is out of date and the foreign key relationship with Artist is
# correctly imported
# *** actually, this occurred because i reflected the tables at the same time, so SQLA was able to
# find the foreign key connection
# if they aren't loaded at the same time, SQLA will not try to hand you a broken foreign key
metadata.tables['Album']
'''
 Table('Album', MetaData(), 
    Column('AlbumId', INTEGER(), table=<Album>, primary_key=True, nullable=False),
    Column('Title', NVARCHAR(length=160), table=<Album>, nullable=False), 
    Column('ArtistId', INTEGER(), ForeignKey('Artist.ArtistId'), table=<Album>, nullable=False), 
    schema=None)

#Code to add a constraint - does this get passed to the DB or just the SQLA object?
album.append_constraint(
ForeignKeyConstraint(['ArtistId'], ['artist.ArtistId'])
)
'''

#join artist with album, convert join object to SQL string
str(artist.join(album))

#That was two tables
#now, let's do the whole DB

metadata.reflect(bind=engine)
#returns all tables, but also the ones we manually defined. They point to the same table as the
#tables pulled from the full reflect
metadata.tables.keys()

#pull the playlist table using the metadata
playlist = metadata.tables['Playlist']

#perform a query on the metadata
s = select([playlist]).limit(10)
engine.execute(s).fetchall()

#final notes on reflection
#checkconstraints, comments, and triggers can't be reflected (at least in 1.0 - we're on 1.4)
#can't reflect client-side defaults or associations between sequence & columns (?)
#can add them manually, though)
