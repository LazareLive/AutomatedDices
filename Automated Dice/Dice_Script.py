#Automated Dice Creator
#Attempted by Lazare -- July 2022
#Based on "Design Your Own Custom Dice for Free | Blender Tutorial | DIY with Cly Ep. 21" by Cly Faker
#https://www.youtube.com/watch?v=nCowrvfOr3Q

#--- DONE ---
#Create classic dices D4, D6, D8, D10, D%, D12 and D20
#Create prism and antiprism n-sided dices
#Modify dice font
#For all non-Platonician dices, generate the number sequence automatically
#Change the function method to authorize sizing parameters on non-Platonician dices
#Do bipyramid dices

#--- TO DO LIST ---
#Correctly center all numbers one to another and automate the thing
#Ability to modify the font imprint
#Change the function method to authorize sizing parameters on platonician dices
#Do D16, D24, D30
#Do rhombic dices
#Do other D24, D48, D60, D120 ... and more ?
#Do D5 and D7 dices
#Do D2 and D4 rounded cube dices
#Do extruded pyramid dices (half-bipyramid, name does not makes sense...)
#Do bipyramidal n-sided dices with twice the number order
#Create altered meshes such as rounded, beveled, etc.
#Optimise code for objects, and dice naming

#Import Blender librairies
import bpy
#Import additionnal libraries
import math

#Global variables
_fontFile = "C:\\Windows\\Fonts\\CantaraGotica.ttf"

#Internal global variables
_fontOpen = bpy.data.fonts.load(_fontFile)
_numName = '_Num'
_numbers = ('.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
    '16', '17', '18', '19', '20', '30', '40', '50', '60', '70', '80', '90', '00')
_dotYPosition = -0.15
_diceList = []

######################################
### TEXT/NUMBERS-RELATED FUNCTIONS ###
######################################

#Function: Number Creator
def numberCreator(stringText):
    #Create Text Object
    bpy.ops.object.text_add(align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(0.0, 0.0, 0.0))
    #Modify text alignments
    bpy.context.object.data.align_x = 'CENTER'
    bpy.context.object.data.align_y = 'CENTER'
    #Modify Text Object Name
    meshName = _numName + stringText
    bpy.data.objects['Text'].name = meshName
    #Get curve name for later deletion
    curve = bpy.data.objects[meshName].data
    #Assign Font To Object
    bpy.data.objects[meshName].data.font = _fontOpen
    #Change Text
    bpy.data.objects[meshName].data.body = stringText
    #Modify Text/Curve to Mesh
    bpy.ops.object.convert(target="MESH")
    #Extrude Number
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 1), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.ops.object.editmode_toggle()
    #Change mesh origin
    #bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    locY = bpy.data.objects[meshName].dimensions.y / 10
    bpy.data.objects[meshName].location = (0, locY, -0.5)
    #Apply transformations
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    #Clean the curve
    bpy.data.curves.remove(curve)
    # Rename Mesh    
    bpy.data.objects[meshName].data.name = meshName
    #Unselect Object
    bpy.data.objects[meshName].select_set(False)
    #Return Object Name
    return meshName

#Function: Creation of all Numbers
def generateAllNumbers():
    #For each number on the list, create them
    for x in _numbers:
        numberCreator(x)
        
#Function: Deletion of all numbers
def clearAllNumbers():
    #Delete all meshes linked to numbers
    for x in _numbers:
        bpy.data.meshes.remove(bpy.data.objects[_numName + x].data)

#Function: Modify the Number Mesh into a new position
def transformNumber(number, scale, locX, locY, locZ, rotate):
    #Get the number mesh name
    meshName = _numName + number
    #Change Number Dimensions
    bpy.data.objects[meshName].scale = (scale, scale, 1)
    #Change Position
    bpy.data.objects[meshName].location = (locX, locY, locZ)
    #Change Z Rotation
    bpy.data.objects[meshName].rotation_euler = (0, 0, math.radians(rotate))
    
#######################
### MESH OPERATIONS ###
#######################
    
#Function: Initialize the scale, position and rotation of a dice
def solidInitializePosition(dice, scale):
    #Reset the rotations
    bpy.data.objects[dice].rotation_euler = (0, 0, 0)
    #Change Position back to 0, 0, 0
    bpy.data.objects[dice].location = (0, 0, 0)
    #Scale the dice
    bpy.data.objects[dice].scale = (scale, scale, scale)
    #Apply transformations
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
#Function: Boolean Operation
def booleanOperationOnObject(objDice, objText):
    #Create the modifier on the Dice
    boolDiff = bpy.data.objects[objDice].modifiers.new(type="BOOLEAN", name="boolDiff")
    #Affect the Text on the modifier
    boolDiff.object = bpy.data.objects[objText]
    #Apply the boolean modification
    bpy.context.view_layer.objects.active = bpy.data.objects[objDice]
    bpy.ops.object.modifier_apply(modifier="boolDiff")
    
######################
### MESH CREATIONS ###
######################

#Function: Generate a two-coned dice with any number of faces
def generateBipyramidalSolid(diceName, vert, rad, dep):
    #Generate the first cone and rename it
    bpy.ops.mesh.primitive_cone_add(vertices=vert, radius1=rad, radius2=0, depth=dep, enter_editmode=False, align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
    renameSolid('Cone', diceName)
    #Generate a second cone, the same, and rotate it by 180° on X
    bpy.ops.mesh.primitive_cone_add(vertices=vert, radius1=rad, radius2=0, depth=dep, enter_editmode=False, align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
    bpy.data.objects['Cone'].rotation_euler = (math.radians(180), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Create a intersect boolean operation  
    intersectDiff = bpy.data.objects[diceName].modifiers.new(type="BOOLEAN", name="intersectDiff")
    #Affect the cone on the modifier
    intersectDiff.object = bpy.data.objects["Cone"]
    #Change the boolean method to INTERSECT
    intersectDiff.operation = "INTERSECT"
    #Apply the boolean modification
    bpy.context.view_layer.objects.active = bpy.data.objects[diceName]
    bpy.ops.object.modifier_apply(modifier="intersectDiff")
    #Delete the remaining cone
    bpy.data.meshes.remove(bpy.data.objects["Cone"].data)
    #Cleaning the new mesh to avoid strange faces and vertices
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type = 'FACE')
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.remove_doubles() 
    bpy.ops.object.mode_set(mode = 'OBJECT')
    #Select the Bipyramidal dice
    bpy.data.objects[diceName].select_set(True)
    
#Function: Generate Prism Dice
def generatePrismSolid(diceName, sides, rad, dep, extrudeSize):
    #Generate a n-sided cylinder
    bpy.ops.mesh.primitive_cylinder_add(vertices=sides, radius=rad, depth=dep, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    #Change the cylinder name
    renameSolid('Cylinder', diceName)
    #Rotate the dice to be aligned with the place
    bpy.data.objects[diceName].rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #And rotate the dice to be face up
    bpy.data.objects[diceName].rotation_euler = (0, math.radians(180 / sides), 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Create sides extrusion for cosmetic design
    #Go to edit mode to unselect all the vertices
    bpy.ops.object.mode_set(mode = 'EDIT') 
    #Select the object by its vertices
    bpy.ops.mesh.select_mode(type = 'VERT')
    #Deselect all the vertices
    bpy.ops.mesh.select_all(action = 'DESELECT')
    #Go to object mode to allow the selection of one of the sides of the prism
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for i in range(sides):
        bpy.context.active_object.data.vertices[i * 2].select = True
    #Return to edit mode
    bpy.ops.object.mode_set(mode = 'EDIT')
    #Extrude the element on one side
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, extrudeSize), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((0, 0, 1), (1, 0, 0), (0, 1, 0)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    #Merge the extrusion to the center
    bpy.ops.mesh.merge(type='CENTER')
    #Unselect all the vertices
    bpy.ops.mesh.select_all(action = 'DESELECT')
    #Go back to object mode to select the other side of the prism
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for i in range(sides):
        bpy.context.active_object.data.vertices[(i * 2) + 1].select = True
    #Go back to edit mode
    bpy.ops.object.mode_set(mode = 'EDIT')
    #Extrude the other vertices on the opposite side
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, (extrudeSize * -1)), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((0, 0, 1), (1, 0, 0), (0, 1, 0)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    #Merge the extrusion to the center of the face
    bpy.ops.mesh.merge(type='CENTER')
    #Return to object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
#Function: Generate Antiprism Dice
def generateAntiprismSolid(diceName, sides, rad, dep, extrudeSize):
    #Check the number sides is even
    if ((sides % 2) == 1):
        #Antiprism dices are only for even sided dices. Break function if odd.
        return
    polygon = int(sides/2)
    #Generate a n-sided circle
    bpy.ops.mesh.primitive_circle_add(vertices=polygon, radius=rad, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    #Change the Circle name to the dice name
    renameSolid('Circle', 'Circle0')
    #Get the Circle 0 mesh object
    meshC0 = bpy.data.objects['Circle0'].data
    #Generate another circle
    bpy.ops.mesh.primitive_circle_add(vertices=polygon, radius=rad, enter_editmode=False, align='WORLD', location=(0, 0, dep), scale=(1, 1, 1))
    #Rotate the last circile
    bpy.data.objects['Circle'].rotation_euler = 0, 0, (math.radians(360/sides))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Select only the objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Circle0'].select_set(True)
    bpy.data.objects['Circle'].select_set(True)    
    #Join both objects together
    bpy.ops.object.join()
    #Modify name of the object
    renameSolid('Circle', diceName)
    #Clean the Circle0 mesh
    bpy.data.meshes.remove(meshC0)
    #Connect all faces together
    #Go to edit mode to unselect all the vertices
    bpy.ops.object.mode_set(mode = 'EDIT') 
    #Select the object by its vertices
    bpy.ops.mesh.select_mode(type = 'VERT')
    #Generate all faces
    for i in range(polygon):
        #Create upper face
        #Deselect all the vertices
        bpy.ops.mesh.select_all(action = 'DESELECT')
        #Go to object mode to allow the selection of one of the sides of the prism
        bpy.ops.object.mode_set(mode = 'OBJECT')
        #Select the vertices to create a new face
        externalVertice = (i + 1) % polygon
        bpy.context.active_object.data.vertices[i].select = True
        bpy.context.active_object.data.vertices[polygon + i].select = True
        bpy.context.active_object.data.vertices[externalVertice + polygon].select = True
        #Return to edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        #Create the new face
        bpy.ops.mesh.edge_face_add()
        #Create lower face
        #Deselect all the vertices
        bpy.ops.mesh.select_all(action = 'DESELECT')
        #Go to object mode to allow the selection of one of the sides of the prism
        bpy.ops.object.mode_set(mode = 'OBJECT')
        #Select the vertices to create a new face
        externalVertice = (i + 1) % polygon
        bpy.context.active_object.data.vertices[polygon + externalVertice].select = True
        bpy.context.active_object.data.vertices[i].select = True
        bpy.context.active_object.data.vertices[(i + 1) % polygon].select = True
        #Return to edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        #Create the new face
        bpy.ops.mesh.edge_face_add()               
    #Create both sides extrusions
    for i in range(2):
        #Deselect all the vertices
        bpy.ops.mesh.select_all(action = 'DESELECT')
        #Go to object mode to allow the selection of one of the sides of the prism
        bpy.ops.object.mode_set(mode = 'OBJECT')
        #Select the vertices to create a new face
        for p in range(polygon):
            bpy.context.active_object.data.vertices[p + (i * polygon)].select = True
        #Return to edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        #Extrusion size methode
        if (i == 0):
            #First, extrude the upper side on positive position
            extrude = extrudeSize
        else:
            #Then: the lower side on negative position
            extrude = (extrudeSize * -1)
        #Generate extrusion
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, extrude), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        #Merge the extrusion to the center of the face
        bpy.ops.mesh.merge(type='CENTER')
    #Deselect all the vertices
    bpy.ops.mesh.select_all(action = 'DESELECT')        
    #Return to object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    #Change Center of Origin
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    #Position and Rotate the antiprism solid
    bpy.data.objects[diceName].rotation_euler = (math.radians(90), 0, 0)
    bpy.data.objects[diceName].location = (0, 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
###########################
### DICE-OBJECT ACTIONS ###
###########################
    
#Replace all dices
def replaceAllDices():
    #Distance //To be placed on global variable ?
    distance = 40
    #Create a counter for the position offset
    position = ((len(_diceList) - 1) * distance) / (-2)
    #For each dice created
    for dice in _diceList:
        #Change Position of D4
        bpy.data.objects[dice].hide_set(False)
        bpy.data.objects[dice].location = (0, position, 0)
        position = position + distance
        
#Function: Fully rename de mesh and the linked object
#oldName : the name of the solid when created
#newName : the new name applied to the solid
def renameSolid(oldName, newName):
    bpy.data.objects[oldName].data.name = newName
    bpy.data.objects[oldName].name = newName        
        
##################################
### NUMBER SEQUENCE GENERATION ###
##################################
        
#Function: Determination of an even number
def isEven(n):
    return ((n % 2) == 0)

#Function: Recursive function for diceNumberAlgorithm
def recursiveDiceNumberSequence(order):
    #There are several "notable" sequences that we will use for the dice number sequence. They are called triad, 
    #tetrad and pentad. As order cannot be less than 3, we will only use these sequences to generate any dice.
    #The goal will be to divide the number of faces until we can find a sequence. These sequences are generated by
    #using various calculations on the classic dices.
    #Tetrad case - Taken on the D3 and D6 dequences
    if(order == 3):
        return [3, 1, 2]
    #Tetrad case - Taken on the D8 sequence
    elif(order == 4):
        return [4, 1, 3, 2]
    #Pentad case - Taken on the D10 sequence -- to be checked. This does not feel right
    elif(order == 5):
        return [5, 1, 4, 2, 3]
    #For any other cases : use recursion until we find a n-ad sequence
    newOrder = math.trunc(order / 2)
    recursiveSequence = recursiveDiceNumberSequence(newOrder)
    #As the recursiveSequence will send half of the information, creation of a new array
    numberSequence = [0] * order
    if(isEven(order)):
        #On the case of an even order dice, check witch method to use based on the last recursion sequence
        for i in range(newOrder):
                #Generate the even-numbers on one polar side
                numberSequence[i] = recursiveSequence[i] * 2
                #Generate the odd_numbers on the other side
                if(isEven(newOrder)):
                    #On the even-even case, the last sequence is repeated to generate the current order
                    numberSequence[newOrder + i] = numberSequence[i] - 1
                else:
                    #On the even-odd case, the last sequence must be inverted to have a weak-strong alternance
                    numberSequence[newOrder + i] = ((newOrder - recursiveSequence[i] + 1) * 2) - 1            
    else:
        #On the case of an odd dice order, generate the dice following these rules
        #Placement of the first number
        numberSequence[0] = order
        #Placement of the recursive sequence
        for i in range(newOrder):
            #Generation of the even numbers on a polar side of the order
            numberSequence[i + 1] = recursiveSequence[newOrder - i - 1] * 2
            #Generation of the odd numbers
            numberSequence[order - (i + 1)] = order - numberSequence[i + 1]
    #Return the number sequence at the end
    return numberSequence
        
#Function: Generate Numbers for a n-sided die as a sequence
def diceNumberAlgorithmSequence(faces):
    #First: check the number of asked faces. Cannot be less than 3.
    if(faces < 3):
        return [(i + 1) for i in range(faces)]
    #If the number of faces is 4, a specific array must be returned as this cannot be created by the algorithm, and this is
    #the only solution for a 4 sided die
    if(faces == 4):
        return [4, 2, 1, 3]
    #In all other cases, we need to check whereas the die is even or odd
    if(isEven(faces)):
        #If it is even, the generation will follow the standard dice number sequence generation as the opposite sides must be
        #equal to the number of the die faces plus one.
        #Calculation of the even number sequence
        evenFaces = math.trunc(faces / 2)
        numberSequenceOrder = recursiveDiceNumberSequence(evenFaces)
        for i in range(evenFaces):
            #For each even number generated (NSO multiplied by 2)
            numberSequenceOrder[i] = numberSequenceOrder[i] * 2
            #Creation of the opposite side of the die
            numberSequenceOrder.append(faces - numberSequenceOrder[i] + 1)
        return numberSequenceOrder
    else:
        #If it is odd, the generation is automatically created by the recursion
        return recursiveDiceNumberSequence(faces)
    #In case of a problem, always send zero
    return [0]
    
################################################
### PRISM-DICES NUMBER SEQUENCE REGENERATION ###
################################################

#Function: Return Prism Dices Number Sequence
def sequenceNumberPrismDice(faces):
    #Get the sequence based on the number of faces
    sequenceOrder = diceNumberAlgorithmSequence(faces)
    #If the number of faces is 10, replace 10 with 0
    if (faces == 10):
        tenPosition = sequenceOrder.index(10)
        sequenceOrder[tenPosition] = 0
    #If even, return the sequence order as is
    if (isEven(faces)):
        return sequenceOrder
    #If odd, generation of a twin-numbered system
    else:
        oddSequence = [0] * (faces * 2)
        for i in range(faces):
            oddSequence[i * 2] = sequenceOrder[i]
            oddSequencePosition = ((i * 2) - 1) % (2 * faces)
            oddSequence[oddSequencePosition] = sequenceOrder[i]
        return oddSequence
    #In case of problem, return something
    return [0]

#Function: Return Bipyramidal Dices Number Sequence
def sequenceNumberBipyramidalDice(faces):
    #Get the sequence based on the number of faces
    sequenceOrder = diceNumberAlgorithmSequence(faces)
    #If the number of faces is 10, replace 10 with 0
    if (faces == 10):
        tenPosition = sequenceOrder.index(10)
        sequenceOrder[tenPosition] = 0
    #Generate the bipyramidal sequence
    bipyramidalSequence = [0] * faces
    #Calcul the base polygon sides
    polygonSides = math.trunc(faces/2)
    for i in range(0, polygonSides):
        #First half of the sequence stays
        bipyramidalSequence[i] = sequenceOrder[i]
        #Of the odd numbers, need to invert the sequence except for the first one
        position = ((i * (-1)) % polygonSides) + polygonSides
        bipyramidalSequence[position] = sequenceOrder[i + polygonSides]  
    return bipyramidalSequence
    
################################################
### DICE TRANSFORMATION SEQUENCE APPLICATION ###
################################################

#Function: Apply faces to the dice using a set of rotations
#diceName : name of the dice object in blender
#rotationSequence : sequence of the dice to apply all the numbers
#numberOrder : number sequence to be applied to the dice
def diceAlgorithm(diceName, rotationSequence, numberOrder, textPosX, textPosY, textPosZ, textScale, textRotation, isPercentile=False):
    #Get the dice size using numberOrder
    faces = len(numberOrder)
    #Get the dice max. number
    maxNumber = max(numberOrder)
    #In case of a dice with more than 8 faces, apply the dotted 6 and 9 for disambiguition
    if(maxNumber > 8):
        #Prepare the dot/underscore sign position
        #Trigonometry has to be used to calculate the dot position
        ratioX = math.sin(math.radians(textRotation * -1))
        ratioY = math.cos(math.radians(textRotation * -1))
        transformNumber('.', textScale, textPosX + (_dotYPosition * textScale * ratioX), textPosY + (_dotYPosition * textScale * ratioY), textPosZ, textRotation)
    #Rotation & Boolean operation between Dice and Number for all faces
    for i in range(faces):
        #Create the number object name
        numberOjectName = str(numberOrder[i])
        #If it is a percentile dice, add a 0 to the name
        if(isPercentile):
            numberOjectName = numberOjectName + '0'
        #Modify Number Position
        transformNumber(numberOjectName, textScale, textPosX, textPosY, textPosZ, textRotation)
        #Apply boolean operation on dice
        booleanOperationOnObject(diceName, _numName + numberOjectName)
        #If there is a 6 or a 9 face, apply the dot/underscore on the bottom
        if((maxNumber > 8) and (isPercentile == False) and ((numberOrder[i] == 6) or (numberOrder[i] == 9))):
            booleanOperationOnObject(diceName, _numName + '.')
        #Sequence the rotations and boolean for half a dice
        for sequence in rotationSequence[(i % len(rotationSequence))]:
            bpy.data.objects[diceName].rotation_euler = sequence
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
###############################            
### CLASSIC DICE GENERATORS ###
###############################
            
#Function: Tetrahedron Dice 4 Generator
def dice4Generator():
    #Dice Name
    diceName = 'D4'
    #Number order
    numOrd = (4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1)
    #Transformations pre-calculations
    transformationX1 = (math.radians(-19.47), 0, 0)
    transformationX2 = (math.radians(19.47), 0, 0)
    transformationX3 = (math.radians(70.53), 0, 0)
    transformationY1 = (0, math.radians(120), 0)
    transformationZ1 = (0, 0, math.radians(120))
    transformationZ2 = (0, 0, math.radians(-120))
    #Transformations order
    rotations = (
        (transformationX1, transformationY1, transformationX2),
        (transformationX1, transformationY1, transformationX2),
        (transformationZ1,),
        (transformationX1, transformationY1, transformationX2),
        (transformationX1, transformationY1, transformationX2),
        (transformationZ2,),
        (transformationX1, transformationY1, transformationX2),
        (transformationX1, transformationY1, transformationX2),
        (transformationX1, transformationY1, transformationX2, transformationZ2),
        (transformationX1, transformationY1, transformationX2),
        (transformationX1, transformationY1, transformationX2),
        (transformationX3,)
        )
    #Generate Tetrahedron
    bpy.ops.mesh.primitive_solid_add(source='4')
    #Rename Tetrahedron
    renameSolid('Solid', diceName)
    #Center and position dice
    solidInitializePosition(diceName, 15)
    #Initial rotation
    bpy.data.objects[diceName].rotation_euler = (0, 0, math.radians(-30))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.data.objects[diceName].rotation_euler = (0, math.radians(180), 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numOrd, 0, 6.5, 5, 10, 0)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the D4
    bpy.data.objects[diceName].hide_set(True)             

#Function: Cube Dice 6 Generator
def dice6Generator():
    #Dice Name
    diceName = 'D6'
    #Number order
    numOrd = (6, 2, 4, 3, 1, 5)
    #Transformations pre-calculations
    transformationA = (0, math.radians(-90), math.radians(90))
    transformationB = (math.radians(180), 0, 0)
    transformationC = (0, math.radians(90), math.radians(-90))
    transformationD = (math.radians(90), math.radians(180), math.radians(-90))
    #Transformations order
    rotations = (
        (transformationA,),
        (transformationA,),
        (transformationB,),
        (transformationC,),
        (transformationC,),
        (transformationD,)
    )
    #Cube generation
    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(8, 8, 8))
    #Modify Cube name to D6
    renameSolid('Cube', diceName)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numOrd, 0, 0, 8, 16, 0)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the D6
    bpy.data.objects[diceName].hide_set(True)
            
#Function: Octahedron Dice 8 Generator
def dice8Generator():
    #Dice Name
    diceName = 'D8'    
    #Number order
    numOrd = (8, 2, 6, 4, 5, 3, 7, 1)
    #Transformations pre-calculations
    transformationX1 = (math.radians(-35.265), 0, 0)
    transformationX2 = (math.radians(35.265), 0, 0)
    transformationX3 = (math.radians(180), 0, 0)
    transformationY1 = (0, math.radians(-90), 0)
    #Transformations order
    rotations = (
        (transformationX1, transformationY1, transformationX2), 
        (transformationX1, transformationY1, transformationX2), 
        (transformationX1, transformationY1, transformationX2),  
        (transformationX3,) 
        )
    #Generate Tetrahedron
    bpy.ops.mesh.primitive_solid_add(source='8')
    #Rename Octahedron
    renameSolid('Solid', diceName)
    #Before any resize, rotate the dice
    bpy.data.objects[diceName].rotation_euler = (0, math.radians(45), 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.data.objects[diceName].rotation_euler = (math.radians(35.265), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Center and position dice
    solidInitializePosition(diceName, 15)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numOrd, 0, 1, 8.66, 13, 0)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the D8
    bpy.data.objects[diceName].hide_set(True)          
            
#Function: Bipyramidal Dice 10 Generator
def dice10UnitGenerator():
    #Dice Name
    diceName = 'D10u'
    #Number order
    numOrd = (6, 4, 8, 2, 0, 1, 9, 3, 7, 5)
    #Transformations pre-calculations
    transformationX1 = (math.radians(-35.7), 0, 0)
    transformationX2 = (math.radians(35.7), 0, 0)
    transformationX3 = (math.radians(180), 0, 0)
    transformationY1 = (0, math.radians(72), 0)
    #Transformations order
    rotations = (
        (transformationX1, transformationY1, transformationX2), 
        (transformationX1, transformationY1, transformationX2), 
        (transformationX1, transformationY1, transformationX2),
        (transformationX1, transformationY1, transformationX2),  
        (transformationX3,) 
        )
    #Generate the D10 solid base
    generateBipyramidalSolid(diceName, 5, 2, 2.25)
    #Rotate the dice for a better scaling
    bpy.data.objects[diceName].rotation_euler = (math.radians(-54.3), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, 13)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numOrd, 0, 0, 8.55, 12, 0)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the D10
    bpy.data.objects[diceName].hide_set(True)  
    
#Function: Bipyramidal Dice 10 Generator
def dice10DecimalGenerator():
    #Dice Name
    diceName = 'D10d'
    #Number order
    numOrd = (6, 4, 8, 2, 0, 1, 9, 3, 7, 5)
    #Transformations pre-calculations
    transformationX1 = (math.radians(-35.7), 0, 0)
    transformationX2 = (math.radians(35.7), 0, 0)
    transformationX3 = (math.radians(180), 0, 0)
    transformationY1 = (0, math.radians(72), 0)
    #Transformations order
    rotations = (
        (transformationX1, transformationY1, transformationX2), 
        (transformationX1, transformationY1, transformationX2), 
        (transformationX1, transformationY1, transformationX2),
        (transformationX1, transformationY1, transformationX2),  
        (transformationX3,) 
        )
    #Generate the D10 solid base
    generateBipyramidalSolid(diceName, 5, 2, 2.25)
    #Rotate the dice for a better scaling
    bpy.data.objects[diceName].rotation_euler = (math.radians(-54.3), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, 13)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numOrd, 0, -1.55, 8.55, 9, 90, True)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the D10
    bpy.data.objects[diceName].hide_set(True)         
                    
#Function: Dodecahedron Dice 12 Generator
def dice12Generator():
    #Dice Name
    diceName = 'D12'
    #Number order
    numOrd = (12, 8, 6, 4, 2, 10, 1, 3, 11, 9, 7, 5)
    #Transformations pre-calculations
    transformationX1 = (math.radians(63.43), 0, 0)
    transformationX2 = (math.radians(-63.43), 0, 0)
    transformationX3 = (math.radians(180), 0, 0)
    transformationZ1 = (0, 0, math.radians(36))
    transformationZ2 = (0, 0, math.radians(72))
    #Transformations order
    rotations = (
        (transformationZ1, transformationX1), 
        (transformationX2, transformationZ2, transformationX1), 
        (transformationX2, transformationZ2, transformationX1), 
        (transformationX2, transformationZ2, transformationX1), 
        (transformationX2, transformationZ2, transformationX1), 
        (transformationX2, transformationZ1, transformationX3)
        )
    #Generate Dodecahedron
    bpy.ops.mesh.primitive_solid_add(source='12')
    #Rename Dodecahedron
    renameSolid('Solid', diceName)
    #Rotate the dice for a better scaling
    bpy.data.objects[diceName].rotation_euler = (math.radians(-58.285), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, 12)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numOrd, 0, 0, 9.54, 10, 0)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the D12
    bpy.data.objects[diceName].hide_set(True)          
    
#Function: Icosahedron Dice 20 Generator
def dice20Generator():    
    #Dice Name
    diceName = 'D20'
    #Number order
    numOrd = (20, 14, 6, 4, 8, 10, 16, 2, 18, 12, 1, 19, 9, 3, 13, 5, 11, 7, 17, 15)
    #Transformations pre-calculations
    transformationInit = (math.radians(20.905), 0, 0)
    transformationX1 = (math.radians(41.81), 0, 0)
    transformationX2 = (math.radians(-41.81), 0, 0)
    transformationX3 = (math.radians(180), 0, 0)
    transformationZ1 = (0, 0, math.radians(60))
    transformationZ2 = (0, 0, math.radians(120))
    transformationZ3 = (0, 0, math.radians(-120))
    #Transformations order
    rotations = (
        (transformationZ1, transformationX1),
        (transformationZ1, transformationX1),
        (transformationX2, transformationZ3, transformationX1),
        (transformationX2, transformationZ1, transformationX2, transformationZ2, transformationX1),
        (transformationZ1, transformationX1),
        (transformationX2, transformationZ3, transformationX1),
        (transformationX2, transformationZ1, transformationX2, transformationZ2, transformationX1),
        (transformationZ1, transformationX1),
        (transformationX2, transformationZ3, transformationX1),
        (transformationX2, transformationZ1, transformationX2, transformationZ1, transformationX3)
        )
    #Generate Icosahedron
    bpy.ops.mesh.primitive_solid_add(source='20')
    #Rename Dodecahedron
    renameSolid('Solid', diceName)
    #Rotate the dice for a better scaling
    bpy.data.objects[diceName].rotation_euler = (math.radians(20.905), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, 14)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numOrd, 0, 0, 11.125, 7, 0)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the D20
    bpy.data.objects[diceName].hide_set(True)  
    
################################
### PRISMATIC DICE GENERATOR ###
################################
    
#Function: Generate any even-faced prismatic dice
def diceEvenPrismaticGenerator(faces, radius, depth, extrude, scale, textSize):
    #Test the function use, if the number of faces is odd, quit the function
    if (((faces % 2) == 1) and (faces < 4)):
        return
    #Dice Name
    diceName = 'D' + str(faces) + 'Prism'
    #Generate the number sequence
    numberSequence = sequenceNumberPrismDice(faces)
    #Generate prism rotation
    transformationY = (0, math.radians(360.0 / faces), 0)
    rotations = ((transformationY,),)
    #Generate the solid
    generatePrismSolid(diceName, faces, radius, depth, extrude)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Get the face upper position using dimensions
    textZ = bpy.data.objects[diceName].dimensions.z / 2
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequence, 0, 0, textZ, textSize, 0)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the dice
    bpy.data.objects[diceName].hide_set(True)     
    
#Function: Generate any odd-faced prismatic dice
def diceOddPrismaticGenerator(faces, radius, depth, extrude, scale, textSize):
    #Test the function use, if the number of faces is even, quit the function
    if (((faces % 2) == 0) and (faces < 3)):
        return
    #Dice Name
    diceName = 'D' + str(faces) + 'Prism'
    #Generate the number sequence
    numberSequence = sequenceNumberPrismDice(faces)
    #Generate prism rotation
    transformationY = (0, math.radians(360.0 / faces), 0)
    transformationZ = (0, 0, math.radians(180))
    rotations = ((transformationZ,), (transformationZ, transformationY))
    #Generate the solid
    generatePrismSolid(diceName, faces, radius, depth, extrude)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Get the upper face index
    for poly in bpy.data.objects[diceName].data.polygons:
        #Check the normal position of the polygon. If the normal is 1, this is the upper face
        if (poly.normal.z >= 0.99):
            break
    #Get the face side dimensions to calculate the text position
    textX = abs(bpy.data.objects[diceName].data.vertices[poly.vertices[0]].co.x) / 2
    #Get the face upper position using dimensions
    textZ = abs(bpy.data.objects[diceName].data.vertices[poly.vertices[0]].co.z)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequence, textX, 0, textZ, textSize, -90)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the dice
    bpy.data.objects[diceName].hide_set(True)
    
#Function: Generate any prismatic dice
def diceAntirismaticGenerator(faces, radius, depth, extrude, scale, textSize):
    #Antiprismatic dice are only even, and start with a 6-face dice
    if (((faces % 2) == 1) and (faces < 6)):
        return
    #Dice Name
    diceName = 'D' + str(faces) + 'Antiprism'
    #Generate the number sequence
    numberSequence = sequenceNumberPrismDice(faces)
    #Generate the solid
    generateAntiprismSolid(diceName, faces, radius, depth, extrude)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Get the upper face index
    poly = bpy.data.objects[diceName].data.polygons[0]
    for p in bpy.data.objects[diceName].data.polygons:
        #Check the normal position of the polygon. 
        #If the normal is > 0.9, we can consider that this is the upper face
        if (p.normal.z >= poly.normal.z):
            poly = p          
    #Get the X angle to create the rotation
    angle = abs(poly.normal.y) * (-1)
    transformationXPosCalc = (math.sin(angle), 0, 0)
    #Create other rotations
    transformationXYZ1 = (math.sin(angle) * (-1), math.radians(360.0 / faces), math.radians(180))
    transformationXYZ2 = (math.sin(angle) * (-1), math.radians((-360.0) / faces), math.radians(180))
    #Transform the dice rotation
    bpy.data.objects[diceName].rotation_euler = transformationXPosCalc
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Redo a round on the dice
    for polyg in bpy.data.objects[diceName].data.polygons:
        if (abs(polyg.normal.z) == 1):
            poly = polyg
            break
    #Get the Y-text position
    upperY = 0
    lowerY = 0
    #From the upper polygon, get the vertices position
    for v in poly.vertices:
        vertex = bpy.data.objects[diceName].data.vertices[v]
        #Get the uppest and lowest values of the polygon on Y
        upperY = max(upperY, vertex.co.y)
        lowerY = min(lowerY, vertex.co.y)   
    #The antiprism seems to have a construction problem, should deal with absolutes (like the Devil)
    upperY = abs(upperY)
    lowerY = abs(lowerY)
    #The minimal value of Y always points toward the triangle base of the polygon
    minimalY = min(upperY, lowerY)
    #Calculate the text Y position on the solid
    textY = ((1/4) * (upperY + lowerY)) - minimalY
    #Get the Z-text position
    textZ = abs(bpy.data.objects[diceName].data.vertices[poly.vertices[0]].co.z)
    #Generate automatic rotations
    rotations = ((transformationXYZ1, transformationXPosCalc), (transformationXYZ2, transformationXPosCalc))
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequence, 0, textY, textZ, textSize, 0)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the dice
    bpy.data.objects[diceName].hide_set(True)
    
#Function: Generate any bipyramidal dice
def diceBipyramidGenerator(faces, radius, depth, scale, textSize):
    #Dice Name
    diceName = 'D' + str(faces) + 'Bipyramid'
    #Generate the number sequence
    numberSequence = sequenceNumberBipyramidalDice(faces)
    #Calculate the cone polygon shape
    polygonOrder = math.trunc(faces / 2)
    #Generate the bipyramidal solid base
    generateBipyramidalSolid(diceName, polygonOrder, radius, depth)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Transform the dice rotation to have a face plane on Y
    bpy.data.objects[diceName].rotation_euler = (0, 0, math.radians(180.0 + (360.0 / faces)))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Get polyhedra height
    height = abs(bpy.data.objects[diceName].dimensions.z / 2.0)
    #Get the polygon facing Y after rotation
    for polygon in bpy.data.objects[diceName].data.polygons:
        if(abs(polygon.normal.x) < 0.01):
            break
    #From that polygon, get all the vertices composing the polygon
    for v in polygon.vertices:
        vertex = bpy.data.objects[diceName].data.vertices[v]
        #If the polygon formed by the section of the bipyramid is even based
        if (isEven(polygonOrder)):
            #Polygon has 3 vertices, get one point where z=0 and return position
            if(abs(vertex.co.z) < 0.01):
                break
        #If the polygon formed by the section of the bipyramid is oddd based
        else:
            #Polygon has 4 vertices, generating a "kite" polygon
            #Get one of the lateral point where x=0 and is not the top of the polygon
            if((abs(vertex.co.x) < 0.01) and (abs(vertex.co.z) < height)):
                break
    #From the vertex selected, generate a rectangular triangle to calculate the angle of transformation
    width = abs(vertex.co.y)
    height = height + abs(vertex.co.z)
    #Get the dice rotation to be applied
    angle = math.atan(width/height) - math.radians(90)
    #Rotation calculations
    transformationXNeg = (angle, 0, 0)
    transformationXPos = (angle * (-1), 0, 0)
    transformationZ = (0, 0, math.radians(360.0 / polygonOrder))
    #Generate automatic rotations
    rotations = ()
    for i in range(polygonOrder - 1):
        rotations = rotations + ((transformationXPos, transformationZ, transformationXNeg),)
    rotations = rotations + ((transformationXPos, transformationZ, transformationXNeg, (math.radians(180), 0, 0)),)
    #Rotate the dice, one more, to have a face facing Z axis
    bpy.data.objects[diceName].rotation_euler = transformationXNeg
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Get the Y-text position from the shape of the upper face
    upperY = 0
    lowerY = 0
    for v in polygon.vertices:
        vertex = bpy.data.objects[diceName].data.vertices[v]
        upperY = max(upperY, vertex.co.y)
        lowerY = min(lowerY, vertex.co.y)
    textYDivider = math.ceil(math.sqrt(polygonOrder + 1))
    textY = lowerY + ((1/textYDivider) * (upperY - lowerY))
    #Set rotation if n faces > 12
    textRotation = 0
    if(faces > 12):
        textRotation = 90
    #Get the Z-text position
    textZ = abs(vertex.co.z)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequence, 0, textY, textZ, textSize, textRotation)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the dice
    bpy.data.objects[diceName].hide_set(True)
    
#####################
### MAIN FUNCTION ###
#####################
    
#Main function
def main():
    #Generate all numbers
    generateAllNumbers()
    #Dice Generation Sequence
    dice4Generator()
    dice6Generator()
    dice8Generator()
    dice10UnitGenerator()
    dice10DecimalGenerator()
    dice12Generator()
    dice20Generator()
    #Even-faces prism dice
    diceEvenPrismaticGenerator(4, 0.75, 2, 0.75, 8, 12)
    diceEvenPrismaticGenerator(6, 0.75, 2, 0.75, 8, 9)  
    diceEvenPrismaticGenerator(8, 1, 2, 0.75, 8, 8) 
    diceEvenPrismaticGenerator(10, 1.25, 2, 0.75, 8, 8)
    #Odd-faces prism dice
    diceOddPrismaticGenerator(3, 1, 1.25, 0.75, 8, 7) 
    diceOddPrismaticGenerator(5, 1.25, 1.5, 1, 8, 6)
    diceOddPrismaticGenerator(7, 1.5, 1.5, 1.25, 8, 6)
    diceOddPrismaticGenerator(9, 2.5, 2.5, 1.5, 8, 6)
    #Antiprism dices
    diceAntirismaticGenerator(6, 0.9, 2.25, 0.75, 9, 9)
    diceAntirismaticGenerator(8, 0.9, 2.25, 0.75, 9, 9)
    diceAntirismaticGenerator(10, 1, 2.25, 0.75, 9, 8) 
    diceAntirismaticGenerator(12, 1, 2.25, 0.5, 9, 7)
    diceAntirismaticGenerator(14, 1.25, 2.5, 0.5, 9, 7) 
    diceAntirismaticGenerator(16, 1.25, 2.5, 0.5, 9, 7) 
    diceAntirismaticGenerator(18, 1.33, 2.75, 0.5, 9, 7) 
    diceAntirismaticGenerator(20, 1.5, 3, 0.5, 9, 7) 
    #Bipyramidal dices --D8 and 10 not generated : looks a lot like Platonic
    diceBipyramidGenerator(6, 2, 2.25, 10, 8)
    diceBipyramidGenerator(12, 2.25, 2.25, 10, 6)
    diceBipyramidGenerator(14, 2.5, 2.25, 10, 6)
    diceBipyramidGenerator(16, 2.5, 2.5, 10, 6)
    diceBipyramidGenerator(18, 2.75, 2.5, 10, 6)
    diceBipyramidGenerator(20, 2.75, 2.5, 10, 6)
 
    #Delete all numbers
    clearAllNumbers()
    #Replace all dices of a better view
    #replaceAllDices()
    
    #Clean the font used
    bpy.data.fonts.remove(_fontOpen)
            
if __name__ == "__main__":
    main()
#Success !!!