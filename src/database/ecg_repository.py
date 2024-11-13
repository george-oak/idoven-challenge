from sqlalchemy.orm import Session
from src.database.database_models import DBEcg, DBLead
from src.models.ecg_model import CreateEcgRequest
from datetime import datetime


def get_ecg_by_id(id: int, db: Session) -> DBEcg | None:
    return db.query(DBEcg).filter(DBEcg.id == id).first()


def create_ecg_on_db(
    ecg_request: CreateEcgRequest,
    user_id: int,
    db: Session
) -> DBEcg:
    leads = []
    delimiter = ","
    for lead in ecg_request.leads:
        lead_to_insert = DBLead(
            name=lead.name,
            samples=lead.samples,
            signal=delimiter.join(map(str, lead.signal))
        )
        leads.append(lead_to_insert)
    ecg = DBEcg(
        date=datetime.now(),
        user_id=user_id,
        leads=leads
    )
    db.add(ecg)
    db.commit()
    db.refresh(ecg)
    return ecg
