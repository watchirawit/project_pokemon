
import re
from flask.json import tag
import requests
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webadmin:ZQQcoa88817@node17333-wachirawit.app.ruk-com.cloud:11107/mydb'
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
db = SQLAlchemy(app)

   

    

class User(db.Model) :
    __tablename__ = 'Data_pokemon'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    Photo = db.Column(db.String(100))
    Description = db.Column(db.String(1000))
    types = db.Column(db.String(100))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    special_attack = db.Column(db.Integer)
    special_defense = db.Column(db.Integer)

@app.route('/', methods=['GET', 'POST'])
def index() :
    result = User.query.all()
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form['tag']
        search = "%{}%".format(tag.lower())
        result = User.query.filter(User.name.like(search))
        
        return render_template('index6.html',result=result,tag=tag)
    return render_template('index6.html',result=result)


@app.route('/About')
def About() :
    return render_template('About.html')



@app.route('/search')
def search():
    result = User.query.whoosh_search(request.args.get('query')).all()
    return render_template('index6.html',result=result)




    


def create_db_user() :
    db.drop_all()
    db.create_all()
    for i in range(898):
        gg(i+1)
    db.session.commit()
    print('create done')

def gg(num):
    api = f'https://pokeapi.co/api/v2/pokemon/{num}/'
    api_x = f'https://pokeapi.co/api/v2/pokemon-species/{num}/'
    res = requests.get(api)
    res_x = requests.get(api_x)
    poked = res.json()
    pokedc_x = res_x.json()
    Types_x = []
    Stats_x = []
    break_loop = 0
    Description_pokemon = '' 
    for k in poked['types']:
        Types_x.append(k['type']['name'])
    for k in poked['stats']:
        Stats_x.append(k['base_stat'])

    for text_for_poke in pokedc_x['flavor_text_entries']:
        if text_for_poke['language']['name'] == 'en':
            if break_loop != 1:
                for text in text_for_poke['flavor_text']:
                    if text != '\n':
                        Description_pokemon += text
                break_loop += 1    
    user = User(name=poked['name'], Photo=poked['sprites']['front_default']
    , weight=(poked['weight']/10), types=str(Types_x), 
    hp=Stats_x[0], attack=Stats_x[1], defense=Stats_x[2], special_attack=Stats_x[3], special_defense=Stats_x[4], speed=Stats_x[5],
    height=(poked['height']/10), Description=Description_pokemon)
    db.session.add(user)

#create_db_user()

if __name__ == "__main__" :
    app.run(host='0.0.0.0', debug=True,port=88)