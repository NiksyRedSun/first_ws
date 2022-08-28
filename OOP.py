from flask import Flask, request
import json
import random
app = Flask(__name__)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        info = 'Hi, I\'m ' + (self.name).capitalize() + ' ' + 'and I\'m ' + str(self.age)
        return info

    def short_info(self):
        short_info = 'Name: ' + (self.name).capitalize() + ',' + ' ' + 'age: ' + str(self.age)
        return short_info

niksy = Person('niksy', 25)
andrew = Person('andrew', 25)
zheka = Person('zheka', 25)
ilya = Person('ilya', 25)

slovnik = {
    niksy.name:niksy,
    andrew.name:andrew,
    zheka.name:zheka,
    ilya.name:ilya,
}

names = ['john', 'jack', 'bill', 'sady', 'chavier', 'charles', 'arthur', 'leopold', 'shon', 'caren']

def CheckInputs(inputs, requires):
    for param in requires:
            if param not in inputs:
                return (json.dumps({'status': 'data_error', 'message': f'{param} expected'}), 400)
    return 'passed'

@app.route('/users')
def show_users_profile():
    slovnik_info = ''
    for value in slovnik.values():
        slovnik_info += str(value.short_info()) + '; '
    return slovnik_info

@app.route('/user/<user>')
def show_user_profile(user):
    if user in slovnik:
        return json.dumps(slovnik[user].info())
    else:
        return json.dumps('You are looking for the wrong person')

@app.route('/user/<user>', methods=['DELETE'])
def delete_user_profile(user):
    if user in slovnik:
        del slovnik[user]
        deleted_data = user.capitalize() + ' ' + 'had deleted even before you thought about it'
        return json.dumps(deleted_data)
    else:
        return json.dumps('You are trying to delete unregistered person')

@app.route('/user/<user>', methods=['POST'])
def post_user_profile(user):
    inputs = request.get_json()
    check = CheckInputs(inputs,  ['name', 'age'])
    if check != 'passed':
        return check
    if user not in slovnik:
        age = inputs['age']
        user = Person(user, age)
        slovnik[user.name] = user
        posted_data = (user.name).capitalize() + ' ' + 'has been successfully added to dictionary'
        return json.dumps(posted_data)
    else:
        return json.dumps('This person is alredy on the list')

@app.route('/postrandom', methods=['POST'])
def post_random_profile():
    if len(names) > 0:
        name = random.choice(names)
        age = random.randint(16, 55)
        user = Person(name, age)
        names.remove(name)
        slovnik[user.name] = user
        posted_data = (user.name).capitalize() + ' ' + 'that is ' + str(user.age) + ' ' + 'has been successfully added to dictionary'
        return json.dumps(posted_data)
    else:
        return json.dumps('There is no free nicknames left')

@app.route('/user/<user>', methods=['PUT'])
def put_user_profile(user):
    inputs = request.get_json()
    check = CheckInputs(inputs, ['name', 'age'])
    if check != 'passed':
        return check
    if user in slovnik:
        prevname = user.capitalize()
        name = inputs['name']
        age = inputs['age']
        del slovnik[user]
        user = Person(name, age)
        slovnik[user.name] = user
        posted_data = prevname + ' has been changed successfully for ' + (user.name).capitalize()
        return json.dumps(posted_data)
    else:
        return json.dumps('You are trying to change unregistered person')

if __name__ == '__main__':
    app.run(debug = True, port = 5001)