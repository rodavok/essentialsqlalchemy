from orm_exceptions_db import User, Cookie, LineItem, Order, session
from sqlalchemy import inspect
'''
session states

when querying for an object, the object that is returned is from the session
there are four states an object can be in:
Transient: not in the session, not in the db
Pending: added to the session, but not committed (or flushed)
Persistent: it's available and in the db
Detached: not in the session, but is in the db
'''

#inspect a newly made cookie object
cc_cookie = Cookie('chocolate chip', 'http://some.aweso.me/cookie/recipe.html',
                   'CC01', 12, 0.50)
insp = inspect(cc_cookie)
'''
#hasn't been added to the db yet - it's transient
for state in ['transient', 'pending', 'persistent', 'detached']:
    print('{:>10}: {}'.format(state, getattr(insp, state)))

session.add(cc_cookie)

insp = inspect(cc_cookie)
#added, but not committed - pending
for state in ['transient', 'pending', 'persistent', 'detached']:
    print('{:>10}: {}'.format(state, getattr(insp, state)))

session.commit()

insp = inspect(cc_cookie)
#committed - persistent
for state in ['transient', 'pending', 'persistent', 'detached']:
    print('{:>10}: {}'.format(state, getattr(insp, state)))

#for moving data to a new session
session.expunge(cc_cookie)

insp = inspect(cc_cookie)
#cc_cookie is now detached
for state in ['transient', 'pending', 'persistent', 'detached']:
    print('{:>10}: {}'.format(state, getattr(insp, state)))

#better to check state with inspect(object).transient, .pending, etc
'''

session.add(cc_cookie)
#name of cookie has been changed since it was added to the session
cc_cookie.cookie_name = 'Change chocolate chip'

insp = inspect(cc_cookie)

print(insp.modified)  #true

for attr, attr_state in insp.attrs.items():
    #inspect object has attibutes in an sql attributes object...
    #shich contains the attributes (i.e. columns), and a state object
    #which has its own attributes, such as its change history
    if attr_state.history.has_changes():
        print('{}: {}'.format(attr, attr_state.value))
        print('History: {}\n'.format(attr_state.history))
