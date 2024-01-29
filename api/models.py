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

    id = Column(Integer, primary_key=True)


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
