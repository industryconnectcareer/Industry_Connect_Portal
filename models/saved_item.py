# models/saved_item.py
from datetime import datetime
from app import db


class SavedItem(db.Model):
    __tablename__ = "saved_items"

    id = db.Column(db.Integer, primary_key=True)

    # User who saved the item
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    # Supports internships + OJT
    item_type = db.Column(db.String(50), nullable=False, index=True)   # "internship" | "ojt"
    item_id = db.Column(db.Integer, nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # --------------------------------------------------------
    # Prevent duplicates → (user_id, item_type, item_id)
    # --------------------------------------------------------
    __table_args__ = (
        db.UniqueConstraint("user_id", "item_type", "item_id",
                            name="unique_saved_item"),
    )

    # --------------------------------------------------------
    # RELATIONSHIPS (Lazy Load Target Models)
    # --------------------------------------------------------
    @property
    def internship(self):
        """Return internship object if type is internship."""
        if self.item_type == "internship":
            from models.internship import Internship
            return Internship.query.get(self.item_id)
        return None

    @property
    def ojt(self):
        """Return OJT object if type is ojt."""
        if self.item_type == "ojt":
            from models.ojt import OJT
            return OJT.query.get(self.item_id)
        return None

    # --------------------------------------------------------
    # HELPERS
    # --------------------------------------------------------
    def is_internship(self):
        return self.item_type == "internship"

    def is_ojt(self):
        return self.item_type == "ojt"

    def get_item(self):
        """Returns the actual object (internship / ojt)."""
        return self.internship if self.is_internship() else self.ojt

    # --------------------------------------------------------
    # API DICTIONARY
    # --------------------------------------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "item_type": self.item_type,
            "item_id": self.item_id,
            "created_at": self.created_at.strftime("%Y-%m-%d"),
        }

    def __repr__(self):
        return f"<SavedItem user:{self.user_id} {self.item_type}:{self.item_id}>"