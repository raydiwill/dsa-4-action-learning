from pydantic import BaseModel


class CustomerData(BaseModel):
    id: str
    region: str
    tenure: str
    amount: float
    frequence_rech: float
    revenue: float
    arpu_segment: float
    frequence: float
    data_volume: float
    on_net: float
    orange: float
    tigo: float
    regularity: int
    top_pack: str
    freq_top_pack: float
