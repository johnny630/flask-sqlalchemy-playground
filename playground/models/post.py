from datetime import datetime
from .. import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title

# Single table
## select
# Post.query.count()
# Post.query.get(1)                         get by id
# Post.query.limit(2).all()                 Limiting
# Post.query.order_by(Post.title).all()     Ordering
# Post.query.filter_by(title='title1').first()   where
#
## update
# 

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


# category = Category(name='test')
# post = Post(title='Hello Python!', body='Python is pretty cool', category=category)
# db.session.add(post)
# db.session.commit()

# from flask_sqlalchemy import get_debug_queries
# for query in get_debug_queries():
#     print(query.statement)
#     print(query.parameters)
#     print(query.duration)
#     print(query.context)