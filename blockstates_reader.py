import json
import os
import random
from . import utils

def get_model_file(namespace: str):
    pass

class ModeledBlockState():
    name: str = ""
    x: int = 0
    y: int = 0
    uv_lock: bool = False

    def __init__(self, data: dict) -> None:
        self.name = data["model"]
        self.x = 0 if "x" in data else data["x"]
        self.y = 0 if "y" in data else data["y"]
        self.uv_lock = False if "uvlock" in data else data["uvlock"]


class BlockStateData():

    data: dict = {}

    def __init__(self, file_name: str) -> None:
        with open(file_name, "r") as file:
            self.data = json.load(file)
    
    def read_variant(self, variant: dict) -> ModeledBlockState:
        if type(variant) == list:
            return self.read_variant(variant[random.randint(0, len(variant) - 1)])
        else:
            return ModeledBlockState(variant)

    def get_required_models(self) -> list[str]:
        out: list[str] = []
        if "variants" in self.data:
            variants: dict = self.data["variants"]
            # Process Variants
            for variant in variants:
                if type(variants[variant]) == list:
                    for possilbitiy in variants[variant]:
                        if not possilbitiy["model"] in out:
                            out.append(possilbitiy["model"])
                else:
                    if not variants[variant]["model"] in out:
                        out.append(variants[variant]["model"])
        elif "multipart" in self.data:
            # Process Conditions
            pass
        return out

    def calculate_model(self, blockstate: dict) -> ModeledBlockState:
        if "variants" in self.data:
            variants: dict = self.data["variants"]
            # Process Variants
            variant = []
            for key in blockstate:
                variant.append(key + "=" + str(blockstate[key]))
            condition = ",".join(variant)
            value: ModeledBlockState = None
            if "" in variants:
                value = self.read_variant(variants[""])
            
            if condition in variants:
                value = self.read_variant(variants[condition])
            
        elif "multipart" in self.data:
            pass
            # Process Conditions



blockstates: list[BlockStateData] = []

def load_block_states(dir: str) -> list[str]:
    models: list[str] = []
    for fname in os.listdir(dir):
        if fname.endswith(".json"):
            data = BlockStateData(dir + "/" + fname)
            for model in data.get_required_models():
                if not model in models:
                    models.append(model)
            blockstates.append(data)
    return models

if __name__ == "__main__":
    for model in load_block_states("blockstates"):
        print(model.replace("minecraft:", ""))