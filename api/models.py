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

    user_id = Column(String, primary_key=True)
    region = Column(String)
    tenure = Column(String)
    amount = Column(Float)
    frequence_rech = Column(Float)
    revenue = Column(Float)
    arpu_segment = Column(Float)
    frequence = Column(Float)
    data_volume = Column(Float)
    on_net = Column(Float)
    orange = Column(Float)
    tigo = Column(Float)
    regularity = Column(Float)
    top_pack = Column(String)
    freq_top_pack = Column(Float)
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
    user_id = Column(String, primary_key=True)
    model_pred = Column(Integer)
    actual = Column(Integer)
    pred_risk = Column(String)
    strategy = Column(String)
    resolve = Column(String)
