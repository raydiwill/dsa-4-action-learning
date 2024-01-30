from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.sql import func
from typing import Any
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    id: Any
    __name__: str


class CustomerModel(Base):
    __tablename__ = 'customers_model'

    pred_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    REGION = Column(String)
    TENURE = Column(String)
    MONTANT = Column(Float)
    FREQUENCE_RECH = Column(Float)
    REVENUE = Column(Float)
    ARPU_SEGMENT = Column(Float)
    FREQUENCE = Column(Float)
    DATA_VOLUME = Column(Float)
    ON_NET = Column(Float)
    ORANGE = Column(Float)
    TIGO = Column(Float)
    REGULARITY = Column(Float)
    TOP_PACK = Column(String)
    FREQ_TOP_PACK = Column(Float)
    pred_probability = Column(Float)
    pred_churn = Column(Integer)
    pred_risk = Column(String)
    pred_date = Column(DateTime, server_default=func.now())


class ProblemStats(Base):
    __tablename__ = 'data_problem_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String)
    column = Column(String)
    expectation_type = Column(String)
    unexpected_values = Column(String)
    error_time_found = Column(DateTime, server_default=func.now())


class CustomerReport(Base):
    __tablename__ = 'customers_report'

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    model_pred = Column(Integer)
    actual = Column(Integer)
    pred_risk = Column(String)
    strategy = Column(String)
    resolve = Column(String)
