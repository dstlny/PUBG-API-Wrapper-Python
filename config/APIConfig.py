class APIConfig():

    def __init__(self, auth):
        self._auth = auth

    def returnAuthToken(self):
        return self._auth

    def setupAuth(self):
        '''
            Sets up the authentication header which you will be sending to the PUBG API every request.
        '''
        header = {
            "accept": "application/vnd.api+json",
            "Authorization": "Bearer "+self.returnAuthToken()
        }

        return header