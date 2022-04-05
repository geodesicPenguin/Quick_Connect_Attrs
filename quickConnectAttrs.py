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

    # General UI values    
    menuItemNum=10 # custom default UI row item limit 
    w = 100 #width
    with pm.window(mainWin,resizeToFitChildren=1,title='Connect Attributes'):
        
        with pm.columnLayout():

        # Diplsays selected objects and allows the user to change source and destination inputs
            with pm.rowLayout(numberOfColumns=menuItemNum):
                #pm.textFieldButtonGrp('source_input',label='Source: ') # SOURCE: input is first object in selection index. Button updates input with selected object -- FAILS if more than 1 object selected
                pm.text(label='Source: ',width=w)
                pm.textField('source_input',width=w*2)
                pm.button('refresh_source',label='Refresh',width=w)
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.separator(height=10,width=w*5,style='none')
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.text(label='Destination: ',width=w)
                pm.textScrollList('dest_input',allowMultiSelection=1,append=None,width=w*2)# default selected items inexed after 0)
                pm.button('refresh_dest',label="Refresh") # refreshes list to what is selected 
                pm.button('remove_object',label="Remove") # removes object from list
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.separator(height=10,width=w*5,style='in')
        
            # Displays attributes of source object and destination attributes shared by all destination objects
            with pm.rowLayout(numberOfColumns=menuItemNum):
                with pm.columnLayout():
                    pm.text(label='Source Attributes')
                    pm.textScrollList('source_attrs',append=None)#list of attrs on source obj -- UPDATE REG)
                with pm.columnLayout():
                    pm.text(label='Destination Attributes')
                    pm.textScrollList('dest_attrs',append=None)#dest attrs that are the same -- UPDATE REG)
        
            # Execute or cancel
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.button('execute_button',label='OK')
                pm.button('cancel_button',label='Cancel')






    # Add UI objects


    # Something else


def SELECTION_QUERY():
    '''
    Stores user selection.
    Only one outgoing connection, but multiple incoming connections.

    returns list of selections [OUTGOING,[INCOMING]]
    '''
    pass

    # outgoing connection


    # incoming connections

def ATTRIBUTE_QUERY(selection):
    '''
    Queries available attributes from selection.
    Does not allow for attributes that are not shared by all recieving an incoming connection.
    
    returns (dict?)list of all available attributes for connection
    '''
    pass

def CONNECTION_TYPE_QUERY():
    '''
    
    '''

def CONNECT_ATTRIBUTES(attributes):
    '''
    Connects attributes.
    '''
    pass

