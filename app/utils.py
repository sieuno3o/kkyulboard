import hashlib, json

def sha512_hash(text):
    encoded_text = text.encode('utf-8')
    sha512 = hashlib.sha512()
    sha512.update(encoded_text)
    hashed_text = sha512.hexdigest()
    return hashed_text

def read_from_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data
    