from flask import Flask ,redirect,render_template,request,url_for
from shorten import createid
from flask_sqlalchemy import SQLAlchemy
import re



app=Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'


db = SQLAlchemy(app)
#### handeling errors
# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_server_error(e):
#     # note that we set the 500 status explicitly
#     return render_template('500.html'), 500

# ###############################
#Creating the database 
class LINKS(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    link= db.Column(db.String(1000))
    linkid = db.Column(db.String(6),unique=True)




######################################
def addnewlink(url):
    id =createid()
    if str(LINKS.query.filter_by(linkid=id).first()) != 'None':
        while str(LINKS.query.filter_by(linkid=id).first()) != 'None' :
            id =createid()
    newlink = LINKS(link=url,linkid=id)
    db.session.add(newlink)
    db.session.commit()
    return id



@app.route('/',defaults={'url': 'URL SHORTNER'})
def home(url):
    return render_template('home.html',url=url)


@app.route('/<id>')
def redirectto(id):
    link= LINKS.query.filter_by(linkid=id).first()
    return redirect(link.link)


@app.route('/shorten',methods=['POST','GET'])
def shorten():
    x=request.form.get('link')

    if re.search('https?://\w+.+',x) != None:
        print(x+' is a link')
        x=addnewlink(x)
        message='SUCCESS Your Link is ' + "http://127.0.0.1:5000" + url_for("home")+x
        return render_template('home.html',url=message)
    else:
        message= 'SORRY Not a Link Try Again'
        return render_template('home.html',url=message)
   


if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()