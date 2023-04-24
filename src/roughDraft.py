import pickle, os, random


def initialize():
    ''' this program creates our dictionary and then stores it into a pickle file '''
    document = open("tracker.pickle","wb")
    
    storage = {}
    
    pickle.dump(storage,document)
    
    document.close()
    

def oinitialize():
    dcoument = open("storage.pickle","wb")
    storage = ["blue","system"]
    pickle.dump(storage,dcoument)
    dcoument.close()

def fileChecker():
    ''' this function checks to see if the pickle file exists, and if not it creates it'''
    checker = os.path.isfile("tracker.pickle")
    if checker == False:
        initialize()
    else:
        return True

def ofileChecker():
    ''' this function checks to see if the pickle file exists, and if not it creates it'''
    checker = os.path.isfile("storage.pickle")
    if checker == False:
        oinitialize()
    else:
        return True

def setter(color, theme):
    ofileChecker()
    document = open("storage.pickle","rb")
    storage = pickle.load(document)
    storage.pop()
    storage.pop()
    storage.append(color)
    storage.append(theme)
    document = open("storage.pickle","wb")
    pickle.dump(storage,document)
    document.close()

def getter():
    document = open("storage.pickle","rb")
    storage = pickle.load(document)
    return storage

def storage(name, description, date, priority, position):
    ''' This function stores our values from the user into a dictionary'''
    ''' it first takes all the values submitted by the user and stores it into a List called hold '''
    hold = [name,description,date,priority, position] 
    document = open("tracker.pickle","rb")
    storage = pickle.load(document)
    ''' next it creates a "key" by taking the name submitted by the user, + a unique number '''
    keys = name + str(random.randint(0,100)) + str(len(storage) + 1) + str(random.randint(1,9))
    ''' storing the unique key and value into the dictionary and then storing it into the pickle '''
    storage[keys] = hold
    ndocument = open("tracker.pickle","wb")
    pickle.dump(storage, ndocument)
    document.close()
    ''' returning the unique key '''
    return keys

def getValue(key):
    ''' this function returns the value of the key that was passed '''
    document = open("tracker.pickle","rb")
    storage = pickle.load(document)
    value = storage[key]
    return value

def getAllKeys():
    ''' this function returns ALL keys that have been stored in the pickle file '''
    document = open("tracker.pickle","rb")
    storage = pickle.load(document)
    keylist = []
    keylist = list(storage.keys())
    
    return keylist

def getSpecificKey(name, description, date, priority, position):
    ''' this function searches for a specific key using the values in the dictionary '''
    val = [name, description, date, priority, position]
    document = open("tracker.pickle","rb")
    storage = pickle.load(document)
    key = list(storage.keys())[list(storage.values()).index(val)]
    return key

def deleter(keys):
    ''' deleting a dictionary entry using the keys '''
    document = open("tracker.pickle","rb")
    storage = pickle.load(document)
    del storage[keys]
    ndocument = open("tracker.pickle","wb")
    pickle.dump(storage, ndocument)
    document.close()
    
def editKeys(oldKey, newKey):
    ''' This function lets you edit a key to change its name '''
    document = open("tracker.pickle","rb")
    storage = pickle.load(document)
    storage[newKey] = storage[oldKey]
    deleter(oldKey)
    ndocument = open("tracker.pickle","wb")
    pickle.dump(storage, ndocument)
    document.close()

def editValues(keys, newValue):
    ''' This function changes the values stored in a specific key '''
    document = open("tracker.pickle","rb")
    storage = pickle.load(document)
    storage[keys] = newValue
    ndocument = open("tracker.pickle","wb")
    pickle.dump(storage, ndocument)
    document.close()

