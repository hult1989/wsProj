# -*- coding:utf-8 -*-
import random
from appException import *
from twistar.dbobject import DBObject
from twistar.registry import Registry
from twisted.python import log





def transferOwnershipSql(wsdbpool, imei, username, password, newowner):
    return wsdbpool.runInteraction(_transferOwnership, imei, username, password, newowner)

def _transferOwnership(txn, imei, username, password, newowner):
    if  _checkPassword(txn, username, password):
        txn.execute('select username from user_ws where username = %s and imei = %s', (newowner, str(imei)))
        if not txn.fetchone():
            raise NoUserException
        txn.execute('select state from user_ws where username = %s and imei = %s', (username, str(imei)))
        if txn.fetchone()[0] != 'o':
            raise NoPermissionException
        txn.execute('update user_ws set state = "o" where username = %s and imei = %s', (newowner, imei))
        txn.execute('update user_ws set state = "b" where username = %s and imei = %s', (username, imei))
    print 'ownership changed'
    return True







def _checkPassword(txn, username, password):
    txn.execute('select password from userinfo where username = %s', (username,))
    pwd = txn.fetchone()
    if not pwd:
        raise NoUserException
    if pwd[0] != password:
        raise PasswordErrorException
    return True



def getRelatedUsers(wsdbpool, imei):
    return wsdbpool.runQuery('select username, state from user_ws where imei = %s', (imei,))

def deleteUser(wsdbpool, imei, username, deleteuser):
    return wsdbpool.runInteraction(_deleteUser, imei, username, deleteuser)

def _deleteUser(txn, imei, username, deleteuser):
    txn.execute('select username, state from user_ws where imei = %s' ,(imei,))
    users = txn.fetchall()
    print users
    if len(users) == 0:
        raise NoImeiException
    if username not in [u[0] for u in users if u[1] == 'o']:
        raise NoPermissionException
    if deleteuser in [u[0] for u in users if u[1] == 'o']:
        raise NoPermissionException
    if deleteuser not in [u[0] for u in users if u[1] != 'o']:
        raise NoTargetException
    txn.execute('delete from user_ws where imei = %s and username = %s', (str(imei), str(deleteuser)))
    return True


def getRelationByUsernameSimnum(wsdbpool, username, simnum):
    return wsdbpool.runInteraction(_getRelationByUsernameSimnum, username, simnum)

def _getRelationByUsernameSimnum(txn, username, simnum):
    txn.execute('select user_ws.username, user_ws.imei, user_ws.state, wsinfo.simnum from user_ws, wsinfo where user_ws.imei = wsinfo.imei and user_ws.username = %s and wsinfo.simnum = %s', (str(username), str(simnum)))
    return txn.fetchall()


def _insertTempRelationSql(txn, username, simnum, name):
    #elder bind request record will be erased to avoid collision
    _cleanAppBindRequest(txn, simnum)
    txn.execute('replace into temp_user_ws (username, simnum, name) values (%s, %s, %s)', (str(username), str(simnum), str(name)))

def _cleanAppBindRequest(txn, simnum):
    txn.execute('delete from temp_user_ws where simnum = %s', (str(simnum),))

       
def _getStickNameCheckAppRequest(txn, simnum):
    txn.execute('select username, name from temp_user_ws where simnum = %s', (str(simnum),))
    result = txn.fetchall()
    return result

def setImeiDefault(wsdbpool, username, imei):
    return wsdbpool.runInteraction(_setImeiDefault, username, imei)

def _setImeiDefault(txn, username, imei):
    txn.execute('update user_ws set isdefault = 0 where username = %s', (str(username),))
    txn.execute('update user_ws set isdefault = 1 where username = %s and imei = %s', (str(username),str(imei)))
    return True

def _getStickOwner(txn, imei):
    txn.execute('select * from user_ws where imei = %s and state = "o"', (str(imei),))
    return txn.fetchall()

def _createUserWsRelation(txn, username, imei, name, state):
    txn.execute('replace into user_ws (username, imei, name, state) values (%s, %s, %s, %s)', (str(username), str(imei), str(name), str(state)) )
    _setImeiDefault(txn, username, imei)

def _getWsinfo(txn, imei):
    txn.execute('select * from wsinfo where imei = %s', (str(imei),))
    return txn.fetchall()

def _updateWsinfo(txn, imei, simnum):
    if len(_getWsinfo(txn, imei)) == 0:
        txn.execute('insert into wsinfo (imei, simnum, adminpwd) values(%s, %s, "123456")', (str(imei), str(simnum)))
    else:
        txn.execute('update wsinfo set simnum = %s where imei = %s', (str(simnum), str(imei)))

def _updateUserPhone(txn, username, userphone):
    txn.execute('update userinfo set phone = %s where username = %s', (userphone, username))


def createAuthCode(wsdbpool, imei):
    return wsdbpool.runInteraction(_createAuthCode, imei)

def _deleteOuttimeCode(txn):
    txn.execute('delete from temp_code where unix_timestamp(timestamp) + 120 < unix_timestamp(now())', ())

def _createAuthCode(txn, imei):
    if len(_getWsinfo(txn, imei)) == 0:
        raise NoImeiException

    code = random.randint(100000, 999999)

    _deleteOuttimeCode(txn)
    txn.execute('select * from temp_code where code = %s', (code,))
    result = txn.fetchall()
    #make sure duplicate code doesn't exists
    while len(result) != 0:
        code = random.randint(100000, 999999)
        txn.execute('select * from temp_code where code = %s', (code,))
        result = txn.fetchall()
    txn.execute('insert into temp_code (code, imei) values(%s, %s)', (code, imei))
    return code

def getImeiByCode(wsdbpool, code):
    return wsdbpool.runInteraction(_getImeiByCode, code)

def _getImeiByCode(txn, code):
    _deleteOuttimeCode(txn)
    txn.execute('select imei from temp_code where code = %s', (code,))
    result = txn.fetchall()
    if len(result) == 0:
        raise InvalidCodeException 
    return result[0][0]
    

def handleAppBindRequest(wsdbpool, username, simnum, name):
    return wsdbpool.runInteraction(_handleAppBindRequest, username, simnum, name)

def _handleAppBindRequest(txn, username, simnum, name):
    result = _getRelationByUsernameSimnum(txn, username, simnum)
    if len(result) > 0:
        imei = result[0][1]
        state = result[0][2]
        raise StickExistsException((imei, state))
    _insertTempRelationSql(txn, username, simnum, name)
 

def handleStickBindAck(wsdbpool, message):
    #1,123456789abcdef,bon13800000000,+8613600000000
    message = message.split(',')
    imei = message[1]
    simnum = message[2][3:]
    userphone = message[3]
    return wsdbpool.runInteraction(_handleStickBindAck, imei, simnum, userphone)

def _handleStickBindAck(txn, imei, simnum, userphone):
    result = _getStickNameCheckAppRequest(txn, simnum)
    if len(result) == 0:
        return False

    username = result[0][0]
    name = result[0][1]
    
    owner = _getStickOwner(txn, imei)
    if len(owner) == 0 or owner[0][0] == username:
        _createUserWsRelation(txn, username, imei, name, 'o')
    else:
        _createUserWsRelation(txn, username, imei, name, 'b')
    _updateWsinfo(txn, imei, simnum)
    _updateUserPhone(txn, username, userphone)
    _cleanAppBindRequest(txn, simnum)
    return True

def handleAppSubRequest(wsdbpool, username, name, code):
    return wsdbpool.runInteraction(_handleAppSubRequest, username, name, code)

def _handleAppSubRequest(txn, username, name, code):
    imei = _getImeiByCode(txn, code)
    _createUserWsRelation(txn, username, imei, name, 's')
    _deleteOuttimeCode(txn)
    return _getWsinfo(txn, imei)[0]


def handleDeleteStickRequest(wsdbpool, imei, username, password):
    return wsdbpool.runInteraction(_deleteStick,imei, username, password)

def _deleteStick(txn, imei, username, password):
    if _checkPassword(txn, username, password):
        owner = _getStickOwner(txn, imei)
        if owner and username == owner[0][0] and owner[0][4] == 'o':
            '''
            txn.execute('delete from familynumber where imei = %s', (imei,))
            txn.execute('delete from sosnumber where imei = %s', (imei,))
            '''
            txn.execute('delete from temp_code where imei = %s', (imei,))
            txn.execute('delete from temp_family where imei = %s', (imei,))
            txn.execute('delete from temp_sos where imei = %s', (imei,))
            txn.execute('delete from user_ws where imei = %s', (imei,))
            txn.execute('delete from user_ws_relationships where imei = %s', (imei,))
            return True
        raise NoPermissionException
    return True






if __name__ == '__main__':

    from twisted.internet import reactor, defer
    def testResult(result):
        if type(result) == tuple and len(result) == 0:
            print 'No result'
        print result
        reactor.stop()

    def testUtf(result):
        for r in result:
            for i  in r:
                print i
        reactor.stop()

    def onSuccess(success):
        print success
        reactor.stop()

    def onError(failure):
        print str(failure), failure.__class__
        print failure.value.errCode
        reactor.stop()

    import sys
    from sqlPool import wsdbpool
    Registry.DBPOOL = wsdbpool
    #wsdbpool.runInteraction(_insertTempRelationSql, 'zod', '13836435682', 'd').addCallbacks(onSuccess, onError)
    #handleAppBindRequest(wsdbpool, 'zod', '10086', 'duplicate').addCallbacks(onSuccess, onError)
    #handleStickBindAck(wsdbpool, '1,abcdef12345,bon13836435682,+8613600000000').addCallbacks(onSuccess, onError)
    #createAuthCode(wsdbpool, '1023').addCallbacks(onSuccess, onError)
    #handleAppSubRequest(wsdbpool, 'zod', 'ddx', 603752).addCallbacks(onSuccess, onError)
    #transferOwnershipSql(wsdbpool, '1024', 'batman', 'b', 'hulk').addCallbacks(onSuccess, onError)
    class User_ws_relationship(DBObject):
        pass
    relationship = User_ws_relationship()
    relationship.username = 'alex'
    relationship.imei = '1989'
    #relationship.save().addCallbacks(onSuccess, onError)
    User_ws_relationship().find(where=['username=? ', 'alex']).addCallbacks(onSuccess, onError)

    reactor.run()
