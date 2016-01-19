import hashlib


class Authenticate(object):

    @staticmethod
    def login(graph, session, args):
        error = "invalid username-password combination"
        user = graph.nodes.find("User", args["username"])
        if not user:
            return False, error
        passhash = Authenticate.hashgen(args["username"], args["password"])
        if passhash != user.properties["passhash"]:
            return False, error
        return True, ""

    @staticmethod
    def hashgen(username, password):
        salt = hashlib.sha256(username).hexdigest()
        auth_hash = hashlib.sha256(salt + password).hexdigest()
        return auth_hash
