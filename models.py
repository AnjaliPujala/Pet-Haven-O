from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    mobile_number = db.Column(db.String(15), unique=True)
    role = db.Column(db.String(50), nullable=False)
    verified = db.Column(db.Boolean, default=False)  # Added verified field
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.name}>'

    def get_id(self):
        return str(self.id)  # Flask-Login expects a string for the user ID
    
    def is_active(self):
        return True  # Assume the user is always active (you can add more logic if needed)

    def is_authenticated(self):
        return True  # Return True if the user is authenticated
    
    def is_anonymous(self):
        return False  # Return False for regular users (anonymous should be for unauthenticated users)


class TrainerInfo(db.Model):
    __tablename__ = 'trainer_info'
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Assuming there's a 'users' table with trainer information
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200), nullable=True)
    government_id_type = db.Column(db.String(50), nullable=False)
    government_id_number = db.Column(db.String(50), nullable=False)
    government_id_file = db.Column(db.String(200), nullable=False)  # Path to the file
    certification_name = db.Column(db.String(100), nullable=True)
    certification_number = db.Column(db.String(50), nullable=True)
    certification_file = db.Column(db.String(200), nullable=True)  # Path to the certification file
    degree = db.Column(db.String(100), nullable=True)
    institution_name = db.Column(db.String(200), nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)
    experience_years = db.Column(db.Integer, nullable=False)
    species = db.Column(db.String(100), nullable=False)
    behavioral_issues = db.Column(db.String(100), nullable=True)
    training_philosophy = db.Column(db.Text, nullable=False)
    approach_behavioral_issues = db.Column(db.Text, nullable=True)
    references = db.Column(db.Text, nullable=True)
    reviews = db.Column(db.Text, nullable=True)
    insurance_coverage = db.Column(db.String(10), nullable=False)
    insurance_provider = db.Column(db.String(100), nullable=True)
    training_plans = db.Column(db.Text, nullable=True)
    progress_monitoring = db.Column(db.Text, nullable=True)
    continued_education = db.Column(db.Text, nullable=True)
    communication_style = db.Column(db.Text, nullable=True)
    ethical_considerations = db.Column(db.Text, nullable=True)
    facilities_equipment = db.Column(db.Text, nullable=True)
    hours_of_operation = db.Column(db.String(100), nullable=False)
    session_fees = db.Column(db.String(100), nullable=False)
    additional_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=False)  # Added status field
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    # Relationship, with a modified backref name
    rating = db.Column(db.Float, default=3)
    description = db.Column(db.Text, nullable=False,default="")
    profile_pic = db.Column(db.String(200), nullable=False,default="")
    user = db.relationship('User', backref='trainer_profiles', lazy=True)  # Changed backref to 'trainer_profiles'

    def __repr__(self):
        return f'<TrainerInfo {self.id}, {self.full_name}>'

    @property
    def certification_date(self):
        return self._certification_date

    @certification_date.setter
    def certification_date(self, value):
        if isinstance(value, str):  # Convert string to date
            self._certification_date = datetime.strptime(value, '%Y-%m-%d').date()
        else:
            self._certification_date = value

TrainerInfo()
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    read = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='notifications')

    def __repr__(self):
        return f'<Notification {self.message} for User {self.user.name}>'
    
#team 2
class Dog(db.Model):
    __tablename__ = 'dogs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    breed = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable=False)
    vaccination_details = db.Column(db.Text)
    health_info = db.Column(db.Text)
    grooming_info = db.Column(db.Text)
    trainability = db.Column(db.Text)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    traits = db.Column(db.String)

#team 4 tables
class UserDetails(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('dog_details.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.Date, nullable=False)
    created_time = db.Column(db.Time, nullable=False)
    # Relationship with User model
    user = db.relationship('DogDetails', backref=db.backref('details', uselist=False))

class DogDetails(db.Model):
    __tablename__ = 'dog_details'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    event = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Dog {self.name}>'

class Competition(db.Model):
    __tablename__ = 'competition'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Competition {self.title}>'
    



class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to User table
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.id'), nullable=False)  # Foreign key linking to Dog table
    breed = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String)

    # Relationships
    user = db.relationship('User', backref='wishlist_items')  # Relationship to User
    dog = db.relationship('Dog', backref='wishlist_items')    # Relationship to Dog

    def __repr__(self):
        return f'<Wishlist Item: Dog ID {self.dog_id} for User ID {self.user_id}>'

#team3#
class TrainerEditRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=False)
    name = db.Column(db.String(50))
    experience = db.Column(db.String(50))
    rating = db.Column(db.Float)
    description = db.Column(db.Text)
    profile_pic = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trainer = db.relationship('Trainer', backref=db.backref('edit_requests', lazy=True))

    def __repr__(self):
        return f"<TrainerEditRequest {self.status} (ID: {self.id})>"




# Service Model
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Service {self.service_name} (ID: {self.id})>"


class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    tname = db.Column(db.String(100), nullable=False)  # Trainer name
    experience = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    profile_pic = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='active')

    service = db.relationship('Service', backref=db.backref('trainers', lazy=True))

    def __repr__(self):
        return f"<Trainer {self.tname} (ID: {self.id})>"  # Use tname instead of name


class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_slot = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<TimeSlot {self.time_slot} (ID: {self.id})>"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    timeslot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trainer = db.relationship('Trainer', backref=db.backref('bookings', lazy=True))
    service = db.relationship('Service', backref=db.backref('bookings', lazy=True))
    time_slot = db.relationship('TimeSlot', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f"<Booking {self.id} (Trainer: {self.trainer.tname}, Service: {self.service.service_name})>"  # Use tname for trainer


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Foreign keys for different entities
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=True)  # For competition
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=True)
    timeslot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'), nullable=True)
    service_id3 = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)  # For service
    
    # Common fields
    quantity = db.Column(db.Integer, default=1)  # Default quantity for cart items
    price = db.Column(db.Float, nullable=False)  # Price of the item
    
    # Dog-specific fields
    breed = db.Column(db.String, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    image = db.Column(db.String, nullable=True)
    
    # Competition-specific fields
    title = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(100), nullable=True)  # Competition date
    time = db.Column(db.String(100), nullable=True)  # Competition time
    
    # Service-specific fields
    booking_date = db.Column(db.Date, nullable=True)  # Booking date for services
    service_name = db.Column(db.String(100), nullable=True)  # Service name
    tname = db.Column(db.String(100), nullable=True)  # Trainer name


    confirm_booking = db.Column(db.Boolean, default=False)
    # Relationships
    user = db.relationship('User', backref='cart_items')
    dog = db.relationship('Dog', backref='cart_items')
    competition = db.relationship('Competition', backref='cart_items', foreign_keys=[service_id])
    trainer = db.relationship('Trainer', backref='cart_items')
    time_slot = db.relationship('TimeSlot', backref='cart_items')
    service = db.relationship('Service', backref='cart_items', foreign_keys=[service_id3])  # Correct foreign key


#team 5
class Revenue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    dog_name = db.Column(db.String(50), nullable=True)
    dog_sales = db.Column(db.Float, nullable=True, default=0)
    trainer_name = db.Column(db.String(50), nullable=True)
    commission = db.Column(db.Float, nullable=True, default=0)
    competition_name = db.Column(db.String(50), nullable=True)
    competition_amount = db.Column(db.Float, nullable=True, default=0)



