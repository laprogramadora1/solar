from sqlalchemy import MetaData, create_engine
from sqlalchemy_schemadisplay import create_schema_graph
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb              # <------- HERE!

#db = SQLAlchemy()
#engine = db.create_engine('mysql+pymysql://desarrollo:desarrollo@127.0.0.1/solardb')

# create the pydot graph object by autoloading all tables via a bound metadata object
graph = create_schema_graph(
    engine=create_engine('mysql+pymysql://root:root@localhost/solardb'),
   metadata = MetaData('mysql+pymysql://root:root@localhost/solardb'),
   
   show_datatypes=False, # The image would get nasty big if we'd show the datatypes
   show_indexes=False, # ditto for indexes
   rankdir='LR', # From left to right (instead of top to bottom)
   concentrate=False # Don't try to join the relation lines together,
)
graph.write_png('dbschema.png') # write out the file