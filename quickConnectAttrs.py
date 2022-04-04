'''
This tool easily lets you connect multiple attributes between nodes within a UI.
Made for py3 but if you want a py2 version lmk
'''

import pymel.core as pm

def ATTRIBUTE_UI():
    '''
    Creates the window.
    Window contains list of available attributes to connect from chosen nodes.

    returns None
    '''

    # Create window object


    # Add UI objects


    # Something else


def SELECTION_QUERY():
    '''
    Stores user selection.
    Only one outgoing connection, but multiple incoming connections.

    returns list of selections [OUTGOING,[INCOMING]]
    '''

    # outgoing connection


    # incoming connections

def ATTRIBUTE_QUERY(selection):
    '''
    Queries available attributes from selection.
    Does not allow for attributes that are not shared by all recieving an incoming connection.
    
    returns (dict?)list of all available attributes for connection
    '''

def CONNECTION_TYPE_QUERY():
    '''
    
    '''

def CONNECT_ATTRIBUTES(attributes):
    '''
    Connects attributes.
    '''

