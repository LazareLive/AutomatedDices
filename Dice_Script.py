#Automated Dice Creator
#Attempted by Lazare -- July 2022
#Based on "Design Your Own Custom Dice for Free | Blender Tutorial | DIY with Cly Ep. 21" by Cly Faker
#https://www.youtube.com/watch?v=nCowrvfOr3Q

#--- BEFORE RUNNING THE SCRIPT ---
#On Blender, go to Edit > Preferences > Add-on
#Type "Extra" on the research tool, and check "Add Mesh : Extra Objects"

#--- DONE ---
#Classic dices D4, D6, D8, D10, D%, D12 and D20
#Prism, Antiprism and Bipyramid n-sided dice
#D2 and D4 rounded cube dices
#Pseudo-Antiprism D4
#D30 Rhombic
#D24, D48, D60 nkis-hedron
#Dice scale can be chosen on classic dices
#Dice size and extrusions can be parametered on prism, antiprism and bipyramidal dice
#Text is centered, whatever the used font
#Text size and imprint are parametered
#Number sequence is automatically generated on n-sided dice
#Mesh alteration is global for all asked dice to be generated
#Change dot method for 6 & 9
#Extruded pyramid dices (shard dice)
#Text rotation on Bipyramidal & Antiprismatic
#Better Bevel

#--- TO DO LIST ---
#Do UVsphere dice
#Add symbol change for min/max value

#Import Blender librairies
import bpy, mathutils
#Import additionnal math library
import math, os

#Internal global variables
_mainPath = os.path.dirname(bpy.data.filepath)
_exportPath = _mainPath + "\\export\\"
_fontOpen = None

#Dot position variables
_dotSign = "."
_dotYPosition = -0.05

#Numeric scaling variables
_numName = '_Text'
_numSize = 0.6
_numLocY = 0.0
_numScale = 1.0

#Program lists for easy access
_numbers = []
_diceList = []

#Global bevel modification parameters
_bevelMethodActivation = False
_bevelAmount = 0
_bevelSegments = 5
_bevelShape = 0.5
_bevelMethod = 'EDGES'
_bevelSpread = 0

#Logo data
_logoName = '_Logo'
_logoUploaded = False

######################################
### TEXT/NUMBERS-RELATED FUNCTIONS ###
######################################

#Function: Set font
def setFont(font):
    #Access global parameters
    global _mainPath, _fontOpen
    #Create file pathing
    fontFile = _mainPath + "\\fonts\\" + font
    #Open font
    _fontOpen = bpy.data.fonts.load(fontFile)

#Function: Set dot sign
def setDotSign(dotPos, dot = ""):
    global _dotSign, _dotYPosition
    #Only 3 methods authorized : Bottom dot, Bottom underscore and dotted number
    if ((dot == "") or (dot == ".") or (dot == "_")):
        _dotSign = dot
    else:
        _dotSign = "."
    _dotYPosition = dotPos
        
#Function: Number Creator
def numberMeshCreator(stringText, initializeFont=False):
    #Initialize numSize usage from global
    global _numSize, _numLocY, _numScale
    #Create Text Object
    bpy.ops.object.text_add(align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(0.0, 0.0, 0.0))
    #Modify text alignments
    bpy.context.object.data.align_x = 'CENTER'
    #Modify Text Object Name
    meshName = _numName + stringText
    bpy.data.objects['Text'].name = meshName
    #Get curve name for later deletion
    curve = bpy.data.objects[meshName].data
    #Assign font To object
    bpy.data.objects[meshName].data.font = _fontOpen
    #Change text
    bpy.data.objects[meshName].data.body = stringText
    #Modify text/curve to mesh
    bpy.ops.object.convert(target="MESH")
    #From the conversion, get the lower point on Y-axis for calibration
    if(initializeFont):
        minimalYPos = 99
        for vertex in bpy.data.objects[meshName].data.vertices:
            minimalYPos = min(minimalYPos, vertex.co.y)
        _numLocY = (bpy.data.objects[meshName].dimensions.y / (-2)) - minimalYPos
        _numScale = abs(_numSize / bpy.data.objects[meshName].dimensions.y)    
    #Extrude Number
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 1), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.ops.object.editmode_toggle()
    #Change mesh origin
    bpy.data.objects[meshName].location = (0, _numLocY, -0.5)
    #Apply transformations
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    #Change mesh scaling to match 1 in Y
    bpy.data.objects[meshName].scale = (_numScale, _numScale, 1)   
    #Apply transformations
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) 
    #Clean the curve
    bpy.data.curves.remove(curve)
    # Rename mesh    
    bpy.data.objects[meshName].data.name = meshName
    #Unselect object
    bpy.data.objects[meshName].select_set(False)

#Function: Creation of all Numbers
def generateAllNumbersMeshes(maxNumber = 100):
    #Get the global numbers generated variable
    global _numbers 
    #Initialize _numbers array
    for num in range(maxNumber):
        _numbers.append(str(num + 1))
    _numbers.append('00')
    #Generate the dot sign
    if (_dotSign != ''):
        _numbers.append(_dotSign)
    else:
        #If method is empty, generate 6. and 9. signs
        _numbers.append('6.')
        _numbers.append('9.')    
    #Generate number 0, and find the center of the number. The Y localisation for 0 determine the all set of meshes center
    numberMeshCreator('0', True)
    #For each number on the list, create them
    for x in _numbers:
        numberMeshCreator(x)
    #Then, add 0 on the tuple list
    _numbers.append('0')
    #Clean the font used
    bpy.data.fonts.remove(_fontOpen)
        
#Function: Deletion of all numbers
def clearAllNumbersMeshes():
    #Delete all meshes linked to numbers
    for x in _numbers:
        bpy.data.meshes.remove(bpy.data.objects[_numName + x].data)
    #If a logo has been used, delete it also
    if (_logoUploaded):
        bpy.data.meshes.remove(bpy.data.objects[_logoName].data)

#Function: Modify the Number Mesh into a new position
def transformNumberMeshes(meshName, scale, locX, locY, locZ, rotate, imprint):
    #Change number dimensions
    bpy.data.objects[meshName].scale = (scale, scale, imprint * 2)
    #Change position
    bpy.data.objects[meshName].location = (locX, locY, locZ)
    #Change Z rotation
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
def booleanOperationOnObject(meshDestination, meshModifier, boolOperationType = 'DIFFERENCE'):
    #Create the modifier on the Dice
    boolOperator = bpy.data.objects[meshDestination].modifiers.new(type="BOOLEAN", name="boolOperator")
    #Affect the Text on the modifier
    boolOperator.object = bpy.data.objects[meshModifier]
    boolOperator.operation = boolOperationType
    #Apply the boolean modification
    bpy.context.view_layer.objects.active = bpy.data.objects[meshDestination]
    bpy.ops.object.modifier_apply(modifier="boolOperator")
    
#Function: Merging multi-triangle faces into one polygon
def meshMergeTriangularFaces(meshName):
    #Initialization of the normal vector list
    normalVectorList = []
    #For each polygon, fill normalVectorList with no doubles
    for polygon in bpy.data.objects[meshName].data.polygons:
        foundInList = False
        for vector in normalVectorList:
            if(vector == polygon.normal):
                foundInList = True
                break
        if(not foundInList):
            #Must define Vector type, else it appends the pointer to polygon.normal that will desappear with face dissolution
            normalVectorList.append(mathutils.Vector(polygon.normal))
    #Enter face selection mode through Edit mode and initialize the mesh
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type = 'FACE')
    bpy.ops.mesh.select_all(action = 'DESELECT')           
    #Cycle through the polygons and the list of normals again and select all faces with the same normal
    for vector in normalVectorList:
        #Enter Object mode for face selection
        bpy.ops.object.mode_set(mode = 'OBJECT')
        for polygon in bpy.data.objects[meshName].data.polygons:
            if(vector == polygon.normal):
                polygon.select = True
        #Go to edit mode for face dissolving
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.dissolve_faces()
        #Deselect all faces and continue looping
        bpy.ops.mesh.select_all(action = 'DESELECT')
    #Return to object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')

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
    booleanOperationOnObject(diceName, 'Cone', 'INTERSECT')
    #Delete the remaining cone
    bpy.data.meshes.remove(bpy.data.objects['Cone'].data)
    #Cleaning the new mesh to avoid strange faces and vertices
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type = 'FACE')
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.remove_doubles()
    #Recalculate normals
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.select_all(action = 'DESELECT')
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
    #Recalculate normals
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.select_all(action = 'DESELECT')
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
    #Recalculate normals
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.select_all(action = 'DESELECT')        
    #Return to object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    #Change Center of Origin
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    #Position and Rotate the antiprism solid
    bpy.data.objects[diceName].rotation_euler = (math.radians(90), 0, 0)
    bpy.data.objects[diceName].location = (0, 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
#Function: Generate a 4-sided pseudo antiprism
def generatePseudoAntiprism(diceName, lenght, minWidth, maxWidth):
    #Generate a first rectangle
    bpy.ops.mesh.primitive_plane_add(size=1, calc_uvs=True, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    bpy.data.objects['Plane'].scale = (minWidth, maxWidth, 1)
    #Change plane name
    renameSolid('Plane', 'Plane0')
    #Get the Circle 0 mesh object
    meshR0 = bpy.data.objects['Plane0'].data
    #Generate a second rectangle
    bpy.ops.mesh.primitive_plane_add(size=1, calc_uvs=True, enter_editmode=False, align='WORLD', location=(0, 0, lenght))
    bpy.data.objects['Plane'].scale = (maxWidth, minWidth, 1)
    #Join both planes together
    #Select only the objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Plane0'].select_set(True)
    bpy.data.objects['Plane'].select_set(True)    
    #Join both objects together
    bpy.ops.object.join()    
    #Clean the Circle0 mesh
    bpy.data.meshes.remove(meshR0)
    #Rename Plane as diceName
    renameSolid('Plane', diceName)
    #Go to edit mode to unselect all the vertices
    bpy.ops.object.mode_set(mode = 'EDIT') 
    #Select the object by its vertices
    bpy.ops.mesh.select_mode(type = 'VERT')
    #Generate all faces
    vertexOrder = (0, 1, 3, 2)
    for i in range(4):
        #Deselect all the vertices
        bpy.ops.mesh.select_all(action = 'DESELECT')
        #Go to object mode to allow the selection of one of the sides of the prism
        bpy.ops.object.mode_set(mode = 'OBJECT')
        #Select the vertices to create a new face
        bpy.context.active_object.data.vertices[vertexOrder[i]].select = True
        bpy.context.active_object.data.vertices[vertexOrder[(i + 1) % 4]].select = True
        bpy.context.active_object.data.vertices[4 + vertexOrder[i]].select = True
        bpy.context.active_object.data.vertices[4 + vertexOrder[(i + 1) % 4]].select = True
        #Return to edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        #Create the new face
        bpy.ops.mesh.edge_face_add()
    #Recalculate normals
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.select_all(action = 'DESELECT')
    #Return to object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    #Position and Rotate the antiprism solid
    bpy.data.objects[diceName].rotation_euler = (math.radians(90), 0, 0)
    bpy.data.objects[diceName].location = (0, lenght/(-2), 0)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
#Function: Generate a Rounded-Cube
def generateRoundedCube(diceName, cylinderVertices):
    #Generate a cube
    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.5, 0.0), rotation=(0.0, 0.0, 0.0), scale=(1, 0.5, 1))
    #Generate a cylinder
    bpy.ops.mesh.primitive_cylinder_add(vertices=cylinderVertices, radius=1, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), rotation=(0, math.radians(90), 0), scale=(1, 1, 1))
    #Create a union boolean operation between the cube and the cylinder
    booleanOperationOnObject('Cube', 'Cylinder', 'UNION')
    #Reposition cylinder
    bpy.data.objects['Cylinder'].rotation_euler = (0, 0, 0)
    bpy.data.objects['Cylinder'].location = (0, 1, 0)
    #Create a union boolean operation between the cube and the cylinder
    booleanOperationOnObject('Cube', 'Cylinder', 'UNION')
    #Delete Cylinder
    bpy.data.meshes.remove(bpy.data.objects['Cylinder'].data)
    #Simplify Rounded Cube vertices
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type = 'VERT')
    #Select all the solid to generate new triangular faces
    bpy.ops.mesh.select_all(action = 'SELECT')
    #Create triangle shapes
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    #Deselect all the vertices
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')    
    #Merge all triangular faces together
    meshMergeTriangularFaces('Cube')
    #Cleaning the new mesh to avoid strange faces and vertices
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type = 'FACE')
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.remove_doubles()
    #Recalculate normals
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')    
    #Rename Cube as diceName
    renameSolid('Cube', diceName)
    #Select the current mesh
    bpy.data.objects[diceName].select_set(True)
    #Replace the mesh at center position
    bpy.data.objects[diceName].rotation_euler = (0, 0, 0)
    bpy.data.objects[diceName].location = (0, 0, 0)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
#Function: Generate a shard n-gone trapezoidal dice with any number of faces
def generateShardSolid(diceName, vert, rad, depSize, depRatioTop = 0.5):
    #Check the depRaioTop value
    depRatioTop = max(min(1.0, depRatioTop), 0.0)
    #Generate a standard bipyramid solid
    generateBipyramidalSolid(diceName, vert, rad, depSize)
    #Enter Edit Mode
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type = 'VERT')
    #Select all the solid to generate new triangular faces
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    #Recalculate normals
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    #Select the top vertex only
    vertexZ = 0
    vertexIndex = 0
    #Scan all vertices from the polyhedron
    for vertex in bpy.context.active_object.data.vertices:
        if (vertex.co.z > vertexZ):
            vertexZ = vertex.co.z
            vertexIndex = vertex.index
    #Modify the shard upper vertex
    bpy.context.active_object.data.vertices[vertexIndex].co.z = depRatioTop * depSize * (0.5)
    #Select the shard dice
    bpy.data.objects[diceName].select_set(True) 
    
###########################
### MESH TRANSFORMATION ###
###########################

#Function: Call bevel parameters modifier
def meshBevelGlobalParameters(activation, amount, segments, shape, spread, method):
    global _bevelMethodActivation, _bevelAmount, _bevelSegments, _bevelMethod, _bevelShape, _bevelSpread
    _bevelMethodActivation = activation
    _bevelAmount = amount
    _bevelSegments = segments
    if((method == 'EDGES') or (method == 'VERTICES')):
        _bevelMethod = method
    else:
        _bevelMethod = 'EDGES'
    _bevelShape = max(shape, 0.5)
    _bevelSpread = spread

#Function: Apply bevel to the mesh
def meshBevel(meshName):
    #If method is activated
    if(_bevelMethodActivation):
        #Check Spread mode, Sharp by default if no spread entered
        spreadMode = 'SHARP'
        if(_bevelSpread > 0.0):
            #If spread detected, go to arc mode
            spreadMode = 'ARC'
        #Enter edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        #Select all the vertices
        bpy.ops.mesh.select_all(action = 'SELECT')
        #Apply Bevel
        bpy.ops.mesh.bevel(offset_type='OFFSET', profile_type='SUPERELLIPSE', offset=_bevelAmount, segments=_bevelSegments, profile=_bevelShape, affect=_bevelMethod, miter_inner=spreadMode, spread=_bevelSpread, clamp_overlap=True, loop_slide=True, mark_seam=False, mark_sharp=False, harden_normals=False, face_strength_mode='NONE', vmesh_method='ADJ', release_confirm=True)
        #Return to object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')
    
###########################
### DICE-OBJECT ACTIONS ###
###########################
    
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
def diceAlgorithm(diceName, rotationSequence, numberSequenceOrder, textPosX, textPosY, textPosZ, textScale, textRotation, textImprint, replaceLogo, isPercentile):
    #Bevel the edges of the die --All parameters on global
    meshBevel(diceName)
    #Get the dice size using numberSequenceOrder
    faces = len(numberSequenceOrder)
    #Get the dice max. number
    maxNumber = max(numberSequenceOrder)
    #In case of a dice with more than 8 faces, apply the dotted 6 and 9 for disambiguition
    if(maxNumber > 8):
        #Prepare the dot/underscore sign position
        #Trigonometry has to be used to calculate the dot position
        ratioX = math.sin(math.radians(textRotation * -1))
        ratioY = math.cos(math.radians(textRotation * -1))
        if (_dotSign != ''):
            transformNumberMeshes(_numName + _dotSign, textScale, textPosX + (_dotYPosition * textScale * ratioX), textPosY + (_dotYPosition * textScale * ratioY), textPosZ, textRotation, textImprint)
    #Rotation & Boolean operation between Dice and Number for all faces
    for i in range(faces):
        #Create the number object name
        numberObjectName = str(numberSequenceOrder[i])
        #Generate the 6 or 9 method for _dotSign specificatins
        if ((_dotSign == '') and ((numberSequenceOrder[i] == 6) or (numberSequenceOrder[i] == 9)) and (not isPercentile)):
            numberObjectName += '.'
        #If it is a percentile dice, add a 0 to the name
        if(isPercentile):
            numberObjectName = numberObjectName + '0'
        #If number matches the replace Logo symbol
        if((numberSequenceOrder[i] == replaceLogo) and (_logoUploaded)):
            numberObjectName = _logoName
        else:
            numberObjectName = _numName + numberObjectName
        #Modify Number Position
        transformNumberMeshes(numberObjectName, textScale, textPosX, textPosY, textPosZ, textRotation, textImprint)
        #Apply boolean operation on dice
        booleanOperationOnObject(diceName, numberObjectName)
        #If there is a 6 or a 9 face, apply the dot/underscore on the bottom
        if((maxNumber > 8) and (isPercentile == False) and ((numberSequenceOrder[i] == 6) or (numberSequenceOrder[i] == 9)) and (_dotSign != '')):
            booleanOperationOnObject(diceName, _numName + _dotSign)
        #Sequence the rotations and boolean for half a dice
        for sequence in rotationSequence[(i % len(rotationSequence))]:
            bpy.data.objects[diceName].rotation_euler = sequence
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Add the created dice to the list
    _diceList.append(diceName)
    #Hide the dice
    bpy.data.objects[diceName].hide_set(True)
    #Print out the success
    print(diceName, "has been created")
            
###############################            
### CLASSIC DICE GENERATORS ###
###############################
            
#Function: Tetrahedron Dice 4 Generator
def dice4Generator(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D4'
    #Number order
    numberSequenceOrder = (4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1)
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
    solidInitializePosition(diceName, scale)
    #Initial rotation
    bpy.data.objects[diceName].rotation_euler = (0, 0, math.radians(-30))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.data.objects[diceName].rotation_euler = (0, math.radians(180), 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, (6.5/15)*scale, (scale/3), textSize, 0, textImprint, replaceLogo, False)    

#Function: Cube Dice 6 Generator
def dice6Generator(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D6'
    #Number order
    numberSequenceOrder = (6, 2, 4, 3, 1, 5)
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
    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(scale, scale, scale))
    #Modify Cube name to D6
    renameSolid('Cube', diceName)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, 0, scale, textSize, 0, textImprint, replaceLogo, False)
            
#Function: Octahedron Dice 8 Generator
def dice8Generator(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D8'    
    #Number order
    numberSequenceOrder = (8, 2, 6, 4, 5, 3, 7, 1)
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
    solidInitializePosition(diceName, scale)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, (scale/15), (8.66/15)*scale, textSize, 0, textImprint, replaceLogo, False)         
            
#Function: Bipyramidal Dice 10 Generator
def dice10UnitGenerator(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D10u'
    #Number order
    numberSequenceOrder = (6, 4, 8, 2, 0, 1, 9, 3, 7, 5)
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
    solidInitializePosition(diceName, scale)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, 0, (8.55/13)*scale, textSize, 0, textImprint, replaceLogo, False)
    
#Function: Bipyramidal Dice 10 Generator
def dice10DecimalGenerator(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D10d'
    #Number order
    numberSequenceOrder = (6, 4, 8, 2, 0, 1, 9, 3, 7, 5)
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
    solidInitializePosition(diceName, scale)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, (-1.55/13)*scale, (8.55/13)*scale, textSize, 90, textImprint, replaceLogo, True)        
                    
#Function: Dodecahedron Dice 12 Generator
def dice12Generator(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D12'
    #Number order
    numberSequenceOrder = (12, 8, 6, 4, 2, 10, 1, 3, 11, 9, 7, 5)
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
    #Merging all faces with the same normal vector
    meshMergeTriangularFaces(diceName)
    #Rotate the dice for a better scaling
    bpy.data.objects[diceName].rotation_euler = (math.radians(-58.285), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, 0, (9.54/12)*scale, textSize, 0, textImprint, replaceLogo, False)       
    
#Function: Icosahedron Dice 20 Generator
def dice20Generator(scale, textSize, replaceLogo, textImprint):    
    #Dice Name
    diceName = 'D20'
    #Number order
    numberSequenceOrder = (20, 14, 6, 4, 8, 10, 16, 2, 18, 12, 1, 19, 9, 3, 13, 5, 11, 7, 17, 15)
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
    solidInitializePosition(diceName, scale)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, 0, (11.125/14)*scale, textSize, 0, textImprint, replaceLogo, False)
    
################################
### PRISMATIC DICE GENERATOR ###
################################
    
#Function: Generate any even-faced prismatic dice
def diceEvenPrismaticGenerator(faces, radius, depth, extrude, scale, textSize, replaceLogo, textImprint):
    #Test the function use, if the number of faces is odd, quit the function
    if (((faces % 2) == 1) and (faces < 4)):
        return
    #Dice Name
    diceName = 'D' + str(faces) + 'Prism'
    #Generate the number sequence
    numberSequenceOrder = sequenceNumberPrismDice(faces)
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
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, 0, textZ, textSize, 0, textImprint, replaceLogo, False)    
    
#Function: Generate any odd-faced prismatic dice
def diceOddPrismaticGenerator(faces, radius, depth, extrude, scale, textSize, replaceLogo, textImprint):
    #Test the function use, if the number of faces is even, quit the function
    if (((faces % 2) == 0) and (faces < 3)):
        return
    #Dice Name
    diceName = 'D' + str(faces) + 'Prism'
    #Generate the number sequence
    numberSequenceOrder = sequenceNumberPrismDice(faces)
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
    diceAlgorithm(diceName, rotations, numberSequenceOrder, textX, 0, textZ, textSize, -90, textImprint, replaceLogo, False)
    
#Function: Generate any prismatic dice
def diceAntiprismaticGenerator(faces, radius, depth, extrude, scale, textSize, textRotation, replaceLogo, textImprint, isPercentile=False):
    #Antiprismatic dice are only even, and start with a 6-face dice
    if (((faces % 2) == 1) and (faces < 6)):
        return
    #Dice Name
    diceName = 'D' + str(faces) + 'Antiprism'
    #In case of percentile
    if (isPercentile):
        diceName += '_D'
    #Generate the number sequence
    numberSequenceOrder = sequenceNumberPrismDice(faces)
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
        if (abs(polyg.normal.z) > 0.99999):
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
    textY = (_numSize * scale / 1.33) - minimalY
    #Get the Z-text position
    textZ = abs(bpy.data.objects[diceName].data.vertices[poly.vertices[0]].co.z)
    #Generate automatic rotations
    rotations = ((transformationXYZ1, transformationXPosCalc), (transformationXYZ2, transformationXPosCalc))
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, textY, textZ, textSize, textRotation, textImprint, replaceLogo, isPercentile)
    
#Function: Generate any bipyramidal dice
def diceBipyramidGenerator(faces, radius, depth, scale, textSize, textRotation, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D' + str(faces) + 'Bipyramid'
    #Generate the number sequence
    numberSequenceOrder = sequenceNumberBipyramidalDice(faces)
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
    #Retrieve upper and lower Y limits of the polygon
    for v in polygon.vertices:
        #Return Vertex positions
        vertex = bpy.data.objects[diceName].data.vertices[v]
        upperY = max(upperY, vertex.co.y)
        #Get lowerY depending on polygonOrder
        if (isEven(polygonOrder) or (polygonOrder == 3)):
            #If even (or d6 asked), always take the minimum Y position of the polygon
            lowerY = min(lowerY, vertex.co.y)
        else:
            #If odd, take the side vertex coordinates for Y as minimum
            if (abs(vertex.co.x) > 0.1):
                lowerY = vertex.co.y
    #Calculate the text Y position on the solid
    #Divider changes between odd/even base polygon as odd-faces has natural offset
    if (isEven(polygonOrder)):
        divider = 5/3
    else:
        divider = 2
    textY = (_numSize * scale / divider) + lowerY
    if(faces == 6):
        textY = lowerY + (upperY - lowerY)/2
    #Get the Z-text position
    textZ = abs(vertex.co.z)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, textY, textZ, textSize, textRotation, textImprint, replaceLogo, False)
    
#Function: Generate any bipyramidal dice
def diceShardGenerator(faces, radius, depth, depthTopRaio, scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D' + str(faces) + 'Shard'
    #Generate the number sequence
    numberSequenceOrder = diceNumberAlgorithmSequence(faces)
    #Generate the bipyramidal solid base
    generateShardSolid(diceName, faces, radius, depth, depthTopRaio)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Get the top dice height
    height = depth * depthTopRaio * scale * 0.5
    #Transform the dice rotation to have a face plane on Y
    if (isEven(faces)):
        bpy.data.objects[diceName].rotation_euler = (0, 0, math.radians(180.0 / faces))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Get the polygon facing Y after rotation
    for polygon in bpy.data.objects[diceName].data.polygons:
        if(abs(polygon.normal.x) < 0.01):
            break
    #From that polygon, get all the vertices composing the polygon
    for v in polygon.vertices:
        vertex = bpy.data.objects[diceName].data.vertices[v]
        #If the polygon formed by the section of the bipyramid is even based
        if (isEven(faces)):
            #Polygon has 3 vertices, get one point where z=0 and return position
            if(abs(vertex.co.z) < 0.01):
                break
        #If the polygon formed by the section of the bipyramid is oddd based
        else:
            #Polygon has 4 vertices, generating a "kite" polygon
            #Get one of the lateral point where x=0 and is not the top of the polygon
            if(abs(vertex.co.z) < height):
                break
    #From the vertex selected, generate a rectangular triangle to calculate the angle of transformation
    width = abs(vertex.co.y)
    height = height - abs(vertex.co.z)
    #Get the dice rotation to be applied
    angle = math.atan(width/height) - math.radians(90)
    #Rotation calculations
    transformationXNeg = (angle, 0, 0)
    transformationXPos = (angle * (-1), 0, 0)
    transformationZ = (0, 0, math.radians(360.0 / faces))
    #Generate automatic rotations
    rotations = ()
    for i in range(faces):
        rotations = rotations + ((transformationXPos, transformationZ, transformationXNeg),)
    #rotations = rotations + ((transformationXPos, transformationZ, transformationXNeg, (math.radians(180), 0, 0)),)
    #Rotate the dice, one more, to have a face facing Z axis
    bpy.data.objects[diceName].rotation_euler = transformationXNeg
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Get the Y-text position from the shape of the upper face
    upperY = 0
    lowerY = 0
    #Retrieve upper and lower Y limits of the polygon
    for polygon in bpy.data.objects[diceName].data.polygons:
        if(polygon.normal.z > 0.99):
            break
    for v in polygon.vertices:
        vertex = bpy.data.objects[diceName].data.vertices[v]
        upperY = max(upperY, vertex.co.y)
        lowerY = min(lowerY, vertex.co.y)
    #Calculate the text Y position on the solid
    textY = lowerY + ((upperY - lowerY) / 3)
    #Get the Z-text position
    textZ = abs(vertex.co.z)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, textY, textZ, textSize, 0, textImprint, replaceLogo, False)
    
#############################
### ADDITIONAL SHAPE DICE ###
#############################

#Function: Generate a D2 Rounded Cube
def diceRoundedCubeGenerator(faces, roundVertices, scale, textSize, replaceLogo, textImprint):
    #Rounded cube can be D2 or D4 only
    if ((faces != 2) and (faces != 4)):
        return
    #Dice Name
    diceName = 'D' + str(faces) + 'RoundedCube'
    #Number order
    if(faces == 2):
        numberSequenceOrder = (2, 1, 2, 1)
    else:
        numberSequenceOrder = (4, 2, 1, 3)
    #Transformations pre-calculations
    transformationA = (0, math.radians(90), 0)
    transformationB = (0, 0, math.radians(180))
    #Transformations order
    rotations = ((transformationA, transformationB), (transformationB, transformationA),)
    #Rounded cube generation
    generateRoundedCube(diceName, roundVertices)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, scale/3, scale, textSize, 90, textImprint, replaceLogo, False)
    
#Function: Generate any prismatic dice
def dice4PseudoAntiprismaticGenerator(lenght, minWidth, maxWidth, scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D4PseudoAntiprism'
    #Generate the number sequence
    numberSequenceOrder = sequenceNumberPrismDice(4)
    #Generate the solid
    generatePseudoAntiprism(diceName, lenght, minWidth, maxWidth)
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
    #Transform the dice rotation
    bpy.data.objects[diceName].rotation_euler = transformationXPosCalc
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Create other rotations
    transformationXYZ1 = (math.sin(angle) * (-1), math.radians(90), math.radians(180))
    transformationXYZ2 = (math.sin(angle) * (-1), math.radians(-90), math.radians(180))
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
    textY = ((1/3) * (upperY + lowerY)) - minimalY
    #Get the Z-text position
    textZ = abs(bpy.data.objects[diceName].data.vertices[poly.vertices[0]].co.z)
    #Generate automatic rotations
    rotations = ((transformationXYZ1, transformationXPosCalc), (transformationXYZ2, transformationXPosCalc))
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotations, numberSequenceOrder, 0, textY, textZ, textSize, 0, textImprint, replaceLogo, False)
    
##############################
### RHOMBIC/KIS SHAPE DICE ###
##############################

baseRotationsTetrahedron = (
    ((math.radians(-109.471), 0, math.radians(60)), ),
    ((math.radians(-109.471), 0, math.radians(60)), ),
    ((0, 0, math.radians(60)), (math.radians(109.471), 0, 0)), 
    ((math.radians(-109.471), 0, 0), (0, 0, math.radians(-60)))
    )
    
baseRotationsHexahedron = (
    ((0, math.radians(-90), math.radians(90)), ),
    ((0, math.radians(-90), math.radians(90)), ),
    ((math.radians(180), 0, 0), ),
    ((0, math.radians(90), math.radians(-90)), ),
    ((0, math.radians(90), math.radians(-90)), ),
    ((math.radians(90), math.radians(180), math.radians(-90)), )
    )

baseRotationsDodecahedron = (
    ((0, 0, math.radians(36)), (math.radians(63.43), 0, 0)), 
    ((math.radians(-63.43), 0, 0), (0, 0, math.radians(72)), (math.radians(63.43), 0, 0)), 
    ((math.radians(-63.43), 0, 0), (0, 0, math.radians(72)), (math.radians(63.43), 0, 0)), 
    ((math.radians(-63.43), 0, 0), (0, 0, math.radians(72)), (math.radians(63.43), 0, 0)), 
    ((math.radians(-63.43), 0, 0), (0, 0, math.radians(72)), (math.radians(63.43), 0, 0)), 
    ((math.radians(-63.43), 0, 0), (0, 0, math.radians(36)), (math.radians(180), 0, 0))
    )
    
baseRotationsIcosahedron = (
    ((0, 0, math.radians(60)), (math.radians(41.81), 0, 0)),
    ((0, 0, math.radians(60)), (math.radians(41.81), 0, 0)),
    ((math.radians(-41.81), 0, 0), (0, 0, math.radians(-120)), (math.radians(41.81), 0, 0)),
    ((math.radians(-41.81), 0, 0), (0, 0, math.radians(60)), (math.radians(-41.81), 0, 0), (0, 0, math.radians(120)), (math.radians(41.81), 0, 0)),
    ((0, 0, math.radians(60)), (math.radians(41.81), 0, 0)),
    ((math.radians(-41.81), 0, 0), (0, 0, math.radians(-120)), (math.radians(41.81), 0, 0)),
    ((math.radians(-41.81), 0, 0), (0, 0, math.radians(60)), (math.radians(-41.81), 0, 0), (0, 0, math.radians(120)), (math.radians(41.81), 0, 0)),
    ((0, 0, math.radians(60)), (math.radians(41.81), 0, 0)),
    ((math.radians(-41.81), 0, 0), (0, 0, math.radians(-120)), (math.radians(41.81), 0, 0)),
    ((math.radians(-41.81), 0, 0), (0, 0, math.radians(60)), (math.radians(-41.81), 0, 0), (0, 0, math.radians(60)), (math.radians(180), 0, 0))
    )
       
#Function: Generate a full set of rotation using base and sub rotationnal systems
def rotationKisSequenceGeneration(baseRotations, subAngle, faceDivisions):
    #Generate the sub-angle transformation for the X-axis
    subRotationXPositive = (math.radians(subAngle), 0, 0)
    subRotationXNegative = (math.radians(subAngle * (-1)), 0, 0)
    #Initialize sub-rotation for Z-axis
    subRotationZ = (0, 0, math.radians(360 / faceDivisions))
    #Generate the subRotation full transformations
    subRotationsPosition = (subRotationXNegative, subRotationZ, subRotationXPositive)  
    #Create empty list for transformationsSequence
    transformationsSequence = ()
    #Initialize the complex sub transformation list to include base polyhedron transformation
    complexSubTransformation = ()
    #For each base rotations, generate a set of transformations based on face divisions
    for rotation in range(len(baseRotations)):
        #Add standard subrotations for each base rotation
        for sub in range(faceDivisions - 1):
            transformationsSequence += (subRotationsPosition, )
        #Create the complex sub rotation on the system : return to the vertex position
        complexSubTransformation = (subRotationXNegative, subRotationZ)
        #Add the base rotations to the transformation
        for baseSubRotation in baseRotations[rotation]:
            complexSubTransformation += (baseSubRotation, )
        #Return to a face orientation on the Z axis
        complexSubTransformation += (subRotationXPositive, )
        #Add the complex sub rotation to the sequence
        transformationsSequence += (complexSubTransformation, )        
    #Return the transformations
    return transformationsSequence

#Function: Rhombic Dodecahedron Dice 12 Generator
def dice12RhombicGenerator(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D12Rhombic'
    #Number order
    numberSequenceOrder = (9, 1, 3, 7, 4, 8, 12, 6, 2, 11, 5, 10)
    #Generate Rhombic Dodecahedron
    bpy.ops.mesh.primitive_solid_add(source='4', vTrunc=1, eTrunc=1, snub='None', dual=True, keepSize=True, preset='dr4')
    #Rename Dodecahedron
    renameSolid('Solid', diceName)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Generate full rotation sequence from base rotations and sub rotations
    rotationSequence = rotationKisSequenceGeneration(baseRotationsTetrahedron, 35.2645, 3)
    #Rotate the dice for a face orientation toward Z axis for initialization
    bpy.data.objects[diceName].rotation_euler = (0, 0, math.radians(30))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Rotate the dice for a face orientation toward X axis for initialization
    bpy.data.objects[diceName].rotation_euler = (math.radians(35.2645), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)     
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotationSequence, numberSequenceOrder, 0, 0, (0.8165 * scale), textSize, 0, textImprint, replaceLogo, False)
    
#Function: Catalan Tetrakis Hexahedron Dice 24 Generator
def dice24TetrakisGenerator(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D24Tetrakis'
    #Number order
    numberSequenceOrder = (24, 13, 2, 11, 19, 8, 5, 18, 10, 3, 16, 21, 15, 4, 9, 22, 1, 14, 23, 12, 6, 7, 20, 17)
    #Generate Tetrakis Hexahedron
    bpy.ops.mesh.primitive_solid_add(source='8', vTrunc=0.666667, eTrunc=0, snub='None', dual=True, keepSize=True, preset='dt8')
    #Rename Solid
    renameSolid('Solid', diceName)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Generate full rotation sequence from base rotations and sub rotations
    rotationSequence = rotationKisSequenceGeneration(baseRotationsHexahedron, -26.56, 4)
    #Rotate the dice for a face orientation toward X axis for initialization
    bpy.data.objects[diceName].rotation_euler = (math.radians(-26.56), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotationSequence, numberSequenceOrder, 0, 0, (0.774631 * scale), textSize, 0, textImprint, replaceLogo, False)
    
#Function: Rhombic Triacontrahedron Dice 30 Generator
def dice30RhombicGenerator(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D30Rhombic'
    #Number order
    numberSequenceOrder = (30, 19, 5, 24, 23, 28, 18, 27, 22, 2, 11, 14, 16, 6, 10, 7, 8, 3, 1, 12, 26, 15, 25, 21, 29, 20, 17, 13, 4, 9)
    #Generate Rhombic Triacontrahedron
    bpy.ops.mesh.primitive_solid_add(source='12', vTrunc=1, eTrunc=0, snub='None', dual=True, keepSize=True, preset='dr12')
    #Rename Solid
    renameSolid('Solid', diceName)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Rotate the dice for a face orientation toward X axis for initialization
    bpy.data.objects[diceName].rotation_euler = (math.radians(-58.285), 0, math.radians(36))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.data.objects[diceName].rotation_euler = (math.radians(63.43 - 31.715), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Subtransformation initialization
    subTransformationXPositive = (math.radians(31.715), 0, 0)
    subTransformationXNegative = (math.radians(-31.715), 0, 0)
    subTransformationZIncrement = (0, 0, math.radians(72))
    subTransformationZIncrReposition = (0, 0, math.radians(-144))
    subTransformationZDecrement = (0, 0, math.radians(-72))
    subTransformationZDecrReposition = (0, 0, math.radians(144))
    #Dodecahedron-based transformations
    transformationDodecaInitX = (math.radians(180), 0, math.radians(36))
    transformationDodecaXPositive = (math.radians(-63.43), 0, 0)
    transformationDodecaXNegative = (math.radians(63.43), 0, 0)
    transformationDodecaZ = (0, 0, math.radians(72))
    #Generation of the rotation sequence
    rotationSequence = (
        (subTransformationXPositive, subTransformationZIncrement, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrement, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrReposition, transformationDodecaXPositive, 
            transformationDodecaZ, transformationDodecaXNegative, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrement, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrement, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrReposition, transformationDodecaXPositive, 
            transformationDodecaZ, transformationDodecaXNegative, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrement, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrement, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrReposition, transformationDodecaXPositive, 
            transformationDodecaZ, transformationDodecaXNegative, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrement, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrement, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrReposition, transformationDodecaXPositive, 
            transformationDodecaZ, transformationDodecaXNegative, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrement, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrement, subTransformationXNegative),
        (subTransformationXPositive, subTransformationZIncrReposition, transformationDodecaXPositive,
            transformationDodecaInitX, transformationDodecaXPositive, subTransformationXPositive),      
        (subTransformationXNegative, subTransformationZDecrement, subTransformationXPositive),
        (subTransformationXNegative, subTransformationZDecrement, subTransformationXPositive),
        (subTransformationXNegative, subTransformationZDecrReposition, transformationDodecaXNegative, 
            transformationDodecaZ, transformationDodecaXPositive, subTransformationXPositive),    
        (subTransformationXNegative, subTransformationZDecrement, subTransformationXPositive),
        (subTransformationXNegative, subTransformationZDecrement, subTransformationXPositive),
        (subTransformationXNegative, subTransformationZDecrReposition, transformationDodecaXNegative, 
            transformationDodecaZ, transformationDodecaXPositive, subTransformationXPositive),  
        (subTransformationXNegative, subTransformationZDecrement, subTransformationXPositive),
        (subTransformationXNegative, subTransformationZDecrement, subTransformationXPositive),
        (subTransformationXNegative, subTransformationZDecrReposition, transformationDodecaXNegative, 
            transformationDodecaZ, transformationDodecaXPositive, subTransformationXPositive),  
        (subTransformationXNegative, subTransformationZDecrement, subTransformationXPositive),
        (subTransformationXNegative, subTransformationZDecrement, subTransformationXPositive),
        (subTransformationXNegative, subTransformationZDecrReposition, transformationDodecaXNegative, 
            transformationDodecaZ, transformationDodecaXPositive, subTransformationXPositive),  
        (subTransformationXNegative, subTransformationZDecrement, subTransformationXPositive),
        (subTransformationXNegative, subTransformationZDecrement, subTransformationXPositive),
        (subTransformationXNegative, subTransformationZDecrReposition, transformationDodecaXNegative)                                                                                                                             
    )
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotationSequence, numberSequenceOrder, 0, 0, (0.850651 * scale), textSize, 90, textImprint, replaceLogo, False)    
    
#Function: Catalan Pentakis Dodecahedron Dice 60 Generator
def dice60PentakisGenerator(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D60Pentakis'
    #Number order
    numberSequenceOrder = diceNumberAlgorithmSequence(60)
    #Generate Disdyakis Dodecahedron
    bpy.ops.mesh.primitive_solid_add(source='20', vTrunc=0.666667, eTrunc=0, snub='None', dual=True, keepSize=True, preset='dt20')
    #Rename Solid
    renameSolid('Solid', diceName)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Rotate the dice for a face orientation toward X axis for initialization
    bpy.data.objects[diceName].rotation_euler = (math.radians(-58.285 -20.073), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    #Generate full rotation sequence from base rotations and sub rotations
    rotationSequence = rotationKisSequenceGeneration(baseRotationsDodecahedron, -20.073, 5)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotationSequence, numberSequenceOrder, 0, 0, (0.914957 * scale), textSize, 0, textImprint, replaceLogo, False)    

#Function: Catalan Disdyakis Dice 48 Generator
def dice48DisdyakisDodecahedron(scale, textSize, replaceLogo, textImprint):
    #Dice Name
    diceName = 'D48Disdyais'
    #Number order
    numberSequenceOrder = (1, 48, 42, 7, 19, 30, 36, 13, 25, 24, 31, 18, 12, 37, 43, 6, 15, 34, 28, 21, 3, 46, 40, 9, 
        22, 27, 33, 16, 10, 39, 45, 4, 2, 47, 41, 8, 20, 29, 35, 14, 23, 26, 32, 17, 11, 38, 44, 5)
    #Generate Disdyakis Dodecahedron
    bpy.ops.mesh.primitive_solid_add(source='6', size=1, vTrunc=1.0572, eTrunc=0.585786, snub='None', dual=True, keepSize=True, preset='dc6')
    #Rename Solid
    renameSolid('Solid', diceName)
    #Initialize position, rotation and scale
    solidInitializePosition(diceName, scale)
    #Calculate all rotation vectors
    rotationXPositive = (math.radians(12.45), 0, 0)
    rotationXNegative = (math.radians(-12.45), 0, 0)
    rotationXDNegative = (math.radians(-24.9), 0, 0)
    rotationYPositive = (0, math.radians(32.25), 0)
    rotationYNegative = (0, math.radians(-32.25), 0)
    rotationYDNegative = (0, math.radians(-64.5), 0)
    rotationZAPositive = (0, 0, math.radians(90))
    rotationZNegative = (0, 0, math.radians(-135))
    rotationZBPositive = (0, 0, math.radians(45))
    #Rotate the dice for a face orientation toward X axis for initialization
    bpy.data.objects[diceName].rotation_euler = rotationZBPositive
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.data.objects[diceName].rotation_euler = rotationYPositive
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False) 
    bpy.data.objects[diceName].rotation_euler = rotationXPositive
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)    
    #Generate full rotation sequence from base rotations and sub rotations
    rotationSequence = ()
    subRotations = ()
    for rotation in baseRotationsHexahedron:
        rotationSequence += (
            (rotationXDNegative, ),
            (rotationXPositive, rotationYDNegative, rotationXPositive),
            (rotationXDNegative, ),
            (rotationXPositive, rotationYPositive, rotationZAPositive, rotationYPositive, rotationXPositive),
            (rotationXDNegative, ),
            (rotationXPositive, rotationYDNegative, rotationXPositive),
            (rotationXDNegative, ),
        )
        subRotations = (rotationXPositive, rotationYPositive, rotationZNegative)
        for subR in rotation:
            subRotations += (subR, )
        subRotations += (rotationZBPositive, rotationYPositive, rotationXPositive)
        rotationSequence += (subRotations,)
    #Apply the rotation algorithm
    diceAlgorithm(diceName, rotationSequence, numberSequenceOrder, 0, 0, (0.902 * scale), textSize, 0, textImprint, replaceLogo, False)    
    
#######################
### EXPORT FUNCTION ###
#######################

#Function: Export all dice to STL format
def exportDiceToSTLFile():
    #Deselect all objects on the scene
    bpy.ops.object.select_all(action='DESELECT')
    #For each dice in _diceList
    for dName in _diceList:
        dice = bpy.data.objects[dName]
        dice.hide_set(False)
        dice.select_set(True)
        stlPath = _exportPath + dName + ".stl"
        bpy.ops.export_mesh.stl(filepath=stlPath, use_selection=True, check_existing =False)
        dice.select_set(False)    
        dice.hide_set(True)
        
########################
### LOGO REPLACEMENT ###
########################
#Function: Initialize and import STL for logo
def importLogoFromSTLFile(fileName):  
    #Use global variables
    global _logoUploaded
    #Create file pathing
    stlFile = _mainPath + "\\logo\\" + fileName + ".stl"
    #Open font
    bpy.ops.wm.stl_import(filepath=stlFile)
    #Rename logo
    renameSolid(fileName, _logoName)
    #Simplify STL import
    #meshMergeTriangularFaces(_logoName)
    #Prepare new scaling
    maximumSize = max(bpy.data.objects[_logoName].dimensions.x, bpy.data.objects[_logoName].dimensions.y)
    xyScale = _numSize / maximumSize
    #Get the new scale for Z at 1
    zScale = 1 / bpy.data.objects[_logoName].dimensions.z
    #Resize logo
    bpy.data.objects[_logoName].scale = (xyScale, xyScale, zScale)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    #Tell program a logo has been uploaded
    _logoUploaded = True
    
###############################
### INITIALIZATION FUNCTION ###
###############################

#Function: Initialize Blender scene
def initializeBlenderSceneObjects():
    #Delete all meshes from Blender Scene
    for object in bpy.data.objects:
        if(object.type == 'MESH'):
            bpy.data.meshes.remove(object.data)

#####################
### MAIN FUNCTION ###
#####################
    
#Main function
def main():
    #DEBUG
    print("\n### DICE SCRIPT ALGORITHM ###\n")
    
    #Initialize the scene by deleting everything on the scene
    initializeBlenderSceneObjects()
    importLogoFromSTLFile("logo v2")

    #Set font
    setFont("CantaraGotica.ttf")
    #Set the dotted 6 and 9 method
    setDotSign(-0.2, ".")
    #Generate all numbers
    generateAllNumbersMeshes(90)

    #Dice modifiers parameters
    meshBevelGlobalParameters(True, 0.5, 10, 0.55, 0.0, 'EDGES')
    
    #Dice Generation Sequence
    dice4Generator(15, 8, 0, 0.5)
    dice6Generator(8, 16, 6, 0.5)
    dice8Generator(15, 13, 0, 0.5)
    dice10UnitGenerator(13, 12, 99, 0.5)
    dice10DecimalGenerator(13, 9, 99, 0.5)
    dice12Generator(12, 10, 0, 0.5)
    dice20Generator(14, 7, 20, 0.5)
    #Even-faces prism dice
    diceEvenPrismaticGenerator(4, 1, 2, 0.75, 8, 12, 0, 0.5)
    #Odd-faces prism dice
    diceOddPrismaticGenerator(3, 1.25, 2, 0.5, 8, 8, 0, 0.5)
    #Antiprism dices
    diceAntiprismaticGenerator(6, 0.9, 2.25, 0.75, 9, 9, 0, 0, 0.5)
    diceAntiprismaticGenerator(8, 0.9, 2.25, 0.75, 9, 9, 0, 0, 0.5)
    diceAntiprismaticGenerator(10, 1, 2.25, 0.75, 9, 8, 0, 99, 0.5)
    diceAntiprismaticGenerator(10, 1, 2.25, 0.75, 9, 7, 90, 99, 0.5, True)  
    diceAntiprismaticGenerator(12, 1, 2.25, 0.5, 9, 7, 90, 0, 0.5)
    diceAntiprismaticGenerator(14, 1.25, 2.5, 0.5, 9, 7, 90, 0, 0.5) 
    diceAntiprismaticGenerator(16, 1.25, 2.5, 0.5, 9, 7, 90, 0, 0.5) 
    diceAntiprismaticGenerator(18, 1.33, 2.75, 0.5, 9, 7, 90, 0, 0.5) 
    diceAntiprismaticGenerator(20, 1.5, 3, 0.5, 9, 7, 90, 0, 0.5) 
    #Bipyramidal dices --D8 and 10 not generated : looks a lot like Platonic
    diceBipyramidGenerator(6, 2.25, 2.25, 13, 12, 0, 0, 0.5)
    diceBipyramidGenerator(12, 2, 2.1, 13, 8, 90, 0, 0.5)
    diceBipyramidGenerator(14, 2.2, 2.2, 13, 8, 90, 0, 0.5)
    diceBipyramidGenerator(16, 2.4, 2.3, 13, 8, 90, 0, 0.5)
    diceBipyramidGenerator(18, 2.6, 2.4, 13, 8, 90, 0, 0.5)
    diceBipyramidGenerator(20, 2.8, 2.5, 13, 7, 90, 0, 0.5)
    #Rounded-dice
    diceRoundedCubeGenerator(2, 32, 7, 13, 0, 0.5)
    diceRoundedCubeGenerator(4, 32, 7, 13, 0, 0.5)
    #Pseudo antiprism
    dice4PseudoAntiprismaticGenerator(2.5, 0.3, 1.5, 10, 13, 0, 0.5)
    #Rhombic dice
    dice12RhombicGenerator(12, 9, 0, 0.5)
    #Catalan dice
    dice24TetrakisGenerator(15, 6, 0, 0.5)
    dice30RhombicGenerator(15, 6, 0, 0.5)
    dice60PentakisGenerator(20, 6, 0, 0.5)
    dice48DisdyakisDodecahedron(20, 6, 0, 0.5)
    #Shard Dice
    diceShardGenerator(4, 1.0, 2.5, 0.6, 15, 8, 0, 0.5)    
    diceShardGenerator(5, 1.15, 2.5, 0.6, 15, 7, 0, 0.5)
    diceShardGenerator(6, 1.3, 2.5, 0.55, 15, 7, 0, 0.5)
    diceShardGenerator(7, 1.45, 2.5, 0.55, 15, 7, 0, 0.5)
    diceShardGenerator(8, 1.6, 2.5, 0.5, 15, 7, 0, 0.5)
    diceShardGenerator(9, 1.75, 2.5, 0.5, 15, 7, 0, 0.5) 
    
    #Delete all numbers
    clearAllNumbersMeshes()  
    
    #Export to STL
    exportDiceToSTLFile()
  
if __name__ == "__main__":
    main()
#Success !!!