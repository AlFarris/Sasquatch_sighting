from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Sighting:
    db= "users_schema"
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.number = data['number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def validate_sighting(sighting):
        is_valid = True 
        if len(sighting['location']) < 3:
            flash("All fields required.")
            is_valid = False
        if len(sighting['description']) < 3:
            flash("All fields required.")
            is_valid = False
        if len(sighting['number']) < 1:
            flash("At least 1 Sasquatch.")
            is_valid = False
        if len(sighting['date']) < 1:
            flash("All fields required.")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results= connectToMySQL(cls.db).query_db(query)
        all_sightings=[]
        for row in results:
            all_sightings.append(cls(row))
        return all_sightings

    @classmethod
    def create(cls, data):
        query = "INSERT INTO sightings (location, description, date, number, user_id) VALUES (%(location)s, %(description)s, %(date)s, %(number)s, %(user_id)s);"
        results= connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def get_all_by_id(cls,data):
        query = "SELECT * FROM sightings WHERE id= %(id)s;"
        results= connectToMySQL(cls.db).query_db(query,data)
        one_sighting=cls(results[0])
        return one_sighting

    @classmethod
    def update_sighting(cls, data):
        query = "UPDATE sightings SET location=%(location)s, description=%(description)s, date=%(date)s, number=%(number)s WHERE id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return results
    
    @classmethod
    def delete_sighting(cls,id):
        query = "DELETE FROM sightings WHERE id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,id)
        return results