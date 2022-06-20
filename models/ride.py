from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, ride

class Ride:
    db_name="users_and_rides"
    def __init__(self,data):
        self.id = data["id"]
        self.location=data["location"]
        self.date=data["date"]
        self.time=data["time"]
        self.skill_level=data["skill_level"]
        self.bike_type=data["bike_type"]
        self.description=data["description"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.user_id=data['user_id']
        self.user = None

    @classmethod
    def save(cls, data): 
        query = "INSERT INTO rides (location, date, time, skill_level, bike_type, description, user_id) VALUES (%(location)s, %(date)s, %(time)s,%(skill_level)s, %(bike_type)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_rides(cls):
            query = "SELECT * FROM rides  JOIN users on rides.user_id = users.id;"
            results= connectToMySQL(cls.db_name).query_db(query)
            rides = []
            for row in results:
                ride = cls(row)
                user_data ={
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at':row['created_at'],
                    'updated_at': row['updated_at'],
                }
                ride.user = user.User(user_data)
                rides.append(ride)
            return rides
    @classmethod
    def get_all_rides_with_users(cls):
        query="SELECT * FROM rides JOIN users ON rides.user_id= users.id;"
        results=connectToMySQL(cls.db_name).query_db(query)
        print(results)
        if len(results)==0:
            return []
        else:
            all_ride_instances =[]
            
            for current_ride_dictionary in results:

                ride_instance=cls(current_ride_dictionary)

                new_user_dictionary = {
                    "id":current_ride_dictionary["user.id"],
                    "first_name":current_ride_dictionary["user.first_name"],
                    "last_name": current_ride_dictionary["user.last_name"],
                    "email":current_ride_dictionary['email'],
                    "posted_by":current_ride_dictionary["user.first_name"],
                    "date": current_ride_dictionary["date"],
                    "time": current_ride_dictionary["time"],
                    "location":current_ride_dictionary["location"],
                    "description":current_ride_dictionary["description"],
                    "skill_level":current_ride_dictionary["skill_level"],
                    "bike_type":current_ride_dictionary["bike_type"],
                    "posted_by":current_ride_dictionary["posted_by"],
                    

                }

                user_instance =user.User(new_user_dictionary)

                ride_instance.user = user_instance

                all_ride_instances.append(ride_instance)

            return all_ride_instances

# class method get all from cars
    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM rides;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_rides = []
        for row in results:
            print(row)
            all_rides.append( cls(row) )
        return all_rides  


    # class method to get one from car by id
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM rides WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    # @classmethod
    # def delete_car(cls,data):
    #     query = "DELETE FROM cars WHERE id = %(id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query,data)



    @classmethod
    def edit(cls, data):
        query = "UPDATE rides SET title=%(location)s, date=%(date)s, "\
        "time=%(time)s,skill_level=%(skill_level)s,bike_type=%(bike_type)s, description=%(description)s "\
        "WHERE rides.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    # @classmethod
    # def delete_car(cls, id):
    #     data={
    #         'id':id
    #     }
    #     query = "DELETE FROM cars WHERE id = %(id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query,id)

    @classmethod
    def delete_ride(cls,id):
        data= {
            'id':id
        }
        query = "DELETE FROM rides WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    # @classmethod
    # def delete_car(cls,data):
    #     query = "DELETE FROM cars WHERE user_id = %(user_id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod #validations
    def validate_newride(form_data):
            is_valid = True
            print(form_data)
            if len (form_data["location"]) < 3:
                is_valid =False
                flash("Please enter a valid location", "ride")
            if len (form_data ["date"]) < 1:
                is_valid =False
                flash("Date is required", "ride")
            if len (form_data ["time"]) < 1:
                is_valid =False
                flash("Start time is required", "ride")
            if len (form_data ["skill_level"]) < 1:
                is_valid =False
                flash("Skill level is required", "ride")
            if len (form_data ["bike_type"]) < 1:
                is_valid =False
                flash("Bike type is required", "ride")
                is_valid = False
            # if len (form_data["year"]) < 4:
            #     is_valid =False
                # flash("Must input a year", "car")
            if len (form_data ["description"]) < 3:
                is_valid =False
                flash("Description of ride required", "ride")
            return is_valid