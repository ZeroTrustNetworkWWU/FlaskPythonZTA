# A file that handles connection to the database

import sqlite3
from TrustEngineExceptions import InvalidLogin
from TokenHandler import TokenHandler
from datetime import datetime, timedelta

class UserDataHandler:
    def __init__(self, dbName):
        self.dbName = dbName
        self.tokenHandler = TokenHandler()

        with sqlite3.connect(self.dbName) as conn:
            cursor = conn.cursor()

            # Create the needed tables if they don't exist
            cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, role TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS sessions (username TEXT, session TEXT, expiration TEXT)")

            # add the admin user if it doesn't exist TODO remove this
            if not self.userExists("user1"):
                cursor.execute("INSERT INTO users VALUES (?, ?, ?)", ("user1", "admin", "admin"))
            
            conn.commit()

    def getRoleFromUser(self, user):
        with sqlite3.connect(self.dbName) as conn:
            cursor = conn.cursor()
            role = cursor.execute("SELECT role FROM users WHERE username=?", (user,)).fetchone()[0]

        return role
    
    def getRoleFromSession(self, session):
        with sqlite3.connect(self.dbName) as conn:
            cursor = conn.cursor()
            username = cursor.execute("SELECT username FROM sessions WHERE session=?", (session,)).fetchone()[0]

        return self.getRoleFromUser(username)
    
    def validateUser(self, data):
        if "login" in data.keys():
            user = data["login"].get("user", None)
            password = data["login"].get("password", None)
            if not self.userExists(user):
                raise InvalidLogin("Invalid username")
            return True
        else:
            return False
        
    def validateSession(self, session):
        if session is None:
            return False
        
        with sqlite3.connect(self.dbName) as conn:
            cursor = conn.cursor()
            username, expiration = cursor.execute("SELECT username, expiration FROM sessions WHERE session=?", (session,)).fetchone()

        if username is None or expiration is None:
            return False

        if not self.userExists(username) or datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S") < datetime.now():
            return False

        return True
        
    def getNewSessionToken(self, user):
        # Get the session token
        token = self.tokenHandler.getNewToken()
        expiration = datetime.now() + timedelta(minutes=30)

        # Add the session token to the database making sure to remove any previous sessions for the user
        with sqlite3.connect(self.dbName) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE username=?", (user,))
            cursor.execute("INSERT INTO sessions VALUES (?, ?, ?)", (user, token, expiration.strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

        return token
    
    def userExists(self, user):
        with sqlite3.connect(self.dbName) as conn:
            cursor = conn.cursor()
            username = cursor.execute("SELECT * FROM users WHERE username=?", (user,))

        return username.fetchone() is not None