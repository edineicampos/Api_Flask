from email.policy import default
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource,fields
import sqlalchemy
import os
from datetime import datetime


basedir = os.path.dirname(os.path.realpath(__file__))#Nesta linha, o caminho absoluto do arquivo atual é obtido usando os.path.realpath(__file__). Em seguida, o diretório pai desse caminho é extraído usando os.path.dirname(). O resultado é armazenado na variável basedir.


app = Flask(__name__) # cria uma instância do aplicativo Flask, associando-o ao módulo ou pacote atual. A partir desse ponto, você pode adicionar rotas, definir comportamentos para diferentes URLs e iniciar o servidor web para executar o aplicativo Flask.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True

api = Api(app,doc='/',title="API",description="API FLASK")


db = SQLAlchemy(app)


class Book_res(db.Model):
    id= db.Column(db.Integer(),primary_key=True)
    title= db.Column(db.String(80),nullable=False)
    author = db.Column(db.String(40),nullable=False)
    date_added = db.Column(db.DateTime(),default=datetime.utcnow)

    def __repr__(self):
        return self.title
    
book_model = api.model(
    'Book_res',{
        'id':fields.Integer(),
        'title':fields.String(),
        'author':fields.String(),
        'date_joined':fields.String(),
    }
)

@api.route('/books')
class Books(Resource):
    @api.marshal_list_with(book_model,code=200,envelope="books")

    def get(self):
        '''METODO DE FILTRAR TODOS CADASTROS'''
        books = Book_res.query.all()
        return books            

    
    @api.marshal_with(book_model,code=200,envelope="book")
    def post(self):
        '''METO DE CRIAR'''
        data=request.get_json()

        title=data.get('title')
        author=data.get('author')

        new_book=Book_res(title=title,author=author)
        db.session.add(new_book)
        db.session.commit()
        return new_book


@api.route('/book/<int:id>')
class BookResource(Resource):
    @api.marshal_with(book_model,code=200,envelope="book")
    def get(self,id):
        '''METODO DE FILTRAR ID'''
        book=Book_res.query.get_or_404(id)
        return book,200
        
    @api.marshal_with(book_model,code=200,envelope="book")
    def put(self,id):
        '''METODO DE ATUALIZAR'''
        cad_book_update=Book_res.query.get_or_404(id)
        
        data=request.get_json()

        cad_book_update.title=data.get('title')
        cad_book_update.author=data.get('author')
        db.session.commit()
        return cad_book_update,200



    @api.marshal_with(book_model,code=200,envelope="book_delete")
    def delete(self,id):
       '''METODO DELETE'''
       cad_book_delete=Book_res.query.get_or_404(id)
       db.session.delete(cad_book_delete)
       db.session.commit()
       return cad_book_delete,200

@app.shell_context_processor
def make_shell_context():
    return{
        'db':db,
        'Book_res':Book_res
    }
if __name__ == "__main__":
    app.run(debug=True)