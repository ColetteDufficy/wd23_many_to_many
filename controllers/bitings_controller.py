from flask import Blueprint, Flask, redirect, render_template, request

from models.biting import Biting
import repositories.biting_repository as biting_repository
import repositories.zombie_repository as zombie_repository
import repositories.human_repository as human_repository



bitings_blueprint = Blueprint("bitings", __name__)

# INDEX
# GET '/bitings'
@bitings_blueprint.route("/bitings")
def bitings():
    bitings = biting_repository.select_all() 
    return render_template("bitings/index.html", bitings = bitings)

# NEW
# GET '/bitings/new'
@bitings_blueprint.route("/bitings/new", methods=['GET'])
def new_biting():
    zombies = zombie_repository.select_all()
    humans = human_repository.select_all()
    return render_template("bitings/new.html", zombies = zombies, humans = humans)


# CREATE
# POST '/bitings'
@bitings_blueprint.route("/bitings",  methods=['POST'])
def create_biting():
    human_id = request.form['human_id']
    zombie_id = request.form['zombie_id']

    human = human_repository.select(human_id)
    zombie = zombie_repository.select(zombie_id)
    biting = Biting(human, zombie)
    biting_repository.save(biting)
    return redirect('/bitings')



# EDIT (EDIT and UPDATE are combined)
# GET '/bitings/<id>/edit'
# Step 1:
@bitings_blueprint.route("/bitings/<id>/edit", methods=["GET"])
def edit_biting(id):
    biting = biting_repository.select(id)
    zombies = zombie_repository.select_all() 
    humans = human_repository.select_all()
    return render_template("bitings/edit.html", biting=biting, zombies = zombies, humans = humans)



# UPDATE
# POST '/bitings/<id>'
@bitings_blueprint.route("/bitings/<id>", methods=['POST'])
def update_biting(id):
    human_id = request.form['human_id']
    zombie_id = request.form['zombie_id']
    
    human = human_repository.select(human_id) 
    zombie = zombie_repository.select(zombie_id) 
    biting = Biting(human, zombie, id)

    biting_repository.update(biting)
    return redirect('/bitings')





# DELETE '/bitings/<id>'
# POST '/bitings'
@bitings_blueprint.route("/bitings/<id>/delete", methods=['POST'])
def delete_biting(id):
    biting_repository.delete(id)
    return redirect('/bitings')
