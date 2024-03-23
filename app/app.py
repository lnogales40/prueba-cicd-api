from typing import List, Dict
from flask import Flask
from flask_restplus import Api, Resource

import mysql.connector
import json

app = Flask(__name__)
api = Api(app)


def favorite_colors() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'knights'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM favorite_colors')
    results = [{name: color} for (name, color) in cursor]
    cursor.close()
    connection.close()

    return results


@api.route('/favorite_colors')
class FavoriteColors(Resource):
    def get(self) -> List[Dict]:
        """List all favorite colors"""
        return favorite_colors()


if __name__ == '__main__':
    app.run(host='0.0.0.0')

