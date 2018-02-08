from flask import Flask, render_template, request, json, session
from flaskext.mysql import MySQL
import random
import os
from werkzeug import generate_password_hash, check_password_hash

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

app = Flask(__name__)

mysql = MySQL()


##MySQL configs
app.config['MYSQL_DATABASE_USER'] ='root'
app.config['MYSQL_DATABASE_PASSWORD'] ='password'
app.config['MYSQL_DATABASE_DB'] ='keystore'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)


def generateUserPassHash(password):
    return generate_password_hash(password)

def validateUserPass(inp_pass, hash_pass):
    return check_password_hash(hash_pass, inp_pass)

def generateKeyPassHash(password, username):
    try:
        UserKey = bytes(username)
        #salt = os.urandom(16)
        salt = bytes(random.randint(1, 10**16))
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(UserKey))
        f = Fernet(key)
        hash_pass = f.encrypt(bytes(password))
        return (hash_pass, salt)
    except Exception as e:
        print(e)
        print ('exception')

def retrivePassFromHash(hash_pass, username, salt):
    Userkey = bytes(username)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(Userkey))
    f = Fernet(key)
    password = f.decrypt(hash_pass)
    return str(password)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showRegister')
def showRegister():
    return render_template('registerUser.html')

@app.route('/showSignIn')
def showSignIn():
    return render_template('signIn.html')

@app.route('/registerUser', methods=['POST'])
def registerUser():

    try:
        _username = request.form['userName']
        _password = request.form['password']
        _confirm_password = request.form['confirm_password']
        _firstName = request.form['first_name']
        _lastName = request.form['last_name']
        _hint = request.form['hint']
        #print('here')
        if _username and _password and _confirm_password and _firstName and _lastName:

            if _password != _confirm_password:
                return json.dumps({'message': 'passwords do not match'})

            _hashed_password = generateUserPassHash(_password)

            conn = mysql.connect()
            cur = conn.cursor()
            args = (_username, _hashed_password, _firstName, _lastName, _hint)
            print(args)
            cur.callproc('createUser', args)
            result = cur.fetchall()
            if result[0][0] == 'S':
                conn.commit()
                cur.close()
                conn.close()
                return json.dumps({'Message': result[0][1]})
            else:
                conn.rollback()
                cur.close()
                conn.close()
                return json.dumps({'Error': result[0][1]})

        else:
            return json.dumps({'Error':'Enter all details'})

    except Exception as e:
        return json.dumps({'Error':str(e)})
    finally:
        if conn.open:
            conn.close()

@app.route('/signIn', methods=['POST'])
def signIn():
    """
    :return:
    """
    try:
        _username = request.form['userName']
        _password = request.form['password']

        if _username and _password:
            #_hashed_password = generateUserPassHash(_password)

            conn = mysql.connect()
            cur = conn.cursor()
            cur.callproc('getUserPassword', [_username])
            result = cur.fetchone()
            if result[0]=='S':
                if validateUserPass(_password, result[2]):
                    session['username'] = _username
                    conn.commit()
                    cur.close()
                    conn.close()
                    return json.dumps({'Message': 'Logging you in'})
                else:
                    conn.commit()
                    cur.close()
                    conn.close()
                    return json.dumps({'Error':'Incorrect password'})
            else:
                conn.rollback()
                cur.close()
                conn.close()
                return json.dumps({'Error':result[1]})

        else:
            return json.dumps({'Error':'Please fill all the fields'})

    except Exception as e:
        return json.dumps({'Error': str(e)})
    finally:
        if conn.open:
            conn.close()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

@app.route('/showResetPasswordPage', methods=['POST'])
def showResetPasswordPage():
    return render_template('resetPassword.html')

@app.route('/showUserHomePage')
def showUserHomePage():
    if session['username']:
        userName = session['username']
        try:
            _userName = userName
            if _userName:
                conn = mysql.connect()
                cur = conn.cursor()
                cur.callproc( 'getUserId',[_userName])
                result = cur.fetchall()
                cur.close()
                if result[0][0]=='S':
                    userId = result[0][2]
                    cur = conn.cursor()
                    cur.callproc('getUserKeys',[int(userId)])
                    data = cur.fetchall()
                    #print(type(data))
                    #print (data)
                    data = list(data)
                    result_set = []
                    for item in data:
                        res = list(item)
                        res.append(retrivePassFromHash( str(item[3]) , str(_userName), str(item[4]) ))
                        result_set.append(res)
                    #print (data)
                    data = tuple(result_set)
                    #print(data)
        except Exception as e:
            print(e)
        finally:
            if conn.open:
                conn.close()
        return render_template('userHomePage.html', userName= _userName, data= data)
    else:
        return render_template('errorPage.html')

@app.route('/showAddUserKeys')
def showAddUserKeys():
    userName = session['username']
    return render_template('addUserKeys.html', userName = userName)

@app.route('/addUserKeys', methods=['POST'])
def addUserKeys():
    if session['username']:
        userName = session['username']
        try:
            _key = request.form['key']
            _password = request.form['password']
            _keyHint = request.form['keyHint']
            _username = userName

            if _key and _password and _username:
                result = generateKeyPassHash(_password, _username)
                conn = mysql.connect()
                cur = conn.cursor()
                _args = (_username, _key, unicode(result[0]), str(result[1]), _keyHint)
                print (_args)
                cur.callproc('addUserKeys', _args)
                result = cur.fetchone()

                if result[0]=='S':
                    conn.commit()
                    cur.close()
                    conn.close()
                    return json.dumps({'Message': 'Key added successfully'})
                else:
                    conn.rollback()
                    cur.close()
                    conn.close()
                    return json.dumps({'Error': result[1]})
        except Exception as e:
            print (e)
            return json.dumps({'Error':str(e)})
        finally:
            if conn.open:
                conn.close()
    else:
        return render_template('errorPage.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(16)
    app.run()


