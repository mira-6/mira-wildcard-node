import re
import random
import pathlib

class MiraWildcard:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "prompt": ("STRING", {"multiline": True}),
            "seed": ("INT", {"default": 0, "display": "number"}) 
            }}
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "parse"
    CATEGORY = "Mira Nodes"

    def parse(self, prompt, seed):
        def loadfile(filename):
            with open(filename, "r", encoding="utf-8") as file:
                return file.read().splitlines()

        def parsestring(text, seed):
            ### Wildcards            
            for wildcard in re.findall(r"<wildcard:.{0,}?>", text):
                filename = wildcard[10:-1]
                if ".txt" not in filename: # Compatibility with Swarm
                    filename = filename + ".txt"
                filecontents = loadfile(pathlib.Path(pathlib.Path.cwd(),"input","wildcards",filename))
                # Pick a string
                random.seed(seed)
                choice = random.choice(filecontents)
                seed = seed + 1
                if re.search("<wildcard:.*>", choice):
                    choice = parsestring(choice, seed)
                text = text.replace(wildcard, choice, 1)

            ### Random Prompt
            # Handle {a|b|c} syntax
            for wildcard in re.findall(r"{.+?}", text):
                terms = wildcard[1:-1].split("|")

                random.seed(seed)
                choice = random.choice(terms)
                seed = seed + 1
                text = text.replace(wildcard, choice, 1)

            # Handle <random:a,b,c> syntax
            for wildcard in re.findall(r"<random:.{0,}?>", text):
                if "||" not in wildcard:
                    terms = wildcard[8:-1].split(",")
                else:
                    terms = wildcard[8:-1].split("||")
                random.seed(seed)
                choice = random.choice(terms)
                seed = seed + 1
                text = text.replace(wildcard, choice, 1)

            return text

            
        result = parsestring(prompt, seed) 
        print(f"Generated Prompt: {result}")
        return (result,)
    

NODE_CLASS_MAPPINGS = {
    "MiraWildcard": MiraWildcard
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MiraWildcard": "MiraWildcard"
}