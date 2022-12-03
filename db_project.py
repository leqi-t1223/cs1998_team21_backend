from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here
association_table = db.Table("association",
                             db.Column("location_id", db.Integer,
                                       db.ForeignKey("location.id")),
                             db.Column("user_id", db.Integer,
                                       db.ForeignKey("user.id"))
                             )


class Location(db.Model):
    """
    Location model has a many to many relationship with user model
    """
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    x_coordinate = db.Column(db.Float, nullable=False)
    y_coordinate = db.Column(db.Float, nullable=False)
    name = db.Column(db.String, nullable=False)
    vendors = db.relationship("Vendor", cascade="delete")
    users = db.relationship(
        "User", secondary=association_table, back_populates='locations')

    def __init__(self, **kwargs):
        """
        Creates a course project
        """
        self.x_coordinate = kwargs.get("x_coordinate")
        self.y_coordinate = kwargs.get("y_coordinate")
        self.name = kwargs.get("name")

    def serialize(self):
        """
        Serializes a Location object
        """
        return {
            "id": self.id,
            "x_coordinate": self.x_coordinate,
            "y_coordinate": self.y_coordinate,
            "name": self.name,
            "users": [u.simple_serialize() for u in self.users],
            "vendors": [a.simple_serialize() for a in self.vendors],
        }

    def simple_serialize(self):
        """
          Serializes a Location object
        """
        return {
            "id": self.id,
            "name": self.name,
        }


class Vendor(db.Model):
    __tablename__ = "vendor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position = db.Column(db.String, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey(
        "location.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        creates a vendor project
        """
        self.position = kwargs.get("position")
        self.location_id = kwargs.get("location_id")

    def simple_serialize(self):
        return {
            "id": self.id,
            "position": self.position,
        }


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    locations = db.relationship(
        "Location", secondary=association_table, back_populates='users')

    def __init__(self, **kwargs):
        """
        creates a user project
        """
        self.name = kwargs.get("name", "")
        self.email = kwargs.get("email", "")

    def recent_location(self):
        if self.locations == []:
            return []
        else:
            return self.locations[-1].simple_serialize

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "location": self.recent_location()
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
