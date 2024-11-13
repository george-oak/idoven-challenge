from typing import List
from fastapi import Depends, Path, HTTPException, APIRouter, status
from src.database.database_models import DBUser
from src.models.ecg_model import (
    CreateECGResponse,
    CreateEcgRequest,
    CrossingZeroResponse,
    Lead,
    EcgResponse
)
from src.oauth.oauth import current_user
from src.database.dependency import db_dependency
from src.database.ecg_repository import create_ecg_on_db, get_ecg_by_id


router = APIRouter(
    prefix="/ecg",
    responses={
        404: {"message": "ECG not found"}
    },
    tags=['ECG']
)


ecg_list = []


@router.get("/{id}")
async def get_ecg(
    db: db_dependency,
    id: int = Path(gt=0),
    user: DBUser = Depends(current_user)
) -> EcgResponse:
    if user.is_admin == 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    ecg = get_ecg_by_id(id, db)
    if not ecg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ecg does not exist"
        )
    if ecg.user_id is not user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    leads = prepare_leads(ecg.leads)
    ecg_response = EcgResponse(
        id=ecg.id,
        date=ecg.date,
        user_id=ecg.user_id,
        leads=leads
    )
    return ecg_response


@router.get("/leads_crossing_zero/{id}")
async def get_crossing_zero_signals(
    db: db_dependency,
    id: int,
    user: DBUser = Depends(current_user)
) -> List[CrossingZeroResponse]:
    if user.is_admin == 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    ecg = get_ecg_by_id(id, db)
    if not ecg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ecg does not exist"
        )
    if ecg.user_id is not user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    leads = prepare_leads(ecg.leads)
    response = []
    for lead in leads:
        signals_crossing_zero = list(filter(crossing_zero, lead.signal))
        response.append(
            CrossingZeroResponse(
                name=lead.name,
                signals_crossing_zero=len(signals_crossing_zero)
            ).model_dump()
        )
    return response


@router.post("/", status_code=201)
async def post_ecg(
    ecg_request: CreateEcgRequest,
    db: db_dependency,
    user: DBUser = Depends(current_user)
) -> CreateECGResponse:
    if user.is_admin == 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    ecg = create_ecg_on_db(ecg_request, user.id, db)
    return CreateECGResponse(id=ecg.id)


def crossing_zero(lead: int) -> bool:
    if lead == 0:
        return False
    return True


def prepare_leads(leads: list) -> List[Lead]:
    leads_formatted = []
    for lead in leads:
        lead_response = Lead(
            name=lead.name,
            samples=lead.samples,
            signal=list(map(int, lead.signal.split(',')))
        )
        leads_formatted.append(lead_response)
    return leads_formatted
