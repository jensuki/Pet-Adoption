from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

default_pet_image = "https://archive.org/download/placeholder-image/placeholder-image.jpg"

# configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 's3cr3tk3y'


# connect DB + Flask app
connect_db(app)
db.create_all()
debug = DebugToolbarExtension(app)

@app.route('/')
def pet_list():
    """Show list of pets"""

    pets = Pet.query.all() # get all pets from DB
    return render_template('pet_list.html', pets=pets) # render template with pet data

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Show form to add pet + handle submit pet form"""

    form = AddPetForm() # create instance of AddPetForm

    if form.validate_on_submit(): # if form is submitted & valid
        pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data or default_pet_image,
            age=form.age.data,
            notes=form.notes.data,
            available=form.available.data
        )

        db.session.add(pet)
        db.session.commit()

        return redirect('/') # redirect to home / after successful addition
    else:
        return render_template('add_pet_form.html', form=form)

@app.route('/<int:pet_id>', methods=['GET'])
def pet_detail(pet_id):
    """Show pet details"""

    pet = Pet.query.get_or_404(pet_id) # get pet

    return render_template('pet_details.html', pet=pet, default_pet_image=default_pet_image)

@app.route('/<int:pet_id>/edit', methods=['GET', 'POST'])
def edit_pet(pet_id):
    """Edit pet details"""

    pet = Pet.query.get_or_404(pet_id) # get pet to edit

    form = EditPetForm(obj=pet) # create instance of EditPetForm with loaded pet data

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data or default_pet_image
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()

        return redirect(f'/{pet.id}')
    else:
        return render_template('edit_pet_form.html', pet=pet, form=form, default_pet_image=default_pet_image)


