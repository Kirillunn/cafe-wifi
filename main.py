from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, URLField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


# Create db object
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = '1728395Lka!'

# Create form for a new cafe
class New_cafe(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = URLField('Map URL', validators=[DataRequired(), URL()])
    img_url = URLField('Image URL', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = BooleanField('Sockets', validators=[DataRequired()])
    has_toilet = BooleanField('Toilet', validators=[DataRequired()])
    has_wifi = BooleanField('WiFi', validators=[DataRequired()])
    can_take_calls = BooleanField('Calls', validators=[DataRequired()])
    seats = StringField("Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])


# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
# initialize the app with the extension
db.init_app(app)

# Define Model
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=True)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=True)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=True)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=True)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

# Get unique locations from db (for navbar)
def get_unique_locations():
    with app.app_context():
        loc_result = db.session.execute(db.select(Cafe.location).distinct())
        return loc_result.scalars().all()

unique_locations = get_unique_locations()

# Create table
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # Get all cafes from db
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()
    midpoint = round(len(cafes) / 2)
    return render_template('index.html', cafes=cafes, midpoint=midpoint, locations=unique_locations)


# Filter cafe by locations
@app.route("/locations")
def select_location():
    # Get location which user choose
    location = request.args.get('location')

    # Get all cafes from location
    result = db.session.execute(db.select(Cafe).where(Cafe.location == location))
    cafes = result.scalars().all()
    midpoint = round(len(cafes) / 2)
    return render_template('index.html', cafes=cafes, midpoint=midpoint, locations=unique_locations)

@app.route("/wifi", methods=["GET", "POST"])
def select_wifi():
    # When user presses "Wi-Fi" button
    if request.method == "POST":
        # Get all cafes with wi-fi from db
        result = db.session.execute(db.select(Cafe).where(Cafe.has_wifi == True))
        cafes_with_wifi = result.scalars().all()
        midpoint = round(len(cafes_with_wifi) / 2)
        return render_template('index.html', cafes=cafes_with_wifi, midpoint=midpoint, locations=unique_locations)

@app.route("/sockets", methods=["GET", "POST"])
def select_sockets():
    # When user presses "Sockets" button
    if request.method == "POST":
        # Get all cafes with sockets from db
        result = db.session.execute(db.select(Cafe).where(Cafe.has_sockets == True))
        cafes_with_sockets = result.scalars().all()
        midpoint = round(len(cafes_with_sockets) / 2)
        return render_template('index.html', cafes=cafes_with_sockets, midpoint=midpoint, locations=unique_locations)


@app.route("/toilet", methods=["GET", "POST"])
def select_toilet():
    # When user presses "Toilet" button
    if request.method == "POST":
        # Get all cafes with toilet from db
        result = db.session.execute(db.select(Cafe).where(Cafe.has_toilet == True))
        cafe_with_toilet = result.scalars().all()
        midpoint = round(len(cafe_with_toilet) / 2)
        return render_template("index.html",cafes=cafe_with_toilet, midpoint=midpoint, locations=unique_locations)


@app.route("/calls", methods=["GET", "POST"])
def select_calls():
    # When user presses "Calls" button
    if request.method == "POST":
        # Get all cafes with calls from db
        result = db.session.execute(db.select(Cafe).where(Cafe.can_take_calls == True))
        cafe_with_calls = result.scalars().all()
        midpoint = round(len(cafe_with_calls) / 2)
        return render_template("index.html",cafes=cafe_with_calls, midpoint=midpoint, locations=unique_locations)


# Add new cafe to the db
@app.route('/add_cafe', methods=["GET", "POST"])
def add_cafe():
    form = New_cafe()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            seats = form.seats.data,
            has_toilet = form.has_toilet.data,
            has_wifi = form.has_wifi.data,
            has_sockets = form.has_sockets.data,
            can_take_calls = form.can_take_calls.data,
            coffee_price = form.coffee_price.data
        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add_cafe.html', form=form, locations=unique_locations)


# Delete cafe from db
@app.route('/delete_cafe/<int:cafe_id>', methods=['GET', 'POST'])
def delete_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)






