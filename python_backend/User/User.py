class User():
    def __init__(self, userId, userName, password, email=""):
        self.userId = userId
        self.userName = userName
        self.password = password
        self.email = email
        # {
        # vocabId: {
        # errorCount: int,
        # isSaved: boolean
        # }
        # }
        self.userFile = {}
        self.isAdmin = False

    def populateUserFile(self, list):
        return None

    def getName(self):
        return self.userName

    def checkPassword(self, password):
        return (self.password == password)

    def getEmail(self):
        return self.email

    def getId(self):
        return self.userId

    def isAdmin(self):
        return self.isAdmin

    def getData(self):
        return {"isAdmin": self.isAdmin, "userFile": self.userFile}

    def to_dictionary(self):
        json = {}
        json.setdefault("username", self.userName)
        json.setdefault("userId", self.userId)
        json.setdefault("email", self.email)
        json.setdefault("userFile", self.userFile)
        json.setdefault("isAdmin", self.isAdmin)
        return json

    def __str__(self):
        return self.userId + "\n" + self.userName + "\n" + self.password + "\n" + self.email

    def __eq__(self, user):
        return self.userName == user.getName() and user.checkPassword(self.password) and self.email == user.email and self.userId == user.getId()
