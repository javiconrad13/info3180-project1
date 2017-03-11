from . import db

class user_profile(db.Model):
    userid = db.Column(db.String(8), primary_key=True)
    username = db.Column(db.String(25), unique = True)
    firstname = db.Column(db.String(25))
    lastname = db.Column(db.String(25))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    bio = db.Column(db.String(225))
    pro_pic = db.Column(db.String(100))
    date_created = db.Column(db.Date())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.userid)  # python 2 support
        except NameError:
            return str(self.userid)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)