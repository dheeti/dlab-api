import hashlib


SESSION_KEY = "session"

class Authenticate(object):

    @staticmethod
    def login(graph, session, args):
        user = graph.nodes.find("User", args["username"])
        if not user: return False, "username does not exist"
        passhash = Authenticate.hashgen(args["username"], args["password"])
        if passhash != user.properties["passhash"]:
            return False, "invalid username-password combination"
        session[SESSION_KEY] = True
        return True, ""
                    
    @staticmethod
    def logout(session):            
        if SESSION_KEY not in session or not session[SESSION_KEY]:
            return False, "not logged in"
        session[SESSION_KEY] = False
        return True, ""

    @staticmethod
    def hashgen(username, password):
        salt = hashlib.sha256(username).hexdigest()
        auth_hash = hashlib.sha256(salt + password).hexdigest()
        return auth_hash
