import base64
import zlib

import ujson

from utils.useful import Result

FILENAME = "save.sav"




def write_to_save(dictionary_object: dict):
    """Writes a dictionary object to a localfile."""
    json_str = ujson.dumps(dictionary_object)
    compressed = zlib.compress(json_str.encode(),level=9) # reduce the most amount of space on player's computer
    encoded = base64.b85encode(compressed)

    try:
        with open(FILENAME,"wb") as f:
            f.write(encoded)
            #auto closes file
    except OSError:
        return Result(False,"Error writing to file, it might be read only.")
    return Result(True)

def read_from_save():
    print()
    try:
        with open(FILENAME,"rb") as f:
            filedata = f.read()
            # automatically closes file
    except FileNotFoundError:
        return Result(False,"The save file has not been found.")

    decoded = base64.b85decode(filedata)
    decompressed = zlib.decompress(decoded)
    as_object = ujson.loads(decompressed.decode())
    return Result(True, value=as_object)

