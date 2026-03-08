import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base
from app.database.models_intents import IntentDB, OutcomeDB
from app.services.outcome_service import record_outcome, OutcomeConflictError
from unittest.mock import MagicMock
import datetime

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(bind=engine, future=True)
    Base.metadata.create_all(bind=engine)
    sess = TestingSessionLocal()
    yield sess
    sess.close()

@pytest.fixture
def mock_risk_engine():
    engine = MagicMock()
    engine.update_outcome = MagicMock()
    return engine

def test_record_outcome_creates_row_and_updates_engine(db_session, mock_risk_engine):
    intent = IntentDB(
        deterministic_id="intent_abc",
        intent_type="ProvisionResourceIntent",
        payload={},
        oss_payload={"intent_type": "provision_resource"},
        created_at=datetime.datetime.utcnow()
    )
    db_session.add(intent)
    db_session.commit()
    db_session.refresh(intent)

    outcome = record_outcome(
        db=db_session,
        deterministic_id="intent_abc",
        success=True,
        recorded_by="tester",
        notes="works",
        risk_engine=mock_risk_engine
    )
    assert outcome.success is True
    assert outcome.recorded_by == "tester"
    mock_risk_engine.update_outcome.assert_called_once()

    outcome2 = record_outcome(
        db=db_session,
        deterministic_id="intent_abc",
        success=True,
        recorded_by="tester",
        notes="again",
        risk_engine=mock_risk_engine
    )
    assert outcome2.id == outcome.id
    mock_risk_engine.update_outcome.assert_called_once()

def test_conflict_different_result(db_session, mock_risk_engine):
    intent = IntentDB(
        deterministic_id="intent_def",
        intent_type="ProvisionResourceIntent",
        payload={},
        created_at=datetime.datetime.utcnow()
    )
    db_session.add(intent)
    db_session.commit()

    record_outcome(db_session, "intent_def", True, None, None, mock_risk_engine)
    with pytest.raises(OutcomeConflictError):
        record_outcome(db_session, "intent_def", False, None, None, mock_risk_engine)

def test_nonexistent_intent(db_session, mock_risk_engine):
    with pytest.raises(ValueError):
        record_outcome(db_session, "missing", True, None, None, mock_risk_engine)
