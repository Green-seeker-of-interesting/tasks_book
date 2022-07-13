from app import db


class task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    def get_value_task(self):
        out = {
            "title" : self.title,
            "content" : self.content
        }
        return out

    def __repr__(self):
	    return str(self.get_value_task())
