from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from flask_migrate import Migrate
import json


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class File(db.Model):
	__tablename__ = 'file'
	filename = db.Column(db.String(64))
	description = db.Column(db.String(32))
	data = db.relationship('Data', backref='file', lazy=True)
	id = db.Column(db.Integer, primary_key=True)

	def __init__(self, filename, description):
		self.filename = filename
		self.description = description


class Data(db.Model):
	__tablename__ = 'data'
	timestamp = db.Column(db.Integer)
	value = db.Column(db.Integer)
	file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
	id = db.Column(db.Integer, primary_key=True)

	def __init__(self, timestamp, value, file_id):
		self.timestamp = timestamp
		self.value = value
		self.file_id = file_id


class FileSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = File
		

class DataSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Data
		include_relationships = True


file_schema = FileSchema()
file_schemas = FileSchema(many=True)
data_schema = DataSchema()
data_schemas = DataSchema(many=True)


class getAll(Resource):
	@staticmethod
	def get():
		f =[]
		files = File.query.all()
		data = Data.query.join(File).all()
		for file in files:
			idx = file.id
			data = Data.query.join(File).filter(File.id==idx).all()
			file = json.loads(file_schema.dumps(file))
			data = json.loads(data_schemas.dumps(data))
			file['data'] = data
			f.append(file)
		return json.dumps(f)


class getOne(Resource):
	@staticmethod
	def get(): 
		try: idx = request.args['id']
		except: return json.dumps({'message':"provide id by adding to server address '/getOne?id=x' where x is id"})

		file = File.query.get(idx)
		if not file:
			return json.dumps({'message':'wrong index'})
		data = Data.query.join(File).filter(File.id==idx).all() 

		file = json.loads(file_schema.dumps(file))
		data = json.loads(data_schemas.dumps(data))
		file['data'] = data

		return json.dumps(file)


class delete(Resource):
	@staticmethod
	def delete():
		try: idx = request.args['id']
		except: json.dumps({'message':"provide id by adding to server address '/getOne?id=x' where x is id"})

		file = File.query.get(idx)
		if not file:
			return json.dumps({'message':'wrong index'})

		data = Data.query.join(File).filter(File.id==idx).all()
		db.session.delete(file)
		for d in data:
			db.session.delete(d)
		db.session.commit()
		return 'success', 200


class addOne(Resource):
	@staticmethod
	def post():
		try: data = request.json
		except: return '<h1>provide data in .json format</h1>'

		filename = data['filename']
		description = data['description']
		data = data['data']

		file = File(
		filename=filename,
		description=description)

		db.session.add(file)
		db.session.flush()

		for d in data:
			timestamp = d['timestamp']
			value = d['value']

			dic = Data(
				timestamp=timestamp,
				value=value,
				file_id=file.id)

			db.session.add(dic)

		db.session.commit()
		return 'success', 200

api.add_resource(getAll, '/getAll')
api.add_resource(getOne, '/getOne')
api.add_resource(delete, '/delete')
api.add_resource(addOne, '/addOne')


if __name__ == '__main__':
    app.run(debug=False)

