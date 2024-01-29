from pydantic import BaseModel
from typing import Optional


class CustomerData(BaseModel):
    user_id: str
    REGION: Optional[str] = None
    TENURE: Optional[str] = None
    MONTANT: Optional[float] = None
    FREQUENCE_RECH: Optional[float] = None
    REVENUE: Optional[float] = None
    ARPU_SEGMENT: Optional[float] = None
    FREQUENCE: Optional[float] = None
    DATA_VOLUME: Optional[float] = None
    ON_NET: Optional[float] = None
    ORANGE: Optional[float] = None
    TIGO: Optional[float] = None
    REGULARITY: Optional[int] = None
    TOP_PACK: Optional[str] = None
    FREQ_TOP_PACK: Optional[float] = None
