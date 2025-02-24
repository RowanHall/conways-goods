from app import db  
class PostImage(db.Model):
    __tablename__ = 'post_image'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    posts_id = db.Column(db.Integer, nullable=False)
    order_num = db.Column(db.Integer, default=1, nullable=True)
    url = db.Column(db.Text, nullable=False)
    alt_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
