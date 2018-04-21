from flask import Flask, session, request, send_from_directory, redirect, url_for
import db.db
import base64
import out


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret'
login_user = 'admin'
password_user = 'admin'

utka = db.db.SkrepkaDB('db\\DatBasS.sqlite3')

@app.route('/api/text/<p>', methods=['GET'])
def getText(p):
    return utka.get_text(base64.b64decode(p).decode('utf-8'))

@app.route('/api/tags/<p>', methods=['GET'])
def getTags(p):
    if utka.get_tags(base64.b64decode(p).decode('utf-8')) == -1:
        return ''
    else:
        return ' '.join(utka.get_tags(base64.b64decode(p).decode('utf-8')))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['login'] == login_user and request.form['password'] == password_user:
            session['auth'] = True
            return redirect(url_for('table'))
        else:
            return redirect(url_for('login'))
    else:
        return out.index()

@app.route('/table', methods=['GET'])
def table():
    url = utka.get_path()
    table_arr = []
    if url != -1:
        for u in url:
            table_arr.append([u,utka.get_text(u), ' '.join([str(x[0]) for x in utka.get_tags(u)])])
    return out.table(table_arr)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if session.get('auth') is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        utka.add_tags(request.form['path'], request.form['tags'])
        utka.add_text_to_path(request.form['text'], request.form['path'])
        return redirect(url_for('table'))
    else:
        return out.add()


@app.route('/delete/<p>', methods=['GET'])
def delSt(p):
    if session['auth'] is None:
        return redirect(url_for('login'))
    utka.delete_all_tags(base64.b64decode(p).decode('utf-8'))
    utka.delete_all_text(base64.b64decode(p).decode('utf-8'))
    return redirect(url_for('table'))

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'GET':
        result = []
        return out.search(result)
    text = request.form['search'].lower()
    for x in list(',.;"\'\n!?-\t'):
        text = text.replace(x, ' ')
    while "  " in text: text.replace('  ',' ')
    tags = text.split(' ')
    paths = []
    for tag in tags:
        paths.append(utka.get_path_by_tag(tag))
    path1 = []
    for x in paths:
        if not x in path1: path1.append(x)
    try:
        path1.remove(-1)
    except:
        pass
    result = []
    for path in path1:
        result.append([path[0], utka.get_text(path[0])])
    return out.search(result)

@app.route('/add_node/<parent_node>', methods=['GET'])
def add_node(parent_node):
    if session.get('auth') is None:
        return redirect(url_for('login'))
    #
    return out.addnote(parent_node)



@app.route('/nodes', methods=['GET'])
def nodes():
    return out.nodes(utka.node_list())


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)




if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8888)