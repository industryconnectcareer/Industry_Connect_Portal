# models/saved_search.py
from datetime import datetime
from app import db
import json


class SavedSearch(db.Model):
    __tablename__ = "saved_searches"

    id = db.Column(db.Integer, primary_key=True)

    # User who saved the search
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    # Search filters
    query = db.Column(db.String(255), nullable=True, index=True)   # text searched
    category = db.Column(db.String(120), nullable=True, index=True)
    mode = db.Column(db.String(30), nullable=True, index=True)     # online/offline/hybrid

    # Store full filter object (future-proof for stipend, skills, etc.)
    filters_json = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -------------------------------------------------------
    # Prevent duplicate saved searches for same filter set
    # -------------------------------------------------------
    __table_args__ = (
        db.UniqueConstraint("user_id", "query", "category", "mode",
                            name="unique_saved_search"),
    )

    # -------------------------------------------------------
    # Helpers
    # -------------------------------------------------------
    def set_filters(self, filters: dict):
        """Save full filter dict as JSON."""
        self.filters_json = json.dumps(filters)

    def get_filters(self):
        """Return JSON filter dict."""
        try:
            return json.loads(self.filters_json) if self.filters_json else {}
        except:
            return {}

    # -------------------------------------------------------
    # Dictionary for API responses
    # -------------------------------------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "query": self.query,
            "category": self.category,
            "mode": self.mode,
            "filters": self.get_filters(),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }

    def __repr__(self):
        return f"<SavedSearch user:{self.user_id} query:{self.query}>"