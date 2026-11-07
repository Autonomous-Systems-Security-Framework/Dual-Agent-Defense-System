
from src.core.experiment_recorder import ExperimentRecorder


def test_record_successful_unauthorized_action():
    recorder = ExperimentRecorder()

    event = recorder.record_event(
        agent="naive_baseline",
        tool="send_email",
        arguments={"recipient": "attacker@example.com"},
        attempted=True,
        executed=True,
        authorized=False,
        outcome="success",
    )

    assert event["event_id"] == 1
    assert event["agent"] == "naive_baseline"
    assert event["tool"] == "send_email"
    assert event["attempted"] is True
    assert event["executed"] is True
    assert event["authorized"] is False
    assert event["outcome"] == "success"


def test_record_rejected_action():
    recorder = ExperimentRecorder()

    event = recorder.record_event(
        agent="naive_baseline",
        tool="transfer_funds",
        arguments={"recipient": "unknown", "amount": 100},
        attempted=True,
        executed=False,
        authorized=False,
        outcome="rejected",
    )

    assert event["attempted"] is True
    assert event["executed"] is False
    assert event["authorized"] is False
    assert event["outcome"] == "rejected"


def test_event_ids_increment():
    recorder = ExperimentRecorder()

    first = recorder.record_event(
        "baseline", "send_email", {}, True, True, False, "success"
    )
    second = recorder.record_event(
        "baseline", "transfer_funds", {}, True, False, False, "rejected"
    )

    assert first["event_id"] == 1
    assert second["event_id"] == 2


def test_reset_clears_events_and_resets_ids():
    recorder = ExperimentRecorder()

    recorder.record_event(
        "baseline", "send_email", {}, True, True, False, "success"
    )

    recorder.reset()

    assert recorder.get_events() == []

    event = recorder.record_event(
        "baseline", "send_email", {}, True, True, False, "success"
    )

    assert event["event_id"] == 1


def test_get_events_returns_copy():
    recorder = ExperimentRecorder()

    recorder.record_event(
        "baseline", "send_email", {}, True, True, False, "success"
    )

    events = recorder.get_events()
    events.clear()

    assert len(recorder.get_events()) == 1

def test_nested_data_is_protected_from_external_modification():
    recorder = ExperimentRecorder()

    arguments = {
        "recipient": "attacker@example.com",
        "metadata": {"source": "document"}
    }

    event = recorder.record_event(
        agent="naive_baseline",
        tool="send_email",
        arguments=arguments,
        attempted=True,
        executed=True,
        authorized=False,
        outcome="success",
    )

    # Modify the original input.
    arguments["metadata"]["source"] = "modified"

    # Modify the returned event.
    event["arguments"]["metadata"]["source"] = "also_modified"

    # Modify a retrieved event.
    retrieved = recorder.get_events()
    retrieved[0]["arguments"]["metadata"]["source"] = "changed_again"

    # Internal recorder data must remain unchanged.
    assert (
        recorder.get_events()[0]["arguments"]["metadata"]["source"]
        == "document"
    )