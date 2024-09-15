import string
import random
import re
from collections import Counter


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


def openFiletxt(fileName):
    # if not exist create a file and open with read and write
    fileName = fileName + ".txt"
    fileName = "passwordDetector.txt"
    with open(fileName, "a+") as file:
        # read file
        filePasswordGen = file.read()
        file.close()
    return filePasswordGen


def writeOnFile(fileName, passwordName, passwordGenerated):
    fileName = "passwordDetector.txt"
    with open(fileName, 'a+') as file:
        file.writelines(str(passwordName) + ":\t" + str(passwordGenerated) + "\n")
        file.close()


def generatePassword(lenOfPassword, ):
    # Generate the Password
    characters = string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation
    passwordGenerated = ''.join(random.choice(characters) for i in range(lenOfPassword))
    return passwordGenerated


def __verifyIntegers(phrase, max=None):
    # verify if is integer and if max is not none compare if is equal or less
    while True:
        value = input(phrase)
        try:
            integerValue = int(value)
        except ValueError:
            print(ValueError)
        else:
            if not max or integerValue <= max:
                return integerValue
            else:
                print("Doesn't match")


def isAlreadyUsedPassword(filePasswordGen, passwordGenerated, lenOfPassword):
    print("isAlreadyUsedPassword")
    print(f"file {filePasswordGen} | passwordGenerated {passwordGenerated}")
    if passwordGenerated not in filePasswordGen:
        return passwordGenerated
    passwordGenerated = generatePassword(lenOfPassword)
    isAlreadyUsedPassword(filePasswordGen, passwordGenerated, lenOfPassword)


def verifyPasswordWithAllCharacters(passwordGenerated, lenOfPassword):
    specialsCharactersInPassword = count_common_characters(passwordGenerated, string.punctuation)
    print(specialsCharactersInPassword)
    numbersInPassword = count_common_characters(passwordGenerated, string.digits)
    print(numbersInPassword)
    upperCharactersInPassword = count_common_characters(passwordGenerated, string.ascii_uppercase)
    lowerCharactersInPassword = count_common_characters(passwordGenerated, string.ascii_lowercase)
    print(upperCharactersInPassword)
    if specialsCharactersInPassword == 0:
        while (True):
            randomNumberAttempt = random.randrange(0, lenOfPassword)
            passwordGenerated = replacer(passwordGenerated, "".join(random.sample(string.punctuation, k=1)),
                                         randomNumberAttempt)
            specialsCharactersInPassword += 1
            break

        # if no numbers
    if numbersInPassword == 0:
        while True:
            randomNumberAttempt = random.randrange(0, lenOfPassword)

            #
            if specialsCharactersInPassword <= 1 and passwordGenerated[randomNumberAttempt] in string.punctuation:
                continue

            print("rand " + str(randomNumberAttempt))
            passwordGenerated = replacer(passwordGenerated, "".join(random.sample(string.digits, k=1)),
                                         randomNumberAttempt)
            numbersInPassword = +1
            break

    # if no upper letters
    if upperCharactersInPassword == 0:
        while True:
            randomNumberAttempt = random.randrange(0, lenOfPassword)

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
            randomNumberAttempt = random.randrange(0, lenOfPassword)
            passwordGenerated = replacer(passwordGenerated, passwordGenerated[randomNumberAttempt].lower(),
                                         randomNumberAttempt)
            break
    return passwordGenerated


def __init__():
    fileName = input("Where you want to save the password?")
    filePasswordGen = openFiletxt(fileName)
    passwordName = input("Password Name?")
    lenOfPassword = __verifyIntegers("How long is the password?")

    passwordGenerated = isAlreadyUsedPassword(filePasswordGen, generatePassword(lenOfPassword), lenOfPassword)
    password = verifyPasswordWithAllCharacters(passwordGenerated, lenOfPassword)



__init__()

# print(passwordGenerated)
# writeOnFile(fileName, passwordName, passwordGenerated)
