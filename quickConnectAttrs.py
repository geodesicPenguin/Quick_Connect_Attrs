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
    with pm.window(mainWin,resizeToFitChildren=1,title='Connect Attributes',sizeable=0):
        
        with pm.columnLayout():

        # Diplsays selected objects and allows the user to change source and destination inputs
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.text(label='Source Object: ',width=w*1.5)
                sourceInput = pm.textField('source_input',width=w*2,text='')
                pm.button('refresh_source',label='Refresh',width=w,statusBarMessage='Change input to first object in current selection.',command=EDIT_SELECTION)
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.separator(height=10,width=w*5,style='none')
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.text(label='Destination Objects: ',width=w*1.5)
                destInput = pm.textScrollList('dest_input',allowMultiSelection=1,append=None,width=w*2)# default selected items indexed after 0)
                pm.button('refresh_dest',label="Refresh",statusBarMessage='Change list to current objects in selection.',command=EDIT_SELECTION) # refreshes list to what is selected 
                pm.button('remove_object',label="Remove",statusBarMessage='Remove currenly hilighted object/s in list.',command=EDIT_SELECTION) # removes object from list
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.separator(height=10,width=w*5.15,style='in')
        
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
                pm.separator(width=w*1.5,style='none')
                pm.button('execute_button',label='OK',width=w,statusBarMessage='Connect attributes. This is undoable')
                pm.button('cancel_button',label='Cancel',width=w)

def EDIT_SELECTION():
    '''
    Updates UI source and destination add or remove selected objects
    '''
    pass


def SELECTION_QUERY():
    '''
    Stores user selection.
    Only one outgoing connection, but multiple incoming connections.

    returns list of selections [OUTGOING,[INCOMING]]
    '''
    select = pm.ls(selection=1)

    # outgoing connection


    # incoming connections

def ATTRIBUTE_QUERY(in_attributes):
    '''
    Queries available attributes from in-attributes.
    Does not allow for attributes that are not shared by all recieving an incoming connection.
    
    returns (dict?)list of all available attributes for connection
    '''
    attributeTypes = pm.listAttr()

def CONNECTION_TYPE_QUERY(out_attrribute,in_attributes):
    '''
    Updates destination textScrollList UI object to illustrate what connections are/aren't compatible.
    '''
    
    outAttrType = pm.listAttr()
    inAttrType = pm.listAttr()


    incompatibleAttrs = 
    lineIndex = -1
    for attr in in_attributes:
        if attr 
        lineIndex += 1 
        pm.textScrollList('dest_input',edit=1,lineFont=(lineIndex,'obliqueLabelFont'))

def CONNECT_ATTRIBUTES(attributes):
    '''
    Connects attributes.
    '''
    pass


# something about attributes
# sel = pm.ls(sl=1)[0]

# attrList = pm.listAttr(sel)

# for attr in attrList:

#     attrObj = pm.Attribute(f'{sel}.{attr}')
#     print(attrObj)