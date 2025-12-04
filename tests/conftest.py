import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.utils.database import Base, get_db

# 使用内存数据库进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite需要这个参数
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """创建一个新的数据库会话用于测试"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # 删除所有表
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """创建一个测试客户端，使用测试数据库会话"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    # 覆盖依赖项
    app.dependency_overrides[get_db] = override_get_db
    
    # 创建测试客户端
    with TestClient(app) as test_client:
        yield test_client
    
    # 恢复依赖项
    app.dependency_overrides.clear()
