from fastapi import APIRouter,Depends
from sqlalchemy import select
from .database import session
from .auth import current,editor,admin
from .review_models import ScreenReview
from .review_schemas import ReviewInput,DecisionInput
from . import review_service
router=APIRouter()
@router.get('/screen-reviews')
def reviews(user=Depends(current),db=Depends(session)):return db.scalars(select(ScreenReview).order_by(ScreenReview.id.desc())).all()
@router.post('/screen-reviews')
def request(body:ReviewInput,user=Depends(editor),db=Depends(session)):return review_service.request(db,body,user)
@router.post('/screen-reviews/{key}/decision')
def decide(key:int,body:DecisionInput,user=Depends(admin),db=Depends(session)):return review_service.decide(db,key,body,user)
