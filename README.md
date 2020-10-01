# _**Portal.py**_

## suraj kakkad (spk101)

### > Implementation of an authentication and access control (authorization) library that can be used by services that need to rely on their own set of users rather than those who have accounts on the computer.

# The access control system support's: (TEST CASES)

-   AddUser(): Define a new user for the system along with the user’s password.

    ##### > python portal.py AddUser "suraj" Mypassword

    ##### > Success

    ##### > python portal.py AddUser "fang" 123456

    ##### > Success

-   Authenticate(): Validate a user’s password by passing the username and password.

    ##### > python portal.py Authenticate "suraj" Mypassword

    ##### > Success

    ##### > python portal.py Authenticate "suraj" 123456

    ##### > Error: bad password

-   AddAccess(): Adding an access right to a defined user: a string that defines an access permission of a domain to an object. The access permission can be an arbitrary string that makes sense to the service.

    ##### > python portal.py AddAccess view user premium

    ##### > Success

-   CanAccess(): Check whether the user is allowed to perform the specified operation on the object. That means that there exists a valid access right for an operation in some (domain, type) where the user is in domain and the object is in the corresponding type.

    ##### > python portal.py CanAccess view suraj hbo

    ##### > Success

    ##### > python portal.py CanAccess view suraj netfix

    ##### > Success

    ##### > python portal.py CanAccess view fang hbo

    ##### > Error: Access Denied

-   SetType(): Assign a type to an object. Think of this as adding an object to a group of objects of the same type.

    ##### > python portal.py SetType hbo premium

    ##### > Success

    ##### > python portal.py SetType hbo netflix

    ##### > Success

-   SetDomain(): Assign a user to a domain. Think of it as adding a user to a group.

    ##### > python portal.py SetDomain "suraj" user

    ##### > Success

    ##### > python portal.py SetDomain "sur" user

    ##### > Error: no such user

    ##### > python portal.py SetDomain "fang" admin

    ##### > Success

-   Domain Info(): List all the users in a domain.

    ##### > python portal.py DomainInfo admin

    ##### > fang

-   TypeInfo(): List all the objects that have a specific type, one per line.

    ##### > python portal.py TypeInfo premium

    ##### > hbo

    ##### > netflix
