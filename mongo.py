from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
import json
from bson.json_util import dumps

from functools import wraps
from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, create_access_token,
    get_jwt_claims, get_jwt_identity
)

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'RssFeedApiDatabase'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/RssFeedApiDatabase'
app.config['JWT_SECRET_KEY'] = 'secret'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


def protect_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims:
            print(claims)
            return jsonify(msg='jwt missing'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper



@app.route('/api/users/register', methods=['POST'])
def register():
    users = mongo.db.users
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()
    favori_rss = []
    user_id = users.insert({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created,
        'favori_rss': favori_rss
    })
    new_user = users.find_one({'_id': user_id})

    result = {'email': new_user['email'] + ' registered'}

    return jsonify({'result': result})


@app.route('/api/users/login', methods=['POST'])
def login():
    users = mongo.db.users
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    response = users.find_one({'email': email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity={
                'first_name': response['first_name'],
                'email': response['email']}
            )
            result = jsonify({"token": access_token})
        else:
            result = jsonify({"error": "Invalid username and password"})
    else:
        result = jsonify({"result": "No results found"})
    return result


@app.route('/api/rss', methods=['GET'])
@protect_required
def get_all_rss():
    rss = mongo.db.rssFeed

    result = []
     
    datas = rss.find()

    for data in datas:
        result.append({'_id':str(data['_id']),
        'title': data['title'],
        'link': data['link'],
        'description': data['description'],
        'updated': data['updated'],
        'location': data['location']})
    return jsonify(result)


@app.route('/api/get_rss_by_id/<string:id>', methods=['GET'])
@protect_required
def get_rss_by_id(id):
    
    rss = mongo.db.rssFeed
    get_rss = rss.find_one({'_id': ObjectId(id)}) 

    return dumps(get_rss)


@app.route('/api/rss_add_favorite/<string:id>', methods=['POST'])
@protect_required
def post_favorite_rss(id):

    rss = mongo.db.rssFeed
    added_rss = rss.find_one({'_id': ObjectId(id)}) #eklenecek rss

   
    added_rss_id = added_rss['_id']

    current_user = get_jwt_identity()
    email = str(current_user['email'])
    user = mongo.db.users
    find_user_by_email_addres = user.find_one({'email':email})
    user_fav_rss = []
    user_fav_rss = find_user_by_email_addres['favori_rss']
    print(dumps(user_fav_rss))
    
    if not user_fav_rss:
        find_user_by_email_addres['favori_rss'].append(added_rss_id)
        user.save(find_user_by_email_addres)
        return dumps(find_user_by_email_addres)    
    else:
        if added_rss_id not in user_fav_rss:
                find_user_by_email_addres['favori_rss'].append(added_rss_id)
                user.save(find_user_by_email_addres)
                
                return dumps(find_user_by_email_addres)  
        else:
            print('do not make anything')
            return dumps(find_user_by_email_addres)
    return dumps(find_user_by_email_addres)

@app.route('/api/get_favorite_rss', methods=['GET'])
@protect_required
def get_favorite_rss():
    
    current_user = get_jwt_identity()
    email = str(current_user['email'])

    user = mongo.db.users
    find_user_by_email_addres = user.find_one({'email':email})
    
    fav_rss = []
    fav_rss = find_user_by_email_addres['favori_rss']
    rss = mongo.db.rssFeed

    finding_rss = []
    for x in fav_rss:
        id = x
        finding_rss.append(rss.find_one({'_id': ObjectId(id)}))
    
    return dumps(finding_rss)
    
@app.route('/api/get_rss_with_date', methods=['POST'])
@protect_required
def get_rss_with_date():
    rss = mongo.db.rssFeed

    start_date = request.get_json()['start_date']
    end_date = request.get_json()['end_date']

    start_date_year = start_date[0:4]
    start_date_mounth = start_date[5:7]
    start_date_day = start_date[8:10]
    start_date_hour = start_date[11:13]
    start_date_minutes = start_date[14:16]
    
    end_date_year = end_date[0:4]
    end_date_mounth = end_date[5:7]
    end_date_day = end_date[8:10]
    end_date_hour = end_date[11:13]
    end_date_minutes = end_date[14:16]

    to_date = start_date_year + "-" + start_date_mounth + "-" + start_date_day + "T" + start_date_hour + ":" + start_date_minutes
    from_date = end_date_year + "-" + end_date_mounth + "-" + end_date_day + "T" + end_date_hour + ":" + end_date_minutes 

    to_date_time = datetime.strptime(to_date, '%Y-%m-%dT%H:%M')
    from_date_time = datetime.strptime(from_date, '%Y-%m-%dT%H:%M')

    result = []
    
    datas = rss.find({'updated': {'$gte':to_date_time, '$lt': from_date_time}})
    
    for data in datas:
        result.append({'_id':str(data['_id']),
        'title': data['title'],
        'link': data['link'],
        'description': data['description'],
        'updated': data['updated'],
        'location': data['location']})
    print('result:',result)
    return jsonify(result)
    

if __name__ == '__main__':
    app.run(debug=True)
