import string
import random
import re
from collections import Counter



def count_common_characters(str1, str2):
    # Create a counter for both strings
    counter1 = Counter(str1)
    counter2 = Counter(str2)

    # Find the common characters between the two strings
    common_chars = counter1 & counter2  # Intersection of counters keeps minimum counts

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
    fileName = fileName + ".txt"
    fileName = "passwordDetector.txt"
    with open(fileName, "a+") as file:
        filePasswordGen = file.read()
        print("bbb" + filePasswordGen)
        file.close()
    return filePasswordGen


def writeOnFile(fileName, passwordName, passwordGenerated):
    fileName = "passwordDetector.txt"
    with open(fileName, 'a+') as file:
        file.writelines(str(passwordName) + ":\t" + str(passwordGenerated) + "\n")
        file.close()



def generatePassword(lenOfPassword):
    passwordGenerated = "".join(random.sample(string.printable[11:94], k=lenOfPassword))
    return passwordGenerated



fileName = input("Where you want to save the password?")
filePasswordGen = openFiletxt(fileName)
passwordName = input("Password Name?")

lenOfPassword = 16
# print(string.printable[:62]) Numbers and leters
numbers = string.printable[0:10]
lowersCharacters = string.printable[10:36]
upperCharacters = string.printable[36:62]
specialsCharacters = string.printable[63:94]

# PasswordGenerate random from random.sample
passwordGenerated = "c$G)mNP7dgkI#jZe"


while(True):
    print ("aaaaaaa" + filePasswordGen)
    if passwordGenerated not in filePasswordGen:
        break
    passwordGenerated = generatePassword(lenOfPassword)


# Count Characters
numbersInPassword = count_common_characters(passwordGenerated, numbers)
lowerCharactersInPassword = count_common_characters(passwordGenerated, lowersCharacters)
upperCharactersInPassword = count_common_characters(passwordGenerated, upperCharacters)
specialsCharactersInPassword = count_common_characters(passwordGenerated, specialsCharacters)

# if no specials Characters
if specialsCharactersInPassword == 0:
    while (True):
        randomNumberAttempt = random.randrange(0, 15)
        passwordGenerated = replacer(passwordGenerated, "".join(random.sample(specialsCharacters, k=1)),
                                     randomNumberAttempt)
        specialsCharactersInPassword += 1
        break

# if no numbers
if numbersInPassword == 0:
    while True:
        randomNumberAttempt = random.randrange(0, 15)

        #
        if specialsCharactersInPassword <= 1 and passwordGenerated[randomNumberAttempt] in specialsCharacters:
            continue

        print("rand " + str(randomNumberAttempt))
        passwordGenerated = replacer(passwordGenerated, "".join(random.sample(numbers, k=1)),
                                     randomNumberAttempt)
        numbersInPassword = +1
        break

# if no upper letters
if upperCharactersInPassword == 0:
    while True:
        randomNumberAttempt = random.randrange(0, 15)

        if specialsCharactersInPassword <= 1 and passwordGenerated[randomNumberAttempt] in specialsCharacters:
            continue

        if numbersInPassword <= 1 and passwordGenerated[randomNumberAttempt] in numbersInPassword:
            continue

        if passwordGenerated[randomNumberAttempt] in string.printable[10:36]:
            passwordGenerated = replacer(passwordGenerated, passwordGenerated[randomNumberAttempt].upper(),
                                         randomNumberAttempt)
            break

print(passwordGenerated)
writeOnFile(fileName, passwordName, passwordGenerated)




