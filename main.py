from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book-collection.db"
db.init_app(app)







# all_books = []

"""This class creates the model of the data base table"""
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)

"""This commands creates the database"""
with app.app_context():
    db.create_all()








@app.route('/')
def home():
    """This command select the data from the database and display every item"""
    """To show all requests it is used scalarS with plural, if you need just one item you use scalar() in singular"""
    all_books = db.session.execute(db.select(Books).order_by(Books.id)).scalars()
    return render_template('index.html', all_books=all_books)








@app.route('/<id>')
def delete(id):
    """Deleting a book from the data base"""
    book_to_delete = db.session.execute(db.select(Books).where(Books.id == id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()

    """After deleting an item , all the data has to be render"""
    all_books = db.session.execute(db.select(Books).order_by(Books.id)).scalars()
    return render_template('index.html',all_books=all_books)









@app.route("/add", methods=["GET", "POST"])
def add():
    """Creating the form with all the inputs"""
    class MyForm(FlaskForm):
        book_name = StringField("Book Name", validators=[DataRequired()])
        book_author = StringField("Book Author", validators=[DataRequired()])
        book_rating = StringField("Book Rating", validators=[DataRequired()])
        submit = SubmitField("Submit", validators=[DataRequired()])

    form = MyForm()
    """"""
    if form.validate_on_submit():
        # book_details = {
        #     'name': form["book_name"].data,
        #     'author': form["book_author"].data,
        #     'rating': form["book_rating"].data
        # }
        # all_books.append(book_details)

        """A new dict is created with all the data passed in the form in order to add it to the database"""
        new_book = Books(
            title=form["book_name"].data,
            author=form["book_author"].data,
            rating=form["book_rating"].data

        )
        db.session.add(new_book)
        db.session.commit()



        return redirect(url_for("home"))

    return render_template('add.html', form=form)











@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    class MyForm(FlaskForm):
        book_new_rating = StringField("Rating", validators=[DataRequired()])
        submit = SubmitField("Edit Rating", validators=[DataRequired()])


    form = MyForm()

    all_books = db.session.execute(
     db.select(Books).order_by(Books.id)).scalar()

    if form.validate_on_submit():
        book_to_update = db.session.execute(db.select(Books).where(Books.id == id)).scalar()
        book_to_update.rating = form["book_new_rating"].data
        db.session.commit()


        return redirect(url_for('home'))

    return render_template("edit.html", all_books=all_books, form=form)














app.secret_key = "123"

if __name__ == "__main__":
    app.run(debug=True)
