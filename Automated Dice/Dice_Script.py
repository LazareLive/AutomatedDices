#Automated Dice Creator
#Attempted by Lazare -- July 2022
#Based on "Design Your Own Custom Dice for Free | Blender Tutorial | DIY with Cly Ep. 21" by Cly Faker
#https://www.youtube.com/watch?v=nCowrvfOr3Q

#--- TO DO LIST ---
#Correctly center all numbers one to another and automate the thing
#Do D3, D16, D24, D30
#Do antiprism dices D6..D12
#Do rhombic dices
#Do bipyramid dices (D5, D7 and D9 possible with double number)
#Do other D24, D48, D64... and more ?
#Do D5 and D7 dices
#Do D2 and D4 rounded cube dices
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
_dotYPosition = -0.45
_diceList = []

#Function: Number Creator
def numberCreator(stringText):
    #Create Text Object
    bpy.ops.object.text_add(align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(0.0, 0.0, 0.0))
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
    #Change Center of Origin
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
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
        bpy.data.objects[dice].location = (distance, position, 0)
        position = position + distance
    
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
    #Return to object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    #Change Center of Origin
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    #Position and Rotate the antiprism solid
    bpy.data.objects[diceName].rotation_euler = (math.radians(90), 0, 0)
    bpy.data.objects[diceName].location = (0, 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

#Function: Fully rename de mesh and the linked object
#oldName : the name of the solid when created
#newName : the new name applied to the solid
def renameSolid(oldName, newName):
    bpy.data.objects[oldName].data.name = newName
    bpy.data.objects[oldName].name = newName

#Function: Apply faces to the dice using a set of rotations
#diceName : name of the dice object in blender
#rotationSequence : sequence of the dice to apply all the numbers
#numberOrder : number sequence to be applied to the dice
def diceAlgorithm(diceName, rotationSequence, numberOrder, textPosX, textPosY, textPosZ, textScale, textRotation, isPercentile=False):
    #Get the dice size using numberOrder
    faces = len(numberOrder)
    #In case of a dice with more than 8 faces, apply the dotted 6 and 9 for disambiguition
    if(faces > 8):
        #Prepare the dot/underscore sign position
        transformNumber('.', textScale, textPosX, textPosY + (_dotYPosition * textScale), textPosZ, textRotation)
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
        if((faces > 8) and (isPercentile == False) and ((numberOrder[i] == 6) or (numberOrder[i] == 9))):
            booleanOperationOnObject(diceName, _numName + '.')
        #Sequence the rotations and boolean for half a dice
        for sequence in rotationSequence[(i % len(rotationSequence))]:
            bpy.data.objects[diceName].rotation_euler = sequence
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
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
    
#Function: Generate any even-faced prismatic dice
def diceEvenPrismaticGenerator(faces, radius, depth, extrude, scale, numberOrder, textSize):
    #Test the function use, if the number of faces is odd, quit the function
    if (((faces % 2) == 1) and (faces < 4)):
        return
    #Dice Name
    diceName = 'D' + str(faces) + 'Prism'
    #Generate prism rotation
    transformationY = (0, math.radians(360.0 / faces), 0)
    rotations = ((transformationY,), (transformationY,))
    #Generate the solid
    generatePrismSolid(diceName, faces, radius, depth, extrude)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Get the face upper position using dimensions
    textZ = bpy.data.objects[diceName].dimensions.z / 2
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberOrder, 0, 0, textZ, textSize, 0)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the dice
    bpy.data.objects[diceName].hide_set(True)
    
#Function: Generate Prismatic D4
def dicePrismD4():
    #Number Order
    numOrd = (4, 2, 1, 3)
    #Generate the D4 dice with all parameters
    diceEvenPrismaticGenerator(4, 1, 2, 0.75, 7, numOrd, 12)
    
#Function: Generate Prismatic D6
def dicePrismD6():
    #Number Order
    numOrd = (6, 2, 4, 1, 5, 3)
    #Generate the D4 dice with all parameters
    diceEvenPrismaticGenerator(6, 1, 2, 0.75, 8, numOrd, 9)    
    
#Function: Generate Prismatic D8
def dicePrismD8():
    #Number Order
    numOrd = (8, 2, 6, 4, 1, 7, 3, 5)
    #Generate the D4 dice with all parameters
    diceEvenPrismaticGenerator(8, 1, 2, 0.75, 9, numOrd, 7)       
    
#Function: Generate Prismatic D10
def dicePrismD10():
    #Number Order
    numOrd = (6, 4, 8, 2, 0, 5, 7, 3, 9, 1)
    #Generate the D4 dice with all parameters
    diceEvenPrismaticGenerator(10, 1, 2, 0.75, 10, numOrd, 7)  
    
#Function: Generate any odd-faced prismatic dice
def diceOddPrismaticGenerator(faces, radius, depth, extrude, scale, numberOrder, textSize):
    #Test the function use, if the number of faces is even, quit the function
    if (((faces % 2) == 0) and (faces < 3)):
        return
    #Dice Name
    diceName = 'D' + str(faces) + 'Prism'
    #Generate prism rotation
    transformationY = (0, math.radians(360.0 / faces), 0)
    transformationZ = (0, 0, math.radians(180))
    rotations = ()
    for i in range(faces - 1):
        rotations = rotations + ((transformationY,),)
    rotations = rotations + ((transformationY, transformationZ),)
    #Generate the solid
    generatePrismSolid(diceName, faces, radius, depth, extrude)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Get the upper face index
    for poly in bpy.data.objects[diceName].data.polygons:
        #Check the normal position of the polygon. If the normal is 1, this is the upper face
        if (poly.normal.z == 1):
            break
    #Get the face side dimensions to calculate the text position
    textX = abs(bpy.data.objects[diceName].data.vertices[poly.vertices[0]].co.x) / 2
    #Get the face upper position using dimensions
    textZ = abs(bpy.data.objects[diceName].data.vertices[poly.vertices[0]].co.z)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberOrder, textX, 0, textZ, textSize, -90)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the dice
    bpy.data.objects[diceName].hide_set(True)
    
#Function: Generate Prismatic D3
def dicePrismD3():
    #Number Order
    numOrd = (1, 2, 3, 2, 1, 3)
    #Generate the D4 dice with all parameters
    diceOddPrismaticGenerator(3, 1, 1.5, 0.75, 10, numOrd, 7)
    
#Function: Generate Prismatic D5
def dicePrismD5():
    #Number Order
    numOrd = (1, 2, 3, 4, 5, 2, 1, 5, 4, 3)
    #Generate the D4 dice with all parameters
    diceOddPrismaticGenerator(5, 1, 1.5, 0.75, 10, numOrd, 6)
    
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
    dicePrismD4()
    dicePrismD6()
    dicePrismD8()
    dicePrismD10()
    #Odd-faces prism dice
    dicePrismD3()
    dicePrismD5()
    #Delete all numbers
    clearAllNumbers()
    #Replace all dices of a better view
    replaceAllDices()
    #Clean the font used
    bpy.data.fonts.remove(_fontOpen)
    
    #Test generation
    #generateBipyramidalSolid('D16', 8, 2, 2.5)
    #generatePrismSolid('D3Prism', 3, 1, 2, 0.75)
    #generatePrismSolid('D4Prism', 4, 1, 2, 1)
    #generatePrismSolid('D5Prism', 5, 1, 2, 1)
    #generatePrismSolid('D6Prism', 6, 1, 2, 1)
    #generateAntiprismSolid('D6Antiprism', 6, 1, 3, 0.75)
    #generateAntiprismSolid('D8Antiprism', 8, 1, 3, 0.75)
    #generateAntiprismSolid('D10Antiprism', 10, 1, 3, 0.75)
    #generateAntiprismSolid('D12Antiprism', 12, 1, 3, 0.75)
    
if __name__ == "__main__":
    main()
#Success !!!