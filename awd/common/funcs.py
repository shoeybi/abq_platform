import hashlib, random


def get_sha1(name):
    """ Get SHA1 key for an input name """
    
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    key  = hashlib.sha1(salt+name).hexdigest()
    return key
