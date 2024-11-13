from typing import Optional, List
from pydantic import BaseModel, Field, PastDatetime


class Lead(BaseModel):
    name: str = Field(min_length=1, max_length=3)
    samples: Optional[int] = None
    signal: list[int]

    model_config = {
        'json_schema_extra': {
            'example': {
                'name': 'III',
                'samples': 4,
                'signal': [0, 3, 0, -3]
            }
        }
    }


class EcgResponse(BaseModel):
    id: int = Field(gt=0)
    date: PastDatetime
    user_id: int = Field(gt=0)
    leads: List[Lead]


class CreateEcgRequest(BaseModel):
    leads: List[Lead]


class CrossingZeroResponse(BaseModel):
    name: str
    signals_crossing_zero: int

    model_config = {
        'json_schema_extra': {
            'example': {
                'name': 'III',
                'signals_crossing_zero': 2
            }
        }
    }


class CreateECGResponse(BaseModel):
    id: int

    model_config = {
        'json_schema_extra': {
            'example': {
                'id': '1'
            }
        }
    }
