from flask import Flask 
from flask_restplus import Api, Resource, fields
from werkzeug.utils import cached_property
from flask_mysqldb import MySQL 
from flask import jsonify
import sys
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'crudlite'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# api = Api(app)
api = Api(app,
          version='10.5',
          title='Flask Restplus CRUD',
          description='Demo to show various API parameters',
          license='MIT',
          contact='Mohit Sethi',
          contact_url='https://in.linkedin.com/in/mohitsethi',
          )


user_model_post = api.model('user_model_post', {'email' : fields.String('Enter your email'),'password':fields.String("Enter password")})
user_model_del = api.model('user_model_del', {'id' : fields.String('Enter id')})
user_model_patch = api.model('user_model_patch', {'id' : fields.String('Enter id'),'email' : fields.String('Enter your email'),'password':fields.String("Enter password")})

@api.route('/user')
class User(Resource):
	def get(self):
		cur = mysql.connection.cursor()
		cur.execute('''SELECT * FROM user''')
		results = cur.fetchall()
		return {'error':'false','message':"List of data",'data':results }

	@api.expect(user_model_post)
	def post(self):
	    cur = mysql.connection.cursor()
	    email = api.payload['email']
	    password = api.payload['password']
	    sql = """INSERT INTO user (email,password) VALUES (%s,%s)"""
	    input = (email,password)
	    rv = cur.execute(sql, input)
	    # print(rv, file=sys.stdout)
	    id = cur.lastrowid
	    # print(id, file=sys.stdout)
	    mysql.connection.commit()
	    return {'error':'false','message' : 'User added','data':{'id':id}}, 201

	@api.expect(user_model_del)
	def delete(self):
	    cur = mysql.connection.cursor()
	    id = api.payload['id']

	    sql = """DELETE from user where id =%s """
	    input = (id,)
	    rv = cur.execute(sql, input)
	    print(rv, file=sys.stdout)
	    # id = cur.lastrowid
	    # print(id, file=sys.stdout)
	    mysql.connection.commit()
	    return {'error':'false','message' : 'Deleted Sucessfully'}, 201

	@api.expect(user_model_patch)
	def patch(self):
	    cur = mysql.connection.cursor()
	    id = api.payload['id']
	    email = api.payload['email']
	    password = api.payload['password']
	    sql = """UPDATE user SET email=%s,password=%s where id =%s """
	    input = (email,password,id)
	    rv = cur.execute(sql, input)
	    print(rv, file=sys.stdout)
	    # id = cur.lastrowid
	    # print(id, file=sys.stdout)
	    mysql.connection.commit()
	    return {'error':'false','message' : 'Updated Sucessfully'}, 201

if __name__ == '__main__':
    
    app.run(debug=True)