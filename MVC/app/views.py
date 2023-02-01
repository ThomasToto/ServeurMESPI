from flask import Flask, render_template, request, redirect, url_for, session, send_file
import re
from app import app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import psutil

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    test = psutil.virtual_memory().percent

    return render_template('home.html', test=test)

@app.route('/projet', methods=['GET', 'POST'])
def projet():
    return render_template('projet.html')

@app.route('/LFI_RFI', methods=['GET', 'POST'])
def LFI_RFI():
    return render_template('LFI_RFI.html')

@app.route('/HeartBleed', methods=['GET', 'POST'])
def HeartBleed():
    return render_template('HeartBleed.html')

@app.route('/Shellshock', methods=['GET', 'POST'])
def Shellshock():
    return render_template('Shellshock.html')

@app.route('/XSS', methods=['GET', 'POST'])
def XSS():
    return render_template('XSS.html')

@app.route('/MITM', methods=['GET', 'POST'])
def MITM():
    return render_template('MITM.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/profil', methods=['GET', 'POST'])
def profil():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM USER WHERE email = %s', (session['email'],))
    account = cursor.fetchone()
    
    tabProgress1 = (account['LFI_PROGRESS'] / 3)*100
    tabProgress2 = (account['XSS_PROGRESS'] / 3)*100
    tabProgress3 = (account['SHELLSHOCK_PROGRESS'] / 3)*100
    tabProgress4 = (account['HEARTBLEED_PROGRESS'] / 3)*100
    tabProgress5 = (account['MITM_PROGRESS'] / 3)*100
    
    return render_template('profil.html', account=account, tabProgress1=tabProgress1, tabProgress2=tabProgress2,tabProgress3=tabProgress3,tabProgress4=tabProgress4,tabProgress5=tabProgress5)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('email', None)

   return redirect(url_for('index'))


@app.route('/login2/', methods=['GET', 'POST'])
def login2():
    isIdentify = False
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:

        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM USER WHERE email = %s AND password = md5(%s)', (email, password,))
        account = cursor.fetchone()

        if account:
            isIdentify = True


        if isIdentify == True:
            session['loggedin'] = True
            session['email'] = account['email']

            return redirect(url_for('home'))

        else:
            msg = "Username or password incorrect"

    return render_template('login.html', msg=msg)



@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/register2', methods=['GET', 'POST'])
def register2():
    msg = ''

    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'confirmpassword' in request.form and 'email' in request.form :

            username = request.form['username']
            password = request.form['password']
            passwordconfirm = request.form['confirmpassword']
            email = request.form['email']
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            count = cursor.execute('SELECT * from USER where email = %s', (email,))
            
            if(count == 0):
                if(password == passwordconfirm):         
                    
                    cursor.execute('INSERT INTO USER VALUES (%s, %s, md5(%s),0,0,0,0,0)', (username, email, password,))
                    mysql.connection.commit()
                    msg = 'Sign up validated'
                else:
                    msg = 'Passwords do not match'
            else:
                msg = 'Email already exists'
                
        elif request.method == 'POST':
            msg = 'Please complete the form'
        return render_template('register.html', msg=msg)

    return redirect(url_for('login'))


@app.route('/LFI_RFI_results', methods=['GET', 'POST'])
def LFI_RFI_results():
    score = 0
    scoreMax=5
    if request.form.get("1-1"):
        score += 1
    if request.form.get("2-2"):
        score += 1
    if request.form.get("3-1"):
        score += 1
    if request.form.get("4-1"):
        score += 1
    if request.form.get("5-2"):
        score += 1
        
        
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET LFI_SCORE = %s WHERE email = %s', (score,session['email'],))
    mysql.connection.commit()
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET LFI_PROGRESS = 3 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
        
    return render_template('results.html',score=score,scoreMax=scoreMax)


@app.route('/MITM_results', methods=['GET', 'POST'])
def MITM_results():
    score = 0
    scoreMax=3
    if request.form.get("1-2"):
        score += 1
    if request.form.get("2-1"):
        score += 1
    if request.form.get("3-3"):
        score += 1
        
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET MITM_SCORE = %s WHERE email = %s', (score,session['email'],))
    mysql.connection.commit()
    
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET MITM_PROGRESS = 3 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    
    return render_template('results.html',score=score,scoreMax=scoreMax)


@app.route('/HeartBleed_results', methods=['GET', 'POST'])
def HeartBleed_results():
    score = 0
    scoreMax=3
    if request.form.get("1-1"):
        score += 1
    if request.form.get("2-1"):
        score += 1
    if request.form.get("3-2"):
        score += 1
        
        
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET HEARTBLEED_SCORE = %s WHERE email = %s', (score,session['email'],))
    mysql.connection.commit()
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET HEARTBLEED_PROGRESS = 3 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    
    return render_template('results.html',score=score,scoreMax=scoreMax)


@app.route('/Shellshock_results', methods=['GET', 'POST'])
def Shellshock_results():
    score = 0
    scoreMax=4
    if request.form.get("1-2"):
        score += 1
    if request.form.get("2-1"):
        score += 1
    if request.form.get("3-2"):
        score += 1
    if request.form.get("4-3"):
        score += 1
        
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET SHELLSHOCK_SCORE = %s WHERE email = %s', (score,session['email'],))
    mysql.connection.commit()
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET SHELLSHOCK_PROGRESS = 3 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    
    return render_template('results.html',score=score,scoreMax=scoreMax)


@app.route('/XSS_results', methods=['GET', 'POST'])
def XSS_results():
    score = 0
    scoreMax=4
    if request.form.get("1-2"):
        score += 1
    if request.form.get("2-3"):
        score += 1
    if request.form.get("3-1"):
        score += 1
    if request.form.get("4-2"):
        score += 1
        
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET XSS_SCORE = %s WHERE email = %s', (score,session['email'],))
    mysql.connection.commit()
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET XSS_PROGRESS = 3 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    
    return render_template('results.html',score=score,scoreMax=scoreMax)


@app.route('/avancementHeartBleed')
def avancementHeartBleed():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET HEARTBLEED_PROGRESS = 1 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    return render_template('HeartBleed.html')

@app.route('/avancementMITM')
def avancementMITM():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET MITM_PROGRESS = 1 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    return render_template('MITM.html')

@app.route('/avancementLFI_RFI')
def avancementLFI_RFI():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET LFI_PROGRESS = 1 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    return render_template('LFI_RFI.html')

@app.route('/avancementXSS')
def avancementXSS():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET XSS_PROGRESS = 1 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    return render_template('XSS.html')

@app.route('/avancementShellshock')
def avancementShellshock():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET SHELLSHOCK_PROGRESS = 1 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    return render_template('Shellshock.html')




@app.route('/downloadHeartBleed')
def downloadHeartBleed():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET HEARTBLEED_PROGRESS = 2 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    return send_file("G:/EPISEN/ITS2/S2/MESPI/Projet/MVC/app/static/assets/tp/TP_Heartbleed.pdf", as_attachment=True)

@app.route('/downloadMITM')
def downloadMITM():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET MITM_PROGRESS = 2 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    return send_file("G:/EPISEN/ITS2/S2/MESPI/Projet/MVC/app/static/assets/tp/TP_MITM.pdf", as_attachment=True)

@app.route('/downloadLFI_RFI')
def downloadLFI_RFI():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET LFI_PROGRESS = 2 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    return send_file("G:/EPISEN/ITS2/S2/MESPI/Projet/MVC/app/static/assets/tp/TP_LFI_RFI.pdf", as_attachment=True)

@app.route('/downloadXSS')
def downloadXSS():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET XSS_PROGRESS = 2 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    return send_file("G:/EPISEN/ITS2/S2/MESPI/Projet/MVC/app/static/assets/tp/TP_XSS.pdf", as_attachment=True)

@app.route('/downloadShellshock')
def downloadShellshock():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE USER SET SHELLSHOCK_PROGRESS = 2 WHERE email = %s', (session['email'],))
    mysql.connection.commit()
    return send_file("G:/EPISEN/ITS2/S2/MESPI/Projet/MVC/app/static/assets/tp/TP_Shellshock.pdf", as_attachment=True)



