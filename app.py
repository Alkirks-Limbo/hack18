from flask import Flask, url_for, session, redirect, request, send_from_directory
import forms.bforms
import  forms.html
import db.DataBase
import random

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret'

petyx=db.DataBase.DataBase('db\\DatBas.sqlite3')


@app.route('/', methods=['GET'])
def index():
    return forms.html.index()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('email') is not None:
        return redirect('account')
    if request.method=='POST':
        username = request.form['username']
        password = request.form['pswd']
        if petyx.login_user(email=username,
                            password=password):
            session['email'] = username
            return redirect(url_for('account'))
        else:
            return forms.html.login_error()
    else:
        return forms.html.login()

@app.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('login'))

@app.route('/account', methods=['GET'])
def account():
    if session.get('email') is None:
        return redirect(url_for('login'))
    else:
        user = petyx.get_user_info(session['email'])
        pocket = petyx.get_user_pockets_and_money(session['email'])
        return forms.html.account(user['full_name'],
                                  user['phone'],
                                  user['email'],
                                  user['company'],
                                  pocket['pocket_number'],
                                  pocket['money_amount'])


@app.route('/cards', methods=['GET'])
def cards():
    if session.get('email') is None:
        return redirect(url_for('login'))
    cards = petyx.get_cards(petyx.get_user_pockets_and_money(session.get('email'))['pocket_number'])
    mas = []
    for card in cards:
        mas.append([card, petyx.find_driver(card)])
    return forms.html.cards(mas,
                            petyx.get_user_pockets_and_money(session.get('email'))['pocket_number'])

@app.route('/cards/add', methods=['GET'])
def cardadd():
    if session.get('email') is None:
        return redirect(url_for('login'))
    petyx.add_cart2pocket_user(random.randint(10**16, 10**17),
                               petyx.get_user_pockets_and_money(session.get('email'))['pocket_number'])
    return redirect(url_for('cards'))

@app.route('/cards/delete/<cardnum>', methods=['GET'])
def carddel(cardnum):
    if session.get('email') is None:
        return redirect(url_for('login'))
    petyx.del_card(cardnum)
    return redirect(url_for('cards'))




@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if session.get('email') is None:
        return redirect(url_for('login'))
    user = petyx.get_user_info(session['email'])
    if request.method == 'POST' and request.form['fio']!='':
        if request.form['email']!=user['email']:
            if not petyx.check_reg_user(request.form['email']):
                return forms.html.edit(user['full_name'],
                           user['phone'],
                           user['email'],
                           user['company'])
        petyx.update_prefs_user(user['email'],
                            request.form['email'],
                            request.form['fio'],
                            request.form['phone'],
                            request.form['org'])
        session['email'] = request.form['email']
        return redirect(url_for('account'))
    if request.method == 'POST' and request.form['passwd'] != '':
        if request.form['passwd'] == user['password'] and \
                request.form['newpasswd1']==request.form['newpasswd2']:
            petyx.update_pass_user(user['email'], request.form['newpasswd1'])
            return redirect(url_for('account'))
    return forms.html.edit(user['full_name'],
                           user['phone'],
                           user['email'],
                           user['company'])



@app.route('/drivers', methods=['GET'])
def drivers():
    if session.get('email') is None:
        return redirect(url_for('login'))
    return forms.html.drivers(petyx.get_drivers(session.get('email')), petyx.get_user_info(session['email'])['company'])

@app.route('/drivers/add', methods=['GET', 'POST'])
def addDriver():
    if session.get('email') is None:
        return redirect(url_for('login'))
    card = petyx.get_cards(petyx.get_user_pockets_and_money(session.get('email'))['pocket_number'])
    driver = petyx.get_drivers(session.get('email'))
    driver_cards = [x[2] for x in driver]
    freeCards = []
    for c in card:
        if not c in driver_cards:
            freeCards.append(c)

    if request.method == 'POST':
        petyx.add_driver(session.get('email'),
                         request.form['fio'],
                         request.form['card'], '')
        return redirect('drivers')
    else:
        return forms.html.add_driver(freeCards)

@app.route('/drivers/del/<cardnum>', methods=['GET'])
def driverdel(cardnum):
    if session.get('email') is None:
        return redirect(url_for('login'))
    cards = petyx.get_cards(petyx.get_user_pockets_and_money(session.get('email'))['pocket_number'])
    if cardnum in cards:
        petyx.delete_driver(cardnum)
    return redirect(url_for('drivers'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('email')is not None:
        return redirect(url_for('account'))
    if request.method == 'POST':
        if(request.form['pswd1'] == request.form['pswd2']):
            if petyx.reg_user(full_name=request.form['lastname']+' '+request.form['firstname']+' '+request.form['middlename'],
                                 email=request.form['useremail'],
                                 password=request.form['pswd1'],
                                 company=request.form['userorg'],
                                 phone=request.form['usertel']):
                petyx.create_user_pocket(request.form['useremail'], str(random.randint(10**20, 10**21)))
                return redirect(url_for('login'))
            else:
                return redirect(url_for('register'))
        else:
            return redirect(url_for('register'))
    else:
        return forms.html.register()

@app.route('/money', methods=['GET', 'POST'])
def money():
    if session.get('email') is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        petyx.add_money2pocket(petyx.get_user_pockets_and_money(session.get('email'))['pocket_number'],
                               int(request.form['money']))
    return forms.html.add_money()


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run()
