from calendar import c
from flask_app import app
from flask import render_template, redirect,session, request
from flask_app.models import ride, user

@app.route('/ride/new')
def new_ride():
    return render_template('new_ride.html')
# this is the one u are currently editing 
@app.route('/ride/create', methods=['POST'])
def create_ride():
    if not ride.Ride.validate_newride(request.form):
        return redirect('/ride/new')

    else:
        data = {
            "location": request.form["location"],
            "date": request.form["date"],
            "time":request.form["time"],
            "skill_level":request.form["skill_level"],
            "bike_type":request.form["bike_type"],
            "description": request.form["description"],
            "user_id": session["user_id"],
        }
        ride.Ride.save(data)
        return redirect('/dashboard')


@app.route('/ride/<int:id>/update', methods=['POST'])
def update(id):
    if "user_id" not in session:
        return redirect('/dashboard')

    else:
        data= {
            "location": request.form["location"],
            "date": request.form["date"],
            "time":request.form["time"],
            "skill_level":request.form["skill_level"],
            "bike_type":request.form["bike_type"],
            "description": request.form["description"],
            "id":['id'],
        }

        ride.Ride.edit(data)
        return redirect('/dashboard')

# @app.route('/delete/<int:id>')
# def delete_car(id):
#     car.Car.delete_car(id)
#     return redirect ('/dashboard')

@app.route('/delete/ride/<int:id>')
def delete(id):
    ride.Ride.delete_ride(id)
    return redirect('/dashboard')


# @app.route('/delete/car/<int:id>')
# def delete_car(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "id":id
#     }
#     car.Car.delete_car(data)
#     return redirect('/dashboard')


@app.route('/view/ride/<int:id>')
def show_show(id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("ride.html",ride=ride.Ride.get_one(data),apple=user.User.grab_userid({'id':session['user_id']}),postedby=user.User.grab_userid({'id':ride.Ride.get_one(data).user_id})
        )


@app.route('/edit/ride/<int:id>', methods=["POST"])
def edit(id):
    if "user_id" not in session:
        return redirect('/')
    

    ride.Ride.edit(request.form)

    # return redirect(f"/edit/car/{id}")
    return redirect('/dashboard')
    # else:
        # data = {
        #     "price":request.form['price'],
        #     "model":request.form['model'],
        #     "make":request.form['make'],
        #     "year":request.form['year'],
        #     "description": request.form['description'],
        #     "user":request.form['user'],
        # }

    # car.Car.edit(data)
    # return redirect('/dashboard')


@app.route('/edit/ride/<int:id>')
def edit_ride(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    # if they are in session use user id and go to edit.html so they an edit
    # their  own recipe
    return render_template("edit.html",ride=ride.Ride.get_one(data),user=user.User.grab_userid(user_data))