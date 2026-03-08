import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base
from app.database.models_intents import IntentDB
from app.services.intent_store import save_evaluated_intent, get_intent_by_deterministic_id
import datetime

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(bind=engine, future=True)
    Base.metadata.create_all(bind=engine)
    sess = TestingSessionLocal()
    yield sess
    sess.close()

def test_save_intent(db_session):
    det_id = "intent_123"
    saved = save_evaluated_intent(
        db=db_session,
        deterministic_id=det_id,
        intent_type="ProvisionResourceIntent",
        api_payload={"foo": "bar"},
        oss_payload={"intent_type": "provision_resource"},
        environment="prod",
        risk_score=0.42
    )
    assert saved.deterministic_id == det_id
    assert saved.risk_score == "0.42"

    fetched = get_intent_by_deterministic_id(db_session, det_id)
    assert fetched is not None
    assert fetched.payload["foo"] == "bar"

def test_update_existing_intent(db_session):
    det_id = "intent_123"
    save_evaluated_intent(db_session, det_id, "Type", {}, {}, "prod", 0.5)
    updated = save_evaluated_intent(db_session, det_id, "Type", {}, {}, "prod", 0.7)
    assert updated.risk_score == "0.7"
    count = db_session.query(IntentDB).filter(IntentDB.deterministic_id == det_id).count()
    assert count == 1
