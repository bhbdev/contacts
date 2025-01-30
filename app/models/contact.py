from datetime import datetime
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from app import db

PER_PAGE = 10


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True, default='')
    address = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    #avatar = db.Column(db.String(200), nullable=True)
    
    errors: dict = {}
    
    def __repr__(self):
        return f'<Contact {self.name}>'
    
    def validate(self) -> bool:
        self.errors = {}
        if not self.name:
            self.errors['name'] = 'Name is required'

         # check if email is not a duplicate
        if not self.email:
            self.errors['email'] = 'Email is required'

        # check if phone is valid and not a duplicate  
        if not self.phone:
            self.errors['phone'] = 'Phone is required'
        # only digits, spaces, and dashes are allowed max length 20
        if self.phone and isinstance(self.phone, str) and (not all(c.isdigit() or c in ' -' for c in self.phone) or len(self.phone) > 20):
            self.errors['phone'] = 'Invalid phone number'
        

        return len(self.errors) == 0
    
    def save(self) -> bool:
        if not self.validate():
            return False
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if 'email' in str(e.orig):
                self.errors['email'] = 'Email is already in use'
            elif 'phone' in str(e.orig):
                self.errors['phone'] = 'Phone is already in use'
            else:
                self.errors['database'] = 'Database error'
            print(e)
            return False    
        return True
    
    @classmethod
    def count(cls) -> int:
        return db.session.query(db.func.count(cls.id)).scalar()
    
    @classmethod
    def all(cls, page: int = 1) -> list:
        start: int = (page - 1) * PER_PAGE
        end: int = start + PER_PAGE
        query = db.select(cls).order_by(cls.updated_at.desc())
        rs = db.session.execute(query).scalars().all()
        return list(rs)[start:end]
    
    @classmethod
    def search(self, search: str) -> list:
        query = db.select(Contact).filter(
            db.or_(
                Contact.name.ilike(f'%{search}%'),
                Contact.email.ilike(f'%{search}%')
            )
        )
        rs = db.session.execute(query).scalars().all()
        return list(rs)[:PER_PAGE]
    

@event.listens_for(Contact, 'before_insert')
@event.listens_for(Contact, 'before_update')
def update_timestamps(mapper, connection, target):
    target.updated_at = datetime.now()
    if not target.created_at:
        target.created_at = datetime.now()