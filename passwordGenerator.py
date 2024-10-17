import base64
import hashlib
import string
import random
import os
from collections import Counter
import json
from cryptography.fernet import Fernet
from tkinter import filedialog as fd

attributesToCheck = ['Name', 'UserName', "MaxCharacters", "Password"]


def count_common_characters(str1, str2):
    # Create a counter for both strings
    counter1 = Counter(str1)
    counter2 = Counter(str2)

    # Find the common characters between the two strings
    # Intersection of counters keeps minimum counts
    common_chars = counter1 & counter2

    # Sum the counts of all common characters
    return sum(common_chars.values())


def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]

def importFile():
    while True:
        file_path = fd.askopenfilename(title="Select a file")

        if file_path:
            print(file_path[-4:])
            if file_path[-4:] == ".txt":
                with open(file_path, "r+") as file:
                    # read file
                    filePasswordGen = file.read()
                    if filePasswordGen and filePasswordGen.strip() != "":
                        for line in file:
                            newPassword = None
                            load = json.loads(line)
                            if load and all(k in load for k in attributesToCheck):
                                newPassword = PasswordGenerator(load['Name'], load['UserName'], load["MaxCharacters"])
                                newPassword.password = load["Password"]
                                flag = True
                                if "Hash" in load:
                                    newPassword.Hash = load["Hash"]
                                passwordsKeeper.addMember(newPassword)

                    file.close()
                    return file_path, True


def writeOnFile(path, objectToDict):
    # Open the file and write the password in format json with name and username

    with open(path, 'a+') as file:
        person = objectToDict.to_dict()
        json.dump(person, file)
        file.write("\n")
    file.close()


def verifyIntegers(phrase):
    # verify if is integer and if max is not none compare if is equal or less
    integerValue = 0
    while True:
        value = input(phrase)
        try:
            integerValue = int(value)
            break
        except ValueError:
            print(ValueError)

    return integerValue


def generate_key():
    key = Fernet.generate_key()
    return key.decode()  # Return the key as a string


# Encrypt the password
def encryptPassword(password: str, key: str) -> str:
    # Create a Fernet object with the provided key (converting the key back to bytes)
    fernet = Fernet(key.encode())
    # Encode the password to bytes and then encrypt it
    encrypted_password = fernet.encrypt(password.encode())
    # Convert the encrypted bytes to a string (base64 encoding)
    return encrypted_password.decode()


def decryptPassword(encrypted_password: bytes, key: bytes) -> str:
    # Create a Fernet object with the provided key
    fernet = Fernet(key)
    # Decrypt the password and decode it back to a string
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password


class PasswordGenerator:
    def __init__(self, name, userName, maxCharacters):
        self.Name = name
        self.UserName = userName
        self.MaxCharacters = maxCharacters
        self.Password = ""
        self.Hash = ""

    def generatePassword(self):
        characters = string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation
        passwordGenerated = ''.join(random.choice(characters) for i in range(self.MaxCharacters))
        self.Password = self.verifyPasswordWithAllCharacters(passwordGenerated)
        # Generate a key (This key should be stored securely!)
        key = generate_key()
        encryptedpassword = encryptPassword(self.Password, key)

        self.Hash = encryptedpassword
        print(f"NEVER LOOSE THIS KEY: {key}")

    def verifyPasswordWithAllCharacters(self, passwordGenerated):
        specialsCharactersInPassword = count_common_characters(passwordGenerated, string.punctuation)
        numbersInPassword = count_common_characters(passwordGenerated, string.digits)
        upperCharactersInPassword = count_common_characters(passwordGenerated, string.ascii_uppercase)
        lowerCharactersInPassword = count_common_characters(passwordGenerated, string.ascii_lowercase)
        if specialsCharactersInPassword == 0:
            while (True):
                randomNumberAttempt = random.randrange(0, self.MaxCharacters)
                passwordGenerated = replacer(passwordGenerated, "".join(random.sample(string.punctuation, k=1)),
                                             randomNumberAttempt)
                specialsCharactersInPassword += 1
                break

            # if no numbers
        if numbersInPassword == 0:
            while True:
                randomNumberAttempt = random.randrange(0, self.MaxCharacters)

                #
                if specialsCharactersInPassword <= 1 and passwordGenerated[randomNumberAttempt] in string.punctuation:
                    continue

                passwordGenerated = replacer(passwordGenerated, "".join(random.sample(string.digits, k=1)),
                                             randomNumberAttempt)
                numbersInPassword = +1
                break

        # if no upper letters
        if upperCharactersInPassword == 0:
            while True:
                randomNumberAttempt = random.randrange(0, self.MaxCharacters)

                if specialsCharactersInPassword <= 1 and passwordGenerated[randomNumberAttempt] in string.punctuation:
                    continue

                if numbersInPassword <= 1 and passwordGenerated[randomNumberAttempt] in numbersInPassword:
                    continue

                if passwordGenerated[randomNumberAttempt] in string.ascii_uppercase:
                    passwordGenerated = replacer(passwordGenerated, passwordGenerated[randomNumberAttempt].upper(),
                                                 randomNumberAttempt)
                    break
        if lowerCharactersInPassword == 0 and upperCharactersInPassword > 1:
            while True:
                randomNumberAttempt = random.randrange(0, self.MaxCharacters)
                passwordGenerated = replacer(passwordGenerated, passwordGenerated[randomNumberAttempt].lower(),
                                             randomNumberAttempt)
                break
        return passwordGenerated

    def to_dict(self):
        if isinstance(self, PasswordGenerator):
            return {"Name": self.Name, "UserName": self.UserName, "MaxCharacters": self.MaxCharacters,
                    "Password": self.Password, "Hash": self.Hash}
        raise TypeError("Type not serializable")


class PasswordsKeeper:
    def __init__(self):
        self.safe = []

    def addMember(self, PasswordFile):
        self.safe.append(PasswordFile)


passwordsKeeper = PasswordsKeeper()


def __init__():
    print("What is your Bd?")
    fileBd, flag = importFile()
    while True:
        choose = verifyIntegers("1 - Get Password\n2 - Generate Password ")
        if choose == 1:
            siteName = input("What is the site name?")
            key = str(input("What is the the key?"))
            chosenSite = next((x for x in passwordsKeeper.safe if x.Name == siteName), None)
            if chosenSite:
                decryptedPassword = decryptPassword(chosenSite.Hash, key)
                print(f"SITE: {chosenSite.Name}\nUSER NAME:{chosenSite.UserName}\nYOUR PASSWORD IS {decryptedPassword}")

            else:
                print("Site not found")

        if choose == 2:
            siteName = input("Site name?")
            userName = input("User Name?")
            lenOfPassword = verifyIntegers("How long is the password?")
            generatorPassword = PasswordGenerator(siteName, userName, lenOfPassword)
            generatorPassword.generatePassword()
            passwordsKeeper.addMember(generatorPassword)
            writeOnFile(fileBd, generatorPassword)
        else:
            break


__init__()
