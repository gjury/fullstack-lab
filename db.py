from pony.orm import *


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

@db_session
def create_tables():
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
    return rp
