from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange, Length


class EditForm(FlaskForm):
    rating = FloatField("Rating out of 10",
                        validators=[DataRequired(),
                                    NumberRange(min=1, max=10,
                                                message="Invalid rating number")])
    review = StringField("Your review",
                         validators=[DataRequired()],
                         description="Enter your review")
    submit = SubmitField("Done")

class AddForm(FlaskForm):
    movie_title = StringField("Movie title", validators=[DataRequired(), Length(min=1, message="Enter movie title")])
    submit = SubmitField("Done")