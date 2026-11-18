from datetime import datetime
from sqlalchemy import String,Float,Boolean,ForeignKey,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column
from .database import Base
class ScreenReview(Base):
    __tablename__='screen_reviews'
    id:Mapped[int]=mapped_column(primary_key=True)
    visit_id:Mapped[int]=mapped_column(ForeignKey('visits.id'),unique=True)
    reason:Mapped[str]=mapped_column(String(400))
    requested_by:Mapped[str]=mapped_column(String(120))
    requested_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now())
    original_score:Mapped[float]=mapped_column(Float)
    original_flag:Mapped[bool]=mapped_column(Boolean)
    original_threshold:Mapped[float|None]=mapped_column(Float,nullable=True)
    state:Mapped[str]=mapped_column(String(24),default='pending')
    superseded:Mapped[bool]=mapped_column(Boolean,default=False)
    decided_by:Mapped[str]=mapped_column(String(120),default='')
    decision_note:Mapped[str]=mapped_column(String(400),default='')
    decided_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
