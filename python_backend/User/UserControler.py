from User import User


class UserController():
    def __init__(self):
        self.userList = []
        self.adminList = []

    def populateUserList(self, userList):
        for i in self.userList:
            self.addUser(i)

    def addUser(self, user):
        self.userList.append(user)

    def getUserByName(self, userName):
        for i in self.userList:
            if (i.getName() == userName):
                return i
        return None

    def getUserByEmail(self, email):
        for i in self.userList:
            if(i.getEmail() == email):
                return i
        return None

    def getUserById(self, id):
        for i in self.userList:
            if (i.getId() == id):
                return i
        return None

    def authenticate(self, id, name):
        auth1 = self.getUserById(id)
        auth2 = self.getUserByName(name)
        if auth1 and auth2:
            return auth1 == auth2
        else:
            return False

    def printAllUser(self):
        str = ""
        for i in self.userList:
            print(i)

    # TODO: testingMethod

    def testPopulate(self):
        f = open("User/userData.txt", "r")
        for i in f:
            userData = i.split(",")
            if(len(userData) == 4):
                user = User.User(
                    userId=userData[0], userName=userData[1], password=userData[2], email=userData[3])
                self.addUser(user)
