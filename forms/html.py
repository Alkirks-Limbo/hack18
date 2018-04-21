


def index():
    f = open('forms\\beauty\\index.html',encoding="utf8")
    s = f.read()
    f.close()
    return s

def register():
    f = open('forms\\beauty\\register.html',encoding="utf8")
    s = f.read()
    f.close()
    return s

def login():
    f = open('forms\\beauty\\login.html',encoding="utf8")
    s = f.read()
    f.close()
    return s

def login_error():
    f = open('forms\\beauty\\login_err.html', encoding="utf8")
    s = f.read()
    f.close()
    return s

def account(
        fio,
        phone,
        email,
        org,
        schet,
        money):
    f = open('forms\\beauty\\account.html', encoding="utf8")
    s = f.read()
    f.close()
    s = s.replace('&lt;fio&gt;',fio).replace('&lt;fio&gt;',fio)
    s = s.replace('&lt;phone&gt;', phone).replace('&lt;phone&gt;', phone)
    s = s.replace('&lt;email&gt;', email).replace('&lt;email&gt;', email)
    s = s.replace('&lt;org&gt;', org).replace('&lt;org&gt;', org)
    s = s.replace('&lt;schet&gt;', schet).replace('&lt;schet&gt;', schet)
    s = s.replace('&lt;money&gt;', str(money)).replace('&lt;money&gt;', str(money))
    return s

def edit(
        fio,
        phone,
        email,
        org):
    f = open('forms\\beauty\\edit.html', encoding="utf8")
    s = f.read()
    f.close()
    s = s.replace('&lt;fio&gt;',fio).replace('<fio>',fio)
    s = s.replace('&lt;phone&gt;', phone).replace('<phone>', phone)
    s = s.replace('&lt;email&gt;', email).replace('<email>', email)
    s = s.replace('&lt;org&gt;', org).replace('<org>', org)
    return s

def cards(card_arr,schet):


    ins = """<tr class="bg-info">
                  <th scope="row"><<num>></th>
                  <td><<fio>></td>
                  <td>
                    <a href="/cards/delete/<<num>>" class="btn btn-outline-primary" >Delete</a>
                  </td>
                </tr>
                """

    center = ''
    for x in card_arr:
        center+=ins.replace('<<num>>',x[0]).replace('<<fio>>',x[1])
    f = open('forms\\beauty\\cards.html', encoding="utf8")
    s = f.read()
    f.close()
    s = s.replace('%%insert%%',center).replace('&lt;schet&gt;',schet)
    return s


def add_driver(cards_arr):

    ins = '''<option value="NUM">NUM</option>'''
    f = open('forms\\beauty\\add_driver.html', encoding="utf8")
    s = f.read()
    f.close()

    center = ''
    for x in cards_arr:
        center+=ins.replace('NUM',x)

    s = s.replace('%%insert%%',center)
    return s

def drivers(driver_arr,org):

    ins = '''<tr>
                  <td>FIO</td>
                  <td>CARD</td>
                  <td>
                    <a href="/drivers/del/CARD" class="btn btn-outline-primary">Delete</a>
                  </td>
                </tr>
                '''
    center = ''
    for x in driver_arr:
        center+=ins.replace('FIO',x[0]).replace('CARD',x[2])
    f = open('forms\\beauty\\drivers.html', encoding="utf8")
    s = f.read()
    f.close()

    s = s.replace('&lt;org&gt;',org)
    s = s.replace('%%insert%%', center)
    return s

def add_money():
    f = open('forms\\beauty\\add_money.html',encoding="utf8")
    s = f.read()
    f.close()
    return s