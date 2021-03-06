from app import db
from app.models.dict_serializable import DictSerializable
from datetime import datetime


# Rescan Queue
# Each record represents a user-requested rescan of a given target.
# Tracks when it was dispatched, when it was completed, and the scan id of the complete scan.
class RescanTask(db.Model, DictSerializable):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(
        db.DateTime, index=True, default=datetime.utcnow, nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    target = db.Column(db.String(128), index=True, nullable=False)
    dispatched = db.Column(db.Boolean, default=False, index=True)
    date_dispatched = db.Column(db.DateTime, index=True)
    complete = db.Column(db.Boolean, default=False, index=True)
    date_completed = db.Column(db.DateTime, index=True)
    scan_id = db.Column(db.String(256), index=True, unique=True)

    def dispatchTask(self):
        self.dispatched = True
        self.date_dispatched = datetime.utcnow()

    def completeTask(self, scan_id):
        self.scan_id = scan_id
        self.complete = True
        self.date_completed = datetime.utcnow()

    @staticmethod
    def getPendingTasks():
        # Tasks that haven't been completed and haven't been dispatched
        return (
            RescanTask.query.filter_by(complete=False).filter_by(dispatched=False).all()
        )

    @staticmethod
    def getDispatchedTasks():
        # Tasks that have been dispatched but haven't been completed
        return (
            RescanTask.query.filter_by(dispatched=True).filter_by(complete=False).all()
        )

    @staticmethod
    def getIncompleteTasks():
        # All tasks that haven't been marked as complete
        return RescanTask.query.filter_by(complete=False).all()

    @staticmethod
    def getIncompleteTaskForTarget(ip):
        return RescanTask.query.filter_by(target=ip).filter_by(complete=False).all()
