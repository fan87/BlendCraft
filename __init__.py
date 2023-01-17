bl_info = {
    "name": "BlendCraft",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "category": "Object",
    "location": "3D window toolshelf > BlendCraft tab",
    "description": "Synchronizes your Minecraft world with blender",
    "wiki_url": "https://github.com/fan87/BlendCraft"
}

import os
import bpy
try:
    import MCprep_addon
    import MCprep_addon.spawner.mcmodel
except ImportError:
    bl_info["warning"] = "MCprep is required for this addon!"

from . import blockstates_reader
from . import utils
import bmesh

##### Operations #####
class BCLoadModels(bpy.types.Operator):
    bl_idname = "bc.load_models"
    bl_label = "Load Models"
    def execute(self, context):
        if "BlendCraft Assets" in bpy.data.collections:
            for object in bpy.data.collections["BlendCraft Assets"].objects:
                bpy.data.objects.remove(bpy.data.objects[object.name_full])
                
            bpy.data.collections.remove(bpy.data.collections["BlendCraft Assets"])
        collection: bpy.types.Collection = bpy.data.collections.new(name = "BlendCraft Assets")
        bpy.context.scene.collection.children.link(collection)
        amount = 0
        for model in blockstates_reader.load_block_states(os.path.dirname(__file__) + "/blockstates"):
            object = MCprep_addon.spawner.mcmodel.add_model(utils.resolve_namespace(model, "models") + ".json", model.replace(":", "__").replace("/", "-"))
            collection.objects.link(object)
            bpy.context.scene.collection.objects.unlink(object)
            print(model)
            amount += 1
            if amount > 20:
                break
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()

######################


##### Side Panel Section #####
class BCSyncControl(bpy.types.Panel):
    bl_label = "Synchronization Control"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BlendCraft"
    bl_idname = "BCSyncControl"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hello, World!")
        layout.operator("bc.load_models", text = "Setup Scene")


class BCSceneControl(bpy.types.Panel):
    bl_label = "Scene Control"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BlendCraft"
    bl_idname = "BCSceneContro"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hello, World!")
###############################

    
##### Driver Section #####
def driver_mode(self):
    return self.mode

drivers = {
    "mode": driver_mode
}

def register_drivers():
    for key in drivers:
        bpy.app.driver_namespace[key] = drivers[key]
def unregister_drivers():
    for key in drivers:
        bpy.app.driver_namespace[key] = None
##########################


classes = [
    BCSyncControl,
    BCSceneControl,
    BCLoadModels,
]

def register_classes():
    for clazz in classes:
        bpy.utils.register_class(clazz)

def unregister_classes():
    for clazz in classes:
        bpy.utils.unregister_class(clazz)

def register():
    register_drivers()
    register_classes()



def unregister():
    unregister_drivers()
    unregister_classes()

if __name__ == "__main__":
    register()
