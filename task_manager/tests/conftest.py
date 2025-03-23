import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, SQLALCHEMY_DATABASE_URL
from app.main import app
from fastapi.testclient import TestClient

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 创建测试会话工厂
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 夹具：数据库会话
@pytest.fixture(scope="function")
def db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    # 创建新的数据库会话
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # 关闭会话并删除所有表
        db.close()
        Base.metadata.drop_all(bind=engine)


# 夹具：FastAPI 测试客户端
@pytest.fixture(scope="function")
def client():
    # 使用 TestClient 包装 FastAPI 应用
    with TestClient(app) as client:
        yield client
