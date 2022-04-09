'''
This tool easily lets you connect multiple attributes between nodes within a UI.
Made for py3 but if you want a py2 version lmk
'''

import pymel.core as pm
from sys import exit

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
    menuItemNum = 10 # custom default UI row item limit 
    w = 100 # width
    initalSelect = pm.ls(sl=1) # opens window with current selection as default inputs
    if not initalSelect:
        initalSelect = ['']

    with pm.window(mainWin,resizeToFitChildren=1,title='Connect Attributes',sizeable=0):
        
        with pm.columnLayout():

        # Diplsays selected objects and allows the user to change source and destination inputs
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.text(label='Source Object: ',width=w*1.5)
                sourceInput = pm.textField('source_input',width=w*2,text=initalSelect[0])
                sourceRefreshBtn = pm.button('refresh_source',label='Refresh',width=w,annotation='Change input to first object in current selection.')
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.separator(height=10,width=w*5,style='none')
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.text(label='Destination Objects: ',width=w*1.5)
                destInput = pm.textScrollList('dest_input',allowMultiSelection=1,width=w*2,append=initalSelect[1::])# default selected items indexed after 0)
                destRefreshBtn = pm.button('refresh_dest',label="Refresh",annotation='Change list to current objects in selection.',command=pm.Callback(EDIT_SELECTION, edit_type='refresh', object_input=destInput)) # refreshes list to what is selected 
                destRemoveBtn = pm.button('remove_object',label="Remove",annotation='Remove currenly hilighted object/s in list.',command=pm.Callback(EDIT_SELECTION, edit_type='remove', object_input=destInput)) # removes object from list
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.separator(height=10,width=w*5.15,style='in')
        
            # Displays attributes of source object and destination attributes shared by all destination objects # IDEASSS --- should a DOUBLE CLICK COMMAND, connect all common connections? IE - outColor into baseColor? maybe in the distant future...
            with pm.rowLayout(numberOfColumns=menuItemNum):
                with pm.columnLayout():
                    pm.text(label='Source Attributes')
                    sourceAttrsList = pm.textScrollList('source_attrs')#list of attrs on source obj -- UPDATE REG)
                with pm.columnLayout():
                    pm.text(label='Destination Attributes')
                    destAttrsList = pm.textScrollList('dest_attrs',allowMultiSelection=1)
            # Execute or cancel
        
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.separator(width=w*1.5,style='none')
                pm.button('execute_button',label='OK',width=w,annotation='Connect attributes. This is undoable.')
                pm.button('cancel_button',label='Cancel',width=w,command="print('CLOSE')")

    # All UI commands in order of appearance - Ease of use when updating functions in the fututre
    #sourceInput.textChangedCommand(pm.Callback(ATTRIBUTE_QUERY, edit_type = 'source', object_input = sourceInput, attribute_list = sourceAttrsList)) 
    sourceRefreshBtn.setCommand(pm.Callback(EDIT_SELECTION, edit_type='refresh', object_input=sourceInput, attribute_list=sourceAttrsList))
    destRefreshBtn.setCommand(pm.Callback(EDIT_SELECTION, edit_type='refresh', object_input=destInput, attribute_list=destAttrsList))
    destRemoveBtn.setCommand(pm.Callback(EDIT_SELECTION, edit_type='remove', object_input=destInput, attribute_list=destAttrsList))
    
def EDIT_SELECTION(edit_type,object_input,attribute_list):
    '''
    Updates UI source and destination to add or remove selected objects

    returns None
    '''

    activeSelection = SELECTION_QUERY()

    if edit_type == 'refresh':

        if 'source_input' in object_input:
            if len(activeSelection) > 1:
                pm.Mel.mprint('Multiple things selected -- storing only first item in selection list.')
            object_input.setText(activeSelection[0])
            ATTRIBUTE_QUERY(input_type='source', object_input=object_input, attribute_list=attribute_list)

        if 'dest_input' in object_input:
            object_input.removeAll()
            object_input.append(activeSelection)
            ATTRIBUTE_QUERY(input_type='dest', object_input=object_input, attribute_list=attribute_list)
            

    if edit_type == 'remove':
        if 'dest_input' in object_input:
                activeSelection = object_input.getSelectItem()
                object_input.removeItem(activeSelection)
                ATTRIBUTE_QUERY(input_type='dest', object_input=object_input, attribute_list=attribute_list)

def SELECTION_QUERY():
    '''
    Stores user selection.
    Errors if nothing is selected.

    returns selection list
    '''

    select = pm.ls(selection=1)
    if not select:
        pm.error("You must select something.")

    return select

def ATTRIBUTE_QUERY(input_type, object_input, attribute_list):
    '''
    Queries available attributes from source object and destination objects
    Does not allow for attributes that are not shared by all recieving an incoming connection.
    
    returns (dict?)list of all available attributes for connection
    '''

    if input_type == 'source':
        sourceObject = object_input.getText()
        sourceAttrs = pm.listAttr(sourceObject)
        attribute_list.removeAll()
        attribute_list.append(sourceAttrs)

    if input_type == 'dest':
        commonDestAttrs = []
        allAttrs = []
        destObjects = object_input.getAllItems()
        totalObjs = len(destObjects)

        for obj in destObjects:
            objAttrs = pm.listAttr(obj)
            allAttrs.extend(objAttrs)

        totalAttrs = set(allAttrs) # removes duplicate attributes
        attrDict = {i : 0 for i in totalAttrs}

        for attr in allAttrs:
            attrDict[attr] += 1

        for attr in totalAttrs:
            if attrDict[attr] == totalObjs:
                commonDestAttrs.append(attr)

        attribute_list.removeAll()
        attribute_list.append(commonDestAttrs)

            # MUST FIND LIST ITEMS THAT MATCH LENGTH OF THE TOTAL OBJECT COUNT ie: attribute_1 found 10 times == append to destination list.
            # create dictionary with key values for all found attributes, if key is found, value increases by 1.
            # loop thru all values, if value == number of objects, append.



def CONNECTION_TYPE_QUERY(out_attrribute,in_attributes):
    '''
    Updates destination textScrollList UI object to illustrate what connections are/aren't compatible.
    '''
    
    outAttrType = pm.listAttr()
    inAttrType = pm.listAttr()


    incompatibleAttrs = 3
    lineIndex = -1
    for attr in in_attributes:
        if attr:
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