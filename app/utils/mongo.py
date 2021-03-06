# coding=utf_8

import pymongo

import app.utils.config as config

client = pymongo.MongoClient(config.get_database_server_url(), config.get_database_server_port())

db = client['reviews']

review = db.review
score = db.score
