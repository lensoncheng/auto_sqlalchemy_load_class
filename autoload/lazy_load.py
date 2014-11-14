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

    @classmethod
    def map_table_to_class(cls, connection_url, mapper_list):
        lazy_loader = LazyLoader( connection_url )
        for table_name, class_name in mapper_list:
            lazy_loader.load_class_for_table( table_name, class_name )
        return 
        

class ReDefinitionError(Exception):
    def __init__(selfi, class_type):
        self.message = 'Threa already is a type named '+type(class_type)+' , you need changed you class now'

    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.message
            

def auto_load_register_table_class( configure_dict ):
    """
        configure_dict is a configure dict which contain connection , tables and mapper class name.
        example as:
        configure_dict = [
            {
                'mysql_url':'',
                'mapper_list':[('table_name','class_name'),...]
            },
            ...
        ]
    """
    for item in configure_dict:
        LazyLoader.map_table_to_class( item['mysql_url'], item['mapper_list'] )
    return 
    

if __name__ == '__main__':
    MYSQL_URL = 'mysql+pymysql://siren:DCB01C3C1F197C2C0F7B2153522AD6E0768B9B1D@192.168.1.108:3307/comment?charset=utf8mb4'
    configure_dict = []
    comment_dict = {
        'mysql_url':MYSQL_URL,
        'mapper_list':[ ('thread_comment',None), ('topic_comment', 'MyTopicComment'), ('thread_comment_imgs', None) ]
        }
    configure_dict.append( comment_dict )
    auto_load_register_table_class( configure_dict )

    dir(ThreadComment)
    dir( MyTopicComment )
    dir( ThreadCommentImgs)
    
