# -*- coding:utf-8 -*-

__author__ = 'lenson.cheng'

"""
lazy load table in database with configure database connection url;
And mapper this table with a class ;
And register this class in global.
"""

from sqlalchemy.orm import mapper
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base 
from new import classobj


class LazyLoader(object):
    metadata = {}    

    def __init__(self, connection_url):
        self.connection_url = connection_url
        LazyLoader.metadata[ connection_url ] = None

    def load_class_for_table(self, table_name, class_name=None):
        if not LazyLoader.metadata[ self.connection_url ]:
            metadata = MetaData( self.connection_url )
            LazyLoader.metadata[ self.connection_url ] = metadata
        else:
            metadata = LazyLoader.metadata[ self.connection_url ]

        table = Table( table_name, metadata, autoload=True )
        if class_name == None:
            class_name = LazyLoader._generate_class_name_with_table_name( table_name )
        
        CLASS = classobj( class_name, (object,), {} )
        mapper( CLASS, table )
        if class_name in globals():
            raise ReDefinitionError( CLASS )
        else:
            globals()[class_name] = CLASS
        return CLASS

    @classmethod
    def _generate_class_name_with_table_name(cls, table_name):
        return ''.join( map( lambda x: x.capitalize(), table_name.split('_') ) )
        

class ReDefinitionError(Exception):
    def __init__(selfi, class_type):
        self.message = 'Threa already is a type named '+type(class_type)+' , you need changed you class now'

    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.message
            
    
