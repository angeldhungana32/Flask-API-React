import flask
from flask import request, jsonify
import sqlite3
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>An API For Events</p>'''


@app.route('/api/events/all')
def api_all():
    conn = sqlite3.connect('eventDB.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_events = cur.execute('SELECT * FROM Events;').fetchall()
    print(all_events)
    return jsonify(all_events)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/events')
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    loc = query_parameters.get('location')
    nam = query_parameters.get('name')

    query = "SELECT * FROM events WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if nam:
        query += ' Name=? AND'
        to_filter.append(nam)
    if loc:
        query += ' Location=? AND'
        to_filter.append(nam)
    if not (id or nam or loc):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('eventDB.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


@app.route('/api/addevents', methods=['POST'])
def api_adder():
    data = request.get_json()
    query = '''INSERT INTO events (Name, Description, Location, Date) VALUES (?,?,?,?)'''
    values = (data['Name'], data["Description"], data["Location"],
              data["Date"])
    conn = sqlite3.connect('eventDB.db', isolation_level=None)
    cur = conn.cursor()
    _ = cur.execute(query, values)
    return ""


app.run()