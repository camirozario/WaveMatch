from extensions import db

class User(db.Model): # User será um modelo de dados gerenciado pelo meu objeto db
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    password_hash = db.Column(db.String(255),nullable=False)
    surf_level = db.Column(db.String(50),nullable=False)
    min_wave_height = db.Column(db.Float,nullable=True)
    max_wave_height = db.Column(db.Float, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)

class SurfSpot(db.Model):
    __tablename__= 'surf_spot'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100),nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    beach_orientation = db.Column(db.Float, nullable=True)
    surf_level = db.Column(db.String(50), nullable=False)
    wave_direction = db.Column(db.String(100))
    predominant_direction = db.Column(db.String(100))
    wave_shape = db.Column(db.String(100))
    wave_duration = db.Column(db.String(100))
    wave_speed = db.Column(db.String(100))
    break_length = db.Column(db.String(100))
    current_tendency = db.Column(db.String(100))
    
    