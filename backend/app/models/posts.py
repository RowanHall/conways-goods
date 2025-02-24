from app import db

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True) 
    user_id = db.Column(db.Integer, nullable=True)
    available = db.Column(db.Boolean, default=True, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    price = db.Column(db.Integer, default=100, nullable=False)
    designer = db.Column(db.String(50), default='Other', nullable=True)
    category = db.Column(db.String(50), default='Other', nullable=True)
