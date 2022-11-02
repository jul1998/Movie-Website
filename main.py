from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests
from wft_form import EditForm, AddForm



db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Movies.db"
Bootstrap(app)
app.app_context().push()
db.init_app(app)

MOVIES_API_KEY = "KEY"
MOVIES_URL_API = f"https://api.themoviedb.org/3/search/movie/"
MOVIES_URL_API_ID = "https://api.themoviedb.org/3/movie"

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)



# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
#
# db.session.add(new_movie)
# db.session.commit()

@app.route("/")
def home():
    #movies_data = db.session.query(Movie).all()
    sorted_movies_data = Movie.query.order_by(Movie.rating.asc()).all()
    print(sorted_movies_data)
    for index, movie in enumerate(sorted_movies_data):
         new_rank = len(sorted_movies_data)-index
         movie.ranking = new_rank
         print(new_rank)
    db.session.commit()
    return render_template("index.html", movies_data=sorted_movies_data)

@app.route("/edit/id/<int:movie_id>", methods=['GET', 'POST'])
def edit(movie_id):
    form = EditForm()
    if form.validate_on_submit():
        #Data given by user input
        form_rating = form.rating.data
        form_review = form.review.data

        #Update rating column
        rating_id = Movie.query.get(movie_id)
        rating_id.rating = form_rating

        #Update review column
        review_id = Movie.query.get(movie_id)
        review_id.review = form_review
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("edit.html", form=form)

@app.route("/delete/id/<int:movie_id>")
def delete(movie_id):
    movie_id = movie_id
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/add", methods=['GET', 'POST'])
def add():
    add_form = AddForm()
    params = {
        "api_key": MOVIES_API_KEY,
        "query": add_form.movie_title.data
    }
    if add_form.validate_on_submit():
        data = requests.get(url=MOVIES_URL_API, params=params).json()
        movie_titles = data["results"]
        return render_template("select.html", movie_titles=movie_titles)
    return render_template("add.html", add_form=add_form)

@app.route("/movie_id/<int:movie_id>")
def select_movie_by_id(movie_id):
    params = {
        "api_key": MOVIES_API_KEY,
    }

    data = requests.get(url=f"{MOVIES_URL_API_ID}/{movie_id}", params=params).json()
    movie_overview = data["overview"]
    movie_title = data["title"]
    movie_release_data = data["release_date"].split("-")[0]
    movie_img_url = data["poster_path"]
    movie_base_img_url = "https://image.tmdb.org/t/p/w500"

    new_movie = Movie(title=movie_title,
                      year=movie_release_data,
                      description=movie_overview,
                      rating=10.0,
                      ranking=0,
                      review="Awesome",
                      img_url=f"{movie_base_img_url}{movie_img_url}")
    db.session.add(new_movie)
    db.session.commit()
    db.create_all()



    return redirect(url_for("home"))




if __name__ == '__main__':
    app.run(debug=True)
