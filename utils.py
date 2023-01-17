import bpy
import addon_utils
import MCprep_addon
import os

def resolve_namespace(namespace: str, prefix: str = "") -> str:
    resource_pack_dir = os.path.dirname(MCprep_addon.__file__) + "/MCprep_resources/resourcepacks/mcprep_default/"
    assets = resource_pack_dir + "assets"
    owner = "minecraft"
    path = namespace
    if ":" in namespace:
        owner = namespace.split(":")[0]
        path = namespace.split(":")[1]
    return assets + "/" + owner + ("" if prefix == "" else "/" + prefix) + "/" + path