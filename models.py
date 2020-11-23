def create_classes(db):
    class Pet(db.Model):
        __tablename__ = 'pets'

        id = db.Column(db.Integer, primary_key=True)
        year = db.Column(db.Integer)
        state= db.Column(db.String(100))
        state_po= db.Column(db.String(100))
        candidate= db.Column(db.String(100))
        party = db.Column(db.String(100))
        candidatevotes = db.Column(db.Integer)
        writein =db.Column(db.String(100))
        totalvotes =db.Column(db.Integer)
       

        def __repr__(self):
            return '<Pet %r>' % (self.name)
    return Pet


    
