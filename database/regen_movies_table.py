#!/usr/pkg/bin/python3.10

import os
import sqlite3
import pathlib
import re
import unicodedata

dbFile = 'media-server.sqlite3'

movieRootPath = '../static/video'

def extractInfo(filepath):
  file = pathlib.Path(filepath)
  stem = file.stem
  normalizedStem = unicodedata.normalize('NFKC', stem).lower()
  normalizedFilePath = unicodedata.normalize('NFKC', filepath).lower()
  dir = file.parent.as_posix()
  suffix = file.suffix

  return normalizedStem, normalizedFilePath, dir, suffix


def truncateMovies(dbPath):
  try:
    connection = sqlite3.connect(dbPath)
  except sqlite3.Error as e:
    print(e)
  finally:
    cursor = connection.cursor()

  deleteSql = 'delete from movies'
  cursor.execute(deleteSql)
  connection.commit()

  vacuumSql = 'vacuum'
  cursor.execute(vacuumSql)
  connection.commit()

  connection.close()


def regenMoviesTable(dbPath):
  try:
    connection = sqlite3.connect(dbPath)
  except sqlite3.Error as e:
    print(e)
  finally:
    cursor = connection.cursor()

  for root, dirs, files in os.walk(movieRootPath):
    for file in files:
      filepath = os.path.join(root, file).replace(os.path.join(movieRootPath, ''), '')
      stem, normalizedFilePath, dir, suffix = extractInfo(filepath)
      insertSql = '''insert into movies values (?, ?, ?, ?, ?)
                     on conflict (filepath) do nothing'''
      cursor.execute(insertSql, [filepath, stem, normalizedFilePath, dir, suffix])

  connection.commit()
  connection.close()


if __name__ == '__main__':
  truncateMovies(dbFile)
  regenMoviesTable(dbFile)
