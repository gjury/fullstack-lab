# app.py

from flask import Flask, Response, json, request, send_from_directory
from pony.orm import *
from pony.orm.serialization import to_dict
import json

db = Database()
db.bind(provider='sqlite', filename=':memory:')

class Risk(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    valuesph = Set('Value')


class Risk_attr(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    type = Required(str)
    valueph = Set('Value')
    enum_values = Set('Enum_value')


class Enum_value(db.Entity):
    id = PrimaryKey(int, auto=True)
    value = Required(str)
    risk_attrph = Optional(Risk_attr)


class Value(db.Entity):
    id = PrimaryKey(int, auto=True)
    value = Optional(str)
    risk = Required(Risk)
    risk_attr = Required(Risk_attr)

db.generate_mapping(create_tables=True)



app = Flask(__name__, static_url_path='')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# here is how we are handling routing with flask:
@app.route('/')
def index():
    return app.send_static_file('index.html')
    #return "Hello World!", 200



@app.route('/user', methods=["GET", "POST"])
def user():
    resp_dict = {}
    if request.method == "GET":
        resp_dict = {"first_name": "John", "last_name": "doe"}
    if request.method == "POST":
        data = request.form
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        email = data.get("email", "")
        resp_dict = {"first_name": first_name, "last_name": last_name, "email": email}
    response = Response(json.dumps(resp_dict), 200)
    return response

@app.route('/risks', methods=["GET"])
@db_session
def risks():
    #response = Response('[{"id": 1, "name": "Paraglider", "description": "Need to protect my investment on flying", "values": [2, 3, 5]},{"id": 2, "name": "Boat", "description": "a lot of money invested on it", "values": [1, 4]}]', 200)
    risks=select(r for r in Risk)[:]
    response = Response(json.dumps(to_dict(risks)['Risk']),200)
    return response

@app.route('/risk/<riskid>', methods=["GET"])
@db_session
def risk(riskid):
    #response = Response('[{"id": 1, "name": "Paraglider", "description": "Need to protect my investment on flying", "values": [2, 3, 5]},{"id": 2, "name": "Boat", "description": "a lot of money invested on it", "values": [1, 4]}]', 200)
    #risk=select((v) for v in Value if v.risk.id==riskid)[:]
    #riskd=to_dict(risk)
    values=db.select("SELECT va.value, ra.type, ra.name, en.value from VALUE va, Risk_attr ra left outer join Enum_value en on en.risk_attrph=ra.id WHERE va.risk_attr=ra.id and va.risk=$riskid ")
    res={}
    prev=None
    for el in values:
        if(el[0]!=prev):
            val=[]
        val.append(el[3])
        res[el[0]]={'value':el[0],'type':el[1],'name':el[2],'enumv':val[:]}
        prev=el[0]

    response = Response(json.dumps(list(res.values())),200)
    return response

@app.route('/initdb', methods=["GET"])
@db_session
def initdb():
    rp=Risk(name='Paraglider',description='Need to protect my investment on flying')
    rb=Risk(name='Boat', description='a lot of money invested on it')

    ra=[0]*5
    ra[0]=Risk_attr(name='Address',type='string')
    ra[1]=Risk_attr(name='Valuation', type='number')
    ra[2]=Risk_attr(name='StealableIndex',type='enum',enum_values=[Enum_value(value='High'),Enum_value(value='Medium'),Enum_value(value='Low')])
    ra[3]=Risk_attr(name='Purchase',type='date')
    ra[4]=Risk_attr(name='Clause',type='string')

    Value(value='5000',risk=rp,risk_attr=ra[1])
    Value(value='One Way 500',risk=rp,risk_attr=ra[0])
    Value(value='Paragliding is a dangerous thing, please keep it safe',risk=rp,risk_attr=ra[4])
    Value(value='10000000',risk=rb,risk_attr=ra[1])
    Value(value='Bay by the Harbor',risk=rb,risk_attr=ra[0])
    Value(value='High',risk=rb,risk_attr=ra[2])
    Value(value='2018-01-03',risk=rb,risk_attr=ra[3])
    Value(value='Sailing is one of the most wonderful experiences',risk=rb,risk_attr=ra[4])
    commit()
    response = Response('OKK', 200)
    return response



#Out[38]: '{"Risk": {"1": {"id": 1, "name": "Paraglider", "description": "Need to protect my investment on flying", "values": [2, 3, 5]}}, "Value": {"5": {"id": 5, "value": "If you are not carefull enough, then this policy will not apply", "risk": 1, "risk_attr": 3}, "3": {"id": 3, "value": "2018-01-03", "risk": 1, "risk_attr": 2}, "2": {"id": 2, "value": "3000", "risk": 1, "risk_attr": 1}}}'
#Out[41]: '{"Risk": {"2": {"id": 2, "name": "Boat", "description": "a lot of money invested on it", "values": [1, 4]}}, "Value": {"4": {"id": 4, "value": "2017-03-03", "risk": 2, "risk_attr": 2}, "1": {"id": 1, "value": "1000000", "risk": 2, "risk_attr": 1}}}'
# include this for local dev

if __name__ == '__main__':
    app.run()
