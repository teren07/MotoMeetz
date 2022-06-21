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


@app.route('/update/ride/<int:id>',methods=['POST'])
def update_ride(id):
    # update ride if they are in session 
    if 'user_id' not in session:
        return redirect('/logout')
    if not ride.Ride.validate_newride(request.form):
        return redirect(f'/edit/ride/{id}')
        # here is the data being used/entered on mysql 
    data = {
        "id":id,
        "location": request.form["location"],
        "date": request.form["date"],
        "time": request.form["time"],
        "skill_level": request.form["skill_level"],
        "bike_type": request.form["bike_type"],
        "description": request.form["description"], 
    }
    # after submitted update their recipe and return to dashboard
    ride.Ride.update(data)
    return redirect('/dashboard')

def update_ride1():
    if not ride.Ride.validate_newride(request.form):
        return redirect('/dashboard')

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
        ride.Ride.edit(data)
        return redirect('/dashboard')













@app.route('/delete/ride/<int:id>')
def delete(id):
    ride.Ride.delete_ride(id)
    return redirect('/dashboard')





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

    # return redirect(f"/edit/ride/{id}")
    return redirect('/dashboard')



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
    # their  own ride
    return render_template("edit.html",ride=ride.Ride.get_one(data),user=user.User.grab_userid(user_data))
