
from fastapi import APIRouter, Depends
from app.schemas.recommendation import RecommendationRequest
from app.services.recomendation_services import predict_destination_recommendation, get_recommendations_log
from app.api.dependencies import get_db, get_current_active_user
from app.db.models import User
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/")
def recommend_destination(
    recommendation_request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = predict_destination_recommendation(db, recommendation_request,current_user)
    return result

@router.get("/")
def get_recommendation_log(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = get_recommendations_log(db, current_user.id_user)
    return result