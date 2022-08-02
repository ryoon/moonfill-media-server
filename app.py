#!/usr/pkg/bin/python3.10

import flask
import sqlite3
import pathlib
import urllib

dbFile = 'database/media-server.sqlite3'

movieRootPath = '/mnt/nfs1/video'

connection = sqlite3.connect(dbFile)

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = flask.Blueprint('api', __name__, url_prefix='/v1')

@api.route('/getMoviesInfo', methods=['GET'])
def getMoviesInfo():
  query = flask.request.args.get('q').lower()
  #print('query is', query)

  try:
    connection = sqlite3.connect(dbFile)
  except sqlite3.Error as e:
    print(e)

  cursor = connection.cursor()

  searchKeyword = ''
  selectSql = '''select filepath, filename, suffix, dir from movies'''
  if query != None:
    selectSql = selectSql + ''' where filename like ?'''
    searchKeyword = (f'%{query}%',)
  selectSql = selectSql + ''' order by dir, filename'''
  cursor.execute(selectSql, searchKeyword)
  movies = cursor.fetchall()
  #print(movies)

  result = []
  for video in movies:
    result.append({
                    "filename": video[1],
                    "dir": video[3],
                    "filepath": video[0],
                    "encodedfilepath": urllib.parse.quote(video[0]),
                    "suffix": video[2]
                  })
  #print(result)
  return flask.jsonify({"movies": result}), 200

@api.route('/saveProgress', methods=['PUT'])
def saveProgress():
  req = flask.request

  filepath = req.form['filepath']
  user = req.form['user']
  lastseen = req.form['lastseen']
  progress = req.form['progress']

  res = (
    filepath,
    user,
    lastseen,
    progress
  )

  #print(filepath, user, lastseen, progress)

  try:
    connection = sqlite3.connect(dbFile)
  except sqlite3.Error as e:
    print(e)

  cursor = connection.cursor()

  upsertSql = '''insert into watchhistory values (?, ?, ?, ?)
                 on conflict(filepath, userid) do update
                                       set filepath=?,
                                           userid=?,
                                           lastseen=?,
                                           progress=?'''
  cursor.execute(upsertSql, res + res)

  connection.commit()
  connection.close()

  return flask.jsonify(res), 200

@api.route('/getProgress', methods=['GET'])
def getProgress():
  filepath = flask.request.args.get('filepath')
  userid = flask.request.args.get('userid')
  whereParam = (filepath, userid)

  try:
    connection = sqlite3.connect(dbFile)
  except sqlite3.Error as e:
    print(e)

  cursor = connection.cursor()

  selectSql = '''select progress from watchhistory where filepath=? and userid=?'''

  cursor.execute(selectSql, whereParam)

  try:
    progress = str(cursor.fetchone()[0])
  except TypeError:
    progress = '0'
  print('progress', progress)

  connection.commit()
  connection.close()


  return progress, 200

@app.route('/')
def homepage():
  return flask.render_template('index.html')

@app.route('/<path:path>')
def showMoviePage(path):
  #print(path)
  file = pathlib.Path(path)
  stem = file.stem
  return flask.render_template('play.html', moviePath=path, movieName=stem)

@app.route('/video/<path:path>')
def transferMovie(path):
  print("Sending:", path)
  return flask.send_from_directory('static', urllib.parse.unquote(path))


if __name__ == '__main__':
  app.register_blueprint(api)
  app.run(host='0.0.0.0', debug=True, port=5001)
