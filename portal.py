from os import path
from json.decoder import JSONDecodeError
import sys
import json

'''
@author: suraj kakkad (spk101)
'''
'''
To Do: Define a new user for the system along with the user’s password, both strings.

The username cannot be an empty string. The password may be an empty string.

Test program:

portal AddUser myname mypassword
The program should return one of:

Success
Error: user exists - if the user already exists.
Error: username missing - if the username is an empty string.
'''


def AddUser(user_name, password):
    # print('AddUser')
    if user_name == "":
        print('Error: username missing')
        return

    if not path.exists('./tables/userlist.json'):
        open("./tables/userlist.json", "w+")

    file = open("./tables/userlist.json", "r")

    try:
        # loading users list from the json file
        users = json.load(file)
        # checking if user already exists..
        if user_check(user_name):
            print('Error: user exists')
            return
        # add the new user
        users[user_name] = {"UserName": user_name,
                            "Password": password, "Domains": []}

        file = open("./tables/userlist.json", "w+")
        # adding the new users dump into the json file
        json.dump(users, file, indent=4)

    except JSONDecodeError:
        # if the file is empty (first entry)
        file = open("./tables/userlist.json", "w+")
        users = {user_name: {"UserName": user_name,
                             "Password": password, "Domains": []}}
        json.dump(users, file, indent=4)
    # User added acknolegment.. Success
    print('Success')


'''
To Do: Test whether a user can perform a specified operation on an object.

The logic in this function in pseudocode is:

for d in domains(user)
	for t in types(object)
		if access[d][t] contains operation
			return true
return false
Test program:

portal CanAccess operation user object
The program will check whether the user is allowed to perform the specified operation on the object. That means that there exists a valid access right for an operation in some (domain, type) where the user is in domain and the object is in the corresponding type.

As with AddAccess, the program will accept three strings.

Note that the parameters here are user names and object names, not user domains and object types.

The program will return:

Success - if the access is permitted
Error: access denied - for all other cases
'''


def CanAccess(operation, user_name, object_name):
    # print('CanAccess')
    # empty user_name
    if user_name == "":
        print("Error: Username empty")
        return
    # empty object name
    if object_name == "":
        print("Error: Object name empty")
        return
    # empty operation name
    if operation == "":
        print("Error: Operation name empty")
        return

    # check if the file exists in tables folder
    if not path.exists('./tables/userlist.json'):
        open("./tables/userlist.json", "w+")
        return

    if not user_check(user_name):
        print("Error: Username invalid")
        return

    # Check what domains the user is a part of
    file = open("./tables/userlist.json", "r")
    try:
        users = json.load(file)

        user_domains = users[user_name]["Domains"]

    except JSONDecodeError:
        # file is empty
        print("Error: Username invalid")
        return

    # check if the file exists for permissions if not retrun
    if not path.exists('./tables/permissions.json'):
        open("./tables/permission.json", "w+")
        return
    # check if operation exists in permission.json else report error
    if not permission_check(operation):
        print("Error: Operation invalid")
        return

    # check what domains are associated with that operation
    file = open("./tables/permissions.json", "r")
    try:
        permissions = json.load(file)
        permission_domains = permissions[operation]["Domains"]

    except JSONDecodeError:
        # file is empty
        print("Error: Operaton invalid")
        return

    # check which of the user_domains are in permission domains
    shared_domains = []
    for u_domain in user_domains:
        if u_domain in permission_domains:
            shared_domains.append(u_domain)

    # find the types associated
    intersect_types = []
    for s_domain in shared_domains:
        for Type in permission_domains[s_domain]:
            # check if it exists in our types json
            if Type not in intersect_types and type_check(Type):
                intersect_types.append(Type)

    # get the types
    # check if the file exists
    if not path.exists('./tables/types.json'):
        open("./tables/types.json", "w+")
        return

    # get types
    file = open("./tables/types.json", "r")
    try:
        types = json.load(file)

    except JSONDecodeError:
        # empty file
        print("Error: Object invalid")
        return

    # go through all of the shared types and see if object exists in it
    for Type in intersect_types:
        if object_name in types[Type]["Objects"]:
            print("Success")
            return
    print("Error: Access Denied")


'''
To Do: Define an access right: a string that defines an access permission of a domain to an object. The access permission can be an arbitrary string that makes sense to the service.

The domain name and type name must be non-empty strings.

If the domain name or type names do not exist then they will be created.

This is the key function that builds the access control matrix of domains and types.

Test program:

portal AddAccess operation domain_name type_name
The program will accept three strings and report

Success - if the operation was added to the access control matrix
Error: missing operation - if the operation is null
Error: missing domain - if the domain is null
Error: missing type - if the type is null
'''


def AddAccess(operation, domain_name, type_name):
    # print('AddAccess')
    # check if domain and type are not null
    if domain_name == "":
        print("Error: missing domain")
        return
    if type_name == "":
        print("Error: missing type")
        return
    if operation == "":
        print("Error: missing operation")
        return

    # Check if domain name exists
    if not domain_check(domain_name):

        # check if the file exists
        if not path.exists('./tables/domainlist.json'):
            open("./tables/domainlist.json", "w+")
        file = open("./tables/domainlist.json", "r")
        # create the domain
        try:
            domains = json.load(file)
            # add to domains (dont have to check if it exists bc we already did)
            domains[domain_name] = {"Name": domain_name,
                                    "Users": []}
        except JSONDecodeError:
            # emtpy file
            domains = {domain_name: {"Name": domain_name,
                                     "Users": []}}
        file = open("./tables/domainlist.json", "w+")
        json.dump(domains, file, indent=4)

    # Check if type name exists
    if not type_check(type_name):
        # create the type

        # check if the file exists
        if not path.exists('./tables/types.json'):
            open("./tables/types.json", "w+")
        file = open("./tables/types.json", "r")
        try:
            types = json.load(file)
            # add to domains (dont have to check if it exists bc we already did)
            types[type_name] = {"Name": type_name, "Objects": []}
        except JSONDecodeError:
            # emtpy file
            types = {type_name: {"Name": type_name, "Objects": []}}
        file = open("./tables/types.json", "w+")
        json.dump(types, file, indent=4)

    # check if the permissions json exists
    if not path.exists('./tables/permissions.json'):
        open("./tables/permissions.json", "w+")

    file = open("./tables/permissions.json", "r")
    try:
        permissions = json.load(file)
        # File is not empty

        # check if permission exists
        if operation not in permissions:
            # add operation into permissions
            permissions[operation] = {"Name": operation,
                                      "Domains": {domain_name: [type_name]}}
        else:

            # check if the domain exists already
            if domain_name in permissions[operation]["Domains"]:
                # check if the type exists already
                if type_name not in permissions[operation]["Domains"][domain_name]:
                    # append the new type to the list
                    permissions[operation]["Domains"][domain_name].append(
                        type_name)
            else:
                # New domain so create new list
                permissions[operation]["Domains"][domain_name] = [type_name]

    except JSONDecodeError:
        # File is empty
        permissions = {operation: {"Name": operation,
                                   "Domains": {domain_name: [type_name]}}}

    file = open("./tables/permissions.json", "w+")
    json.dump(permissions, file, indent=4)

    # add it to the Access Permissions in the Domain
    print("Success")


'''
To Do: List all the users in a domain.

The group name must be a non-empty string.

Test program:

portal DomainInfo domain_name
The program should report

List all the users in that domain, one per line
Nothing if the domain does not exist or there are no users in a domain.
Error: missing domain - if the domain name is an empty string.
Sample output:

alice
bob
charles
david
ellen

with no leading tabs or spaces. This output format fits into the Unix tools philosophy, which makes the output suitable for input in a pipeline of commands.
'''

# need to check for domain_name if its dne


def DomainInfo(domain_name):
    # print('DomainInfo')
    # Check if domain name is empty report error if so
    if domain_name == "":
        print("Error: missing domain")
        return
    # Check if domainlist file exists. else create json file
    # and return (DO NOTHING IF DOMAIN DNE)
    if not path.exists('./tables/domainlist.json'):
        open("./tables/domainlist.json", "w+")
        return
    # READ FILE AND LOAD JSON DATA
    file = open('./tables/domainlist.json', 'r')

    try:
        domains = json.load(file)
        # IF DOMAIN_NAME IN DOMAINS (DICT)
        # PRINT USERS OF THAT DOMAIN
        if domain_name in domains:
            for user in domains[domain_name]["Users"]:
                print(user)

    except JSONDecodeError:
        return


'''
To Do:Assign a user to a domain. Think of it as adding a user to a group.

If the domain name does not exist, it is created. If a user does not exist, the function should return an error.

A user may belong to multiple domains.

The domain name must be a non-empty string.

Test program:

portal SetDomain user domain_name
The program should report

Success
Error: no such user - if the user does not exist
Error: missing domain - if the domain name is an empty string
'''


def SetDomain(user_name, domain):
    # print('SetDomain')
    # if domain is empty report error
    if domain == '':
        print("Error: missing domain")
        return
    # check if user exists else report error
    if not user_check(user_name):
        print("Error: no such user")
        return
    # check if domainlist exists if not create json file
    if not path.exists('./tables/domainlist.json'):
        open("./tables/domainlist.json", "w+")
    # read file and load json data
    file = open("./tables/domainlist.json", "r")

    try:
        domains = json.load(file)
        # write to file
        file = open("./tables/domainlist.json", "w+")

        if domain not in domains:
            domains[domain] = {"Domain": domain,  "Users": [user_name]}
        else:
            if user_name not in domains[domain]["Users"]:
                domains[domain]["Users"].append(user_name)

        json.dump(domains, file, indent=4)

    except JSONDecodeError:
        domains = {domain: {"Domain": domain, "Users": [user_name]}}
        file = open("./tables/domainlist.json", "w+")
        json.dump(domains, file, indent=4)

    file = open('./tables/userlist.json', "r")
    users = json.load(file)
    if domain not in users[user_name]["Domains"]:
        users[user_name]["Domains"].append(domain)
    file = open('./tables/userlist.json', "w+")
    json.dump(users, file, indent=4)
    print("Success")


'''
To Do: Assign a type to an object. You can think of this as adding an object to a group of objects of the same type.

If the type name does not exist, it is created.

The object can be any non-null string.

Test program:

portal SetType object type_name
The program should report

Success
Failure if the object or the type names are empty strings.
'''
# check set type error


def SetType(object_, type_name):

    # print('SetType')
    # Check if object is empty report Failure
    if object_ == "":
        print("Failure")
        return
    # Check if type is empty report failure
    if type_name == "":
        print("Failure")
        return
    # Check if types.json exists if not create file
    if not path.exists('./tables/types.json'):
        open("./tables/types.json", "w+")
    # Read file and load data to types dict
    file = open("./tables/types.json", "r")
    try:
        types = json.load(file)
        # if type_name exits and append object to the dict
        if type_name in types:
            if object_ not in types[type_name]["Objects"]:
                types[type_name]["Objects"].append(object_)
            else:
                print('Success')
                # print("Object already exits in type")
                return
        else:
            types[type_name] = {"Type": type_name, "Objects": [object_]}
    except JSONDecodeError:
        # create the dict, add the type with object
        # types = {type_name: {"Name": type_name, "Objects": [object_]}}
        types = {type_name: {"Type": type_name, "Objects": [object_]}}

    file = open("./tables/types.json", "w+")
    # dump data to the json file
    json.dump(types, file, indent=4)
    # SUCCESS
    print("Success")


''' 
To Do: Validate a user’s password by passing the username and password, both strings.

Test program:

portal Authenticate myname mypassword

The program should clearly report

Success
Error: no such user
Error: bad password
'''


def Authenticate(user, password):
    # print('Authenticate')
    # Check if user file list already exists if not report error
    if not path.exists('./tables/userlist.json'):
        print('Error: no such user')
        return
    # Open file and load user list
    file = open("./tables/userlist.json", "r")

    try:
        users = json.load(file)
        # check if user is in user list
        if user in users:
            # Check if the password entered is the password stored
            # if not report bad password error
            if users[user]["Password"] != password:
                print('Error: bad password')
                return
        else:
            # If user not in user list report error
            print('Error: no such user')
            return

    except JSONDecodeError:
        # JSON EXCEPTION
        print("Error: no such user")
        return
    # If all checks pass print success
    print('Success')


'''
To Do: List all the objects that have a specific type, one per line.

The type name must be a non-empty string.

Test program:

portal TypeInfo type_name
The program should report

List all the objects that have been assigned type_name with SetType, one per line.
Nothing if the type does not exist or there are no objects associated with that type.
Error if the type name is an empty string.
 Sample output:

alice_file
bob_file
charles_file
david_file
ellen_file
with no leading tabs or spaces. This output format fits into the Unix tools philosophy, which makes the output suitable for input in a pipeline of commands.
'''

# have to set error for typeinfo that dne


def TypeInfo(type_name):
    # print('Type Info')
    # check if type name is empty
    if type_name == "":
        print('Type Name is empty')
        return
    # check if types.json exists if not create file
    if not path.exists("./tables/types.json"):
        open("./tables/types.json", "w+")
        return

    # Read file and load all the type in a dict
    file = open("./tables/types.json", "r")

    try:
        types = json.load(file)
        # check if type_name in types if exits print objects else do nothing return
        if not type_check(type_name):
            return
        if type_name in types:
            for object_ in types[type_name]["Objects"]:
                print(object_)

    except JSONDecodeError:
        # JSON exception
        return


# USER CHECK
''' if user_name in userlist.json return true else false'''


def user_check(user_name):
    if not path.exists('./tables/userlist.json'):
        return False
    file = open('./tables/userlist.json', 'r')
    try:
        users = json.load(file)
        if user_name in users:
            return True
    except JSONDecodeError:
        return False
    return False


# Domain CHECK
''' if domain_name in domainlist.json return true else false'''


def domain_check(domain_name):
    if not path.exists('./tables/domainlist.json'):
        return False
    file = open('./tables/domainlist.json')
    try:
        domains = json.load(file)
        if domain_name in domains:
            return True
    except JSONDecodeError:
        return False
    return False


# permission CHECK
''' if operation in permissions.json return true else false'''


def permission_check(operation):
    if not path.exists('./tables/permissions.json'):
        return False
    file = open('./tables/permissions.json')
    try:
        types = json.load(file)
        if operation in types:
            return True
    except JSONDecodeError:
        return False
    return False


# TypeCHECK
''' if type_name in types.json return true else false'''


def type_check(type_name):
    if not path.exists('./tables/types.json'):
        return False
    file = open('./tables/types.json')
    try:
        types = json.load(file)
        if type_name in types:
            return True
    except JSONDecodeError:
        return False
    return False

# main func. to parse our console inpute and report error accordingly for
# invalid input


def main():
    # input parser
    if len(sys.argv) < 2:
        print("Error: Invalid Input, exiting....")
        return
    elif sys.argv[1] == 'DomainInfo' and len(sys.argv) == 3:
        DomainInfo(sys.argv[2])
    elif sys.argv[1] == 'TypeInfo' and len(sys.argv) == 3:
        TypeInfo(sys.argv[2])
    elif sys.argv[1] == 'AddUser' and len(sys.argv) == 4:
        AddUser(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'Authenticate' and len(sys.argv) == 4:
        Authenticate(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'SetType' and len(sys.argv) == 4:
        SetType(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'SetDomain' and len(sys.argv) == 4:
        SetDomain(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'AddAccess' and len(sys.argv) == 5:
        AddAccess(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'CanAccess' and len(sys.argv) == 5:
        CanAccess(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Error: Invalid Input.. exiting...")
        return


if __name__ == '__main__':
    main()
