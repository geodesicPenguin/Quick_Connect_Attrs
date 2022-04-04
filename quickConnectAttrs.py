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
    mainWin = 'attr_ui_main'
    if pm.window(mainWin, exists=1):
        pm.deleteUI(mainWin)

    with pm.window(mainWin,resizeToFitChildren=1,mainMenuBar=1,title='Connect Attributes') as mw:

        # Diplsays selected objects and allows the user to change source and destination inputs
        with pm.rowLayout():
            pm.textFieldButtonGrp('source_input',text='Source: ') # SOURCE: input is first object in selection index. Button updates input with selected object -- FAILS if more than 1 object selected
        with pm.rowLayout():
            pm.text(label='Destination: ')
            pm.textScrollList('dest_input',allowMultiSelection=1,append=# default selected items inexed after 0)
            pm.button('refresh_dest',label="Refresh") # refreshes list to what is selected 
            pm.button('remove_object',label="Remove") # removes object from list
        pm.separator(height=40,style='in')

        # Displays attributes of source object and destination attributes shared by all destination objects
        with pm.rowLayout():
            with pm.columnLayout():
                pm.text(label='Source Attributes')
                pm.textScrollList('source_attrs',append=#list of attrs on source obj -- UPDATE REG)
            with pm.columnlayout():
                pm.text(label='Destination Attributes')
                pm.textScrollList('dest_attrs',append=#dest attrs that are the same -- UPDATE REG)




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

