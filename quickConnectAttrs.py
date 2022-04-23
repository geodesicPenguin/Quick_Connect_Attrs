'''
This tool easily lets you connect multiple attributes between nodes within a UI.
Made for py3 but if you want a py2 version lmk
'''

from enum import unique
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
    menuItemNum = 10 # custom default UI row item limit 
    w = 100 # width
    initalSelect = pm.ls(sl=1) # opens window with current selection as default inputs
    if not initalSelect:
        initalSelect = ['']
        initialSourceAttrs = None
    else:
        initialSourceAttrs = pm.listAttr(initalSelect,settable=1,connectable=1)
    

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
                destRefreshBtn = pm.button('refresh_dest',label="Refresh",annotation='Change list to current objects in selection.') # refreshes list to what is selected 
                destRemoveBtn = pm.button('remove_object',label="Remove",annotation='Remove currenly hilighted object/s in list.') # removes object from list
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.separator(height=10,width=w*5.15,style='in')
        
            # Displays attributes of source object and destination attributes shared by all destination objects # IDEASSS --- should a DOUBLE CLICK COMMAND, connect all common connections? IE - outColor into baseColor? maybe in the distant future...
            with pm.rowLayout(numberOfColumns=menuItemNum):
                with pm.columnLayout():
                    pm.text(label='Source Attributes')
                    sourceAttrsList = pm.textScrollList('source_attrs',append=initialSourceAttrs)#list of attrs on source obj -- UPDATE REG)
                with pm.columnLayout():
                    pm.text(label='Destination Attributes')
                    destAttrsList = pm.textScrollList('dest_attrs',allowMultiSelection=1)
                    destAttrsList.append(ATTRIBUTE_QUERY(input_type='dest',object_input=destInput,attribute_list=destAttrsList))

            # Execute or cancel
            with pm.rowLayout(numberOfColumns=menuItemNum):
                pm.separator(width=w*1.5,style='none')
                execButton = pm.button('execute_button',label='OK',width=w,annotation='Connect attributes. This is undoable.')
                cancelButton = pm.button('cancel_button',label='Cancel',width=w,command="print('CLOSE')")

    # All UI commands in order of appearance - Ease of use when updating functions in the fututre
    #sourceInput.textChangedCommand(pm.Callback(ATTRIBUTE_QUERY, edit_type = 'source', object_input = sourceInput, attribute_list = sourceAttrsList)) to be deleted 
    sourceRefreshBtn.setCommand(pm.Callback(UI_REFRESH, edit_type='refresh', object_input=sourceInput, attribute_list=sourceAttrsList))
    destRefreshBtn.setCommand(pm.Callback(UI_REFRESH, edit_type='refresh', object_input=destInput, attribute_list=destAttrsList))
    destRemoveBtn.setCommand(pm.Callback(UI_REFRESH, edit_type='remove', object_input=destInput, attribute_list=destAttrsList))
    sourceAttrsList.selectCommand(pm.Callback(CONNECTION_TYPE_QUERY, source_attrs_list=sourceAttrsList, dest_attrs_list=destAttrsList))
    execButton.setCommand(pm.Callback(CONNECT_ATTRIBUTES, source_object=sourceInput, dest_objects=destInput, source_attribute=sourceAttrsList, dest_attributes=destAttrsList))

def UI_REFRESH(edit_type,object_input,attribute_list):
    '''
    Updates UI source and destination to add or remove selected objects.

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

def ATTRIBUTE_QUERY(input_type, object_input, attribute_list):
    '''
    Queries available attributes from source object and destination objects
    Updates UI with new list of editable attributes.
    Does not allow for attributes that are not shared by all recieving an incoming connection.
    
    returns list of destination attributes
    '''

    # Getting source attrs simply finds the object's attrs and lists them in the textFieldList.
    if input_type == 'source':
        uniqueTagNum = 0
        sourceObject = object_input.getText()
        sourceAttrs = sorted(pm.listAttr(sourceObject,connectable=1,settable=1))
        attribute_list.removeAll()

        for attr in sourceAttrs:
            uniqueTagNum += 1
            try:
                attrType = pm.attributeQuery(attr,attributeType=1,node=sourceObject)
            except RuntimeError:
                attrType = False
            

            pm.textScrollList(attribute_list,edit=1,append=attr,uniqueTag=f'{attrType}_{uniqueTagNum}')

    # Getting dest attrs is complex, since we only want attrs every object shares. 
    # We loop through all the objects to get their attrs, then display only attrs found in every object.
    if input_type == 'dest':
        uniqueTagNum = 0
        allAttrs = []
        attrTypeDict = {}
        commonAttrs = []
        commonAttrsTypes = []
        destObjects = object_input.getAllItems()
        objCount = len(destObjects)

        for obj in destObjects:
            objAttrs = pm.listAttr(obj,connectable=1,settable=1)
            for attr in objAttrs:
                try:
                    attrType = pm.attributeQuery(attr,attributeType=1,node=obj) 
                    attrTypeDict[attr] = attrType # adds attr as key with attr type as value
                except RuntimeError:
                    attrType = False
                    attrTypeDict[attr] = attrType 
            allAttrs.extend(objAttrs) # adds object attrs to list of all attrs ie: ['message','outColor','outColor']

        totalAttrs = sorted(list(set(allAttrs))) # casting as set removes duplicate attributes, then re-casting as a list allows sorting before getting attr types + appending.
        attrCount = {i : 0 for i in totalAttrs}

        for attr in allAttrs:
            attrCount[attr] += 1

        attribute_list.removeAll() # Removes all attrs in textFieldList to then re-add new ones

        for commonAttr in totalAttrs:
            if attrCount[commonAttr] == objCount: # if the attribute shows up the same # of times as the # of objects, pass to textScrollList
                uniqueTagNum += 1
                commonAttrType = attrTypeDict[commonAttr]
                commonAttrsTypes.append(commonAttrType) # adds to a new list of all common attrs types
                commonAttrs.append(commonAttr) # adds to a new list of all common attrs
                pm.textScrollList(attribute_list,edit=1,append=commonAttr,uniqueTag=f'{commonAttrType}_{uniqueTagNum}')

        return commonAttrs
        # attribute_list.setSelectItem('color')
        # print(attribute_list.getSelectUniqueTagItem())
        # attribute_list.setSelectItem('diffuse')
        # attribute_list.setSelectUniqueTagItem('float3_1')
        # print(attribute_list.getSelectUniqueTagItem())
        # attribute_list.append('TEST').uniqueTag(['BLARF'])
        # attribute_list.setSelectUniqueTagItem('BLARF')

# NEXT, MAKE A "ON SELECTION" COMMAND FOR SOURCE SCROLL LIST TO UPDATE ATTRIBUTE FONTS BASED ON TYPE

def CONNECTION_TYPE_QUERY(source_attrs_list,dest_attrs_list):
    '''
    WIP

    Updates destination textScrollList UI object to illustrate what connections are/aren't compatible.
    Activates when source list item selected.

    returns None
    '''
    pass

    # sourceAttrType = source_attrs_list.getSelectUniqueTagItem()[0].split('_')[0] #takes off the unique tag number ie: the "_5" in "float3_5"
    # attrTypeSelectList = []
    # dest_attrs_list.selectAll()
    # destAttrTypes = dest_attrs_list.getSelectUniqueTagItem()
    # dest_attrs_list.deselectAll()

    # for attrType in destAttrTypes:
    #     if sourceAttrType in attrType:
    #         dest_attrs_list.setSelectUniqueTagItem(attrType)
        
    # #dest_attrs_list.getSelectItem()
    # attrTypesIndices = dest_attrs_list.getSelectIndexedItem()
    #         # the way this works is really weird.
    #         # the unique tag can only be used to add-select items in the list
    #         # we will have to make it select everything (in a list of all attr types -- [float3_1,float3_4])
    #         # then get their indices, THEn edit the text from there
    #         # then DESELECT them... 
    # attrCount = dest_attrs_list.getNumberOfItems()
    # for index in range(attrCount):
    #     for selectedIndex in attrTypesIndices:
    #         if index == selectedIndex:
    #             dest_attrs_list.lineFont([selectedIndex,'boldLabelFont'])
    #         else:
    #             dest_attrs_list.lineFont([selectedIndex,'obliqueLabelFont'])
    # dest_attrs_list.deselectAll()
    # dest_attrs_list.showIndexedItem(1)


def CONNECT_ATTRIBUTES(source_object, dest_objects, source_attribute, dest_attributes):
    '''
    Connects attributes.

    returns None
    '''
    

    # print(
    # dest_attributes.getSelectItem(),
    # source_attribute.getSelectItem(),
    # dest_objects.getAllItems(),
    # source_object.getText(),
    # sep='\n'
    # )
    
    #print(source_object, dest_objects, source_attribute, dest_attributes,sep='\n')
    errorLog = False

    with pm.UndoChunk():
        source = pm.Attribute(f'{source_object.getText()}.{source_attribute.getSelectItem()[0]}')
        for obj in dest_objects.getAllItems():
            for attr in dest_attributes.getSelectItem():
                destination = pm.Attribute(f'{obj}.{attr}')
                try:
                    source.connect(destination)
                except RuntimeError as e:
                    pm.Mel.mprint('{}'.format(e))
                    errorLog = True
    if not errorLog:
        pm.Mel.mprint('Connected attribute from {} to {} object(s)'.format(source,len(dest_objects.getAllItems())))
    # fun fact: mprint doesn't like f-strings. 
        


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


# something about attributes
# sel = pm.ls(sl=1)[0]

# attrList = pm.listAttr(sel)

# for attr in attrList:

#     attrObj = pm.Attribute(f'{sel}.{attr}')
#     print(attrObj)