import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

database = firestore.client()

# Add documents with auto IDs
data = {'name':'Bobby Jones', 'age': 32, 'employed': True, 'occupation':'librarian'}
database.collection('People').add(data)

# Set documents with known IDs
data = {'name':'Mary Jane', 'age': 22, 'employed': True, 'occupation':'waitress'}
database.collection('People').document('maryjane').set(data) # document reference

# data = {'name':'Robert Downey Jr', 'age': 31, 'employed': True, 'occupation':'actor'}
# database.collection('People').document('robertdowney').set(data) # document reference

# data = {'name':'Peter Parker', 'age': 19, 'employed': True, 'occupation':'hero'}
# database.collection('People').document('peterparker').set(data) # document reference

# Merging
database.collection('People').document('maryjane').set({'residence':'New York'}, merge = True) 

# Set documents with auto IDs
database.collection('People').document().set(data) # document reference

# Remember, lines 15 and 19 are demonstration purposes.


# Read data
# Reading document with a known ID
result = database.collection('People').document('maryjane').get()
if result.exists:
    print(result.to_dict()) #Dictates data as a readable

# Retrieve documents in a collection
docs = database.collection('People').get()
for doc in docs:
    print(doc.to_dict())

# Querying
docs = database.collection('People').where('age','>',20).get()
for doc in docs:
    print(doc.to_dict())


# Updating data - known ID
database.collection('People').document('peterparker').update({'age':44})
database.collection('People').document('robertdowney').update({'age':49})
database.collection('People').document('maryjane').update({'age':46,'employed': False, 'occupation':'none'})

# Updating data - unknown ID
docs = database.collection('People').get()
for doc in docs:
    if doc.to_dict()['age'] >= 35:
        key = doc.id
        database.collection('People').document(key).update({'agegroup': 'middle age'})

# Improves cost-effectiveness if multiple documents are present.
docs = database.collection('People').where('age', '>=', '45').get()
for doc in docs:
    if doc.to_dict()['age'] >= 35:
        key = doc.id
        database.collection('People').document(key).update({'agegroup': 'middle age + 1'})

# Delete data - known ID
database.collection('People').document('maryjane').delete()

# Delete docs - unknown ID
docs = database.collection('People').get()
for doc in docs:
    key = doc.id
    database.collection('People').delete()  #Deleting one by one

#Cost effective with querying
docs = database.collection('People').where('age', '>=', 50).get()
for doc in docs:
    key = doc.id
    database.collection('People').document(key).delete()