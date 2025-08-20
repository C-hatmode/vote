from database.connection import admins_collection

class AdminModel:
    @staticmethod
    def create_admin(data):
        admins_collection.insert_one(data)
        return True

    @staticmethod
    def find_by_email(email):
        return admins_collection.find_one({"email": email})
