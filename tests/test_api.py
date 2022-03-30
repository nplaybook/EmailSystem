import pytest
from json import loads

class TestGetEvent:


    def test_get_event_success(self, server):
        result = server.get("/event")
        result_data = loads(result.data)
        assert result.status_code == 200
        assert set(result_data) == {"result", "message", "data"}
        assert type(result_data["message"]) == str
        assert "success" in result_data["message"]
        assert type(result_data["data"]) == list


class TestPostSavesEmail:

    @pytest.mark.parametrize("event_id, email_subject, email_content, from_email, to_email, timestamp, output", [
        (1, "Test Subject", "Test Content", "sender@example.com", ["recipient@example.com"], "2016-09-08 00:00:00", 201),
        (1, "A", "Test Content", "sender@example.com", ["recipient@example.com"], "2016-09-08 00:00:00", 201),
        (1, "Test Subject", "A", "sender@example.com", ["recipient@example.com"], "2016-09-08 00:00:00", 201),
        (1, "A", "A", "sender@example.com", ["recipient@example.com"], "2016-09-08 00:00:00", 201),
        (1, "Test Subject", "Test Content", "sender@example.com", ["recipient@example.com", "recipient2@example.com"], "2016-09-08 00:00:00", 201),
    ])
    def test_success(self, server, event_id, email_subject, email_content, from_email, to_email, timestamp, output):
        payload: dict = {
            "event_id": event_id,
            "email_subject": email_subject,
            "email_content": email_content,
            "from_email": from_email,
            "to_email": to_email,
            "timestamp": timestamp
            }
        result = server.post("/save_emails", json=payload, content_type="application/json")
        result_data = loads(result.data)
        assert result.status_code == output
        assert set(result_data) == {"result", "message", "data"}
        assert type(result_data["message"]) == str
        assert result_data["message"] == "Request success"
        assert type(result_data["data"]) == list


    @pytest.mark.parametrize("event_id, email_subject, email_content, from_email, to_email, timestamp, output", [
        (1, "", "Test Content", "sender@example.com", ["recipient@example.com"], "2016-09-08 00:00:00", 400)
    ])
    def test_fail_empty_subject(self, server, event_id, email_subject, email_content, from_email, to_email, timestamp, output):
        payload: dict = {
            "event_id": event_id,
            "email_subject": email_subject,
            "email_content": email_content,
            "from_email": from_email,
            "to_email": to_email,
            "timestamp": timestamp
            }
        result = server.post("/save_emails", json=payload, content_type="application/json")
        result_data = loads(result.data)
        assert result.status_code == output
        assert set(result_data) == {"result", "message", "err", "data"}
        assert type(result_data["message"]) == str
        assert result_data["message"] == "Validation error"
        assert result_data["err"] is not "" or []
        assert type(result_data["data"]) == list
        assert result_data["data"] == []


    @pytest.mark.parametrize("event_id, email_subject, email_content, from_email, to_email, timestamp, output", [
        (1, "Test Subject", "", "sender@example.com", ["recipient@example.com"], "2016-09-08 00:00:00", 400),
    ])
    def test_fail_empty_content(self, server, event_id, email_subject, email_content, from_email, to_email, timestamp, output):
        payload: dict = {
            "event_id": event_id,
            "email_subject": email_subject,
            "email_content": email_content,
            "from_email": from_email,
            "to_email": to_email,
            "timestamp": timestamp
            }
        result = server.post("/save_emails", json=payload, content_type="application/json")
        result_data = loads(result.data)
        assert result.status_code == output
        assert set(result_data) == {"result", "message", "err", "data"}
        assert type(result_data["message"]) == str
        assert result_data["message"] == "Validation error"
        assert result_data["err"] is not "" or []
        assert type(result_data["data"]) == list
        assert result_data["data"] == []


    @pytest.mark.parametrize("event_id, email_subject, email_content, from_email, to_email, timestamp, output", [
        (1, "Test Subject", "Test Content", "sender", ["recipient@example.com"], "2016-09-08 00:00:00", 400),
        (1, "Test Subject", "Test Content", "", ["recipient@example.com"], "2016-09-08 00:00:00", 400),
        (1, "Test Subject", "Test Content", 1, ["recipient@example.com"], "2016-09-08 00:00:00", 400),
    ])
    def test_fail_wrong_sender_data(self, server, event_id, email_subject, email_content, from_email, to_email, timestamp, output):
        payload: dict = {
            "event_id": event_id,
            "email_subject": email_subject,
            "email_content": email_content,
            "from_email": from_email,
            "to_email": to_email,
            "timestamp": timestamp
            }
        result = server.post("/save_emails", json=payload, content_type="application/json")
        result_data = loads(result.data)
        assert result.status_code == output
        assert set(result_data) == {"result", "message", "err", "data"}
        assert type(result_data["message"]) == str
        assert result_data["message"] == "Validation error"
        assert result_data["err"] is not "" or []
        assert type(result_data["data"]) == list
        assert result_data["data"] == []


    @pytest.mark.parametrize("event_id, email_subject, email_content, from_email, to_email, timestamp, output", [
        (1, "Test Subject", "Test Content", "sender@example.com", "recipient@example.com", "2016-09-08 00:00:00", 400),
        (1, "Test Subject", "Test Content", "sender@example.com", "recipient@example.com, recipient2@example.com", "2016-09-08 00:00:00", 400),
    ])
    def test_fail_recipient_not_list(self, server, event_id, email_subject, email_content, from_email, to_email, timestamp, output):
        payload: dict = {
            "event_id": event_id,
            "email_subject": email_subject,
            "email_content": email_content,
            "from_email": from_email,
            "to_email": to_email,
            "timestamp": timestamp
            }
        result = server.post("/save_emails", json=payload, content_type="application/json")
        result_data = loads(result.data)
        assert result.status_code == output
        assert set(result_data) == {"result", "message", "err", "data"}
        assert type(result_data["message"]) == str
        assert result_data["message"] == "Validation error"
        assert result_data["err"] is not "" or []
        assert type(result_data["data"]) == list
        assert result_data["data"] == []


    @pytest.mark.parametrize("event_id, email_subject, email_content, from_email, to_email, timestamp, output", [
        (1, "Test Subject", "Test Content", "sender@example.com", ["recipient"], "2016-09-08 00:00:00", 400),
        (1, "Test Subject", "Test Content", "sender@example.com", ["recipient", "recipient2@example.com"], "2016-09-08 00:00:00", 400),
        (1, "Test Subject", "Test Content", "sender@example.com", ["recipient", "recipient2"], "2016-09-08 00:00:00", 400),
    ])
    def test_fail_recipient_wrong_data(self, server, event_id, email_subject, email_content, from_email, to_email, timestamp, output):
        payload: dict = {
            "event_id": event_id,
            "email_subject": email_subject,
            "email_content": email_content,
            "from_email": from_email,
            "to_email": to_email,
            "timestamp": timestamp
            }
        result = server.post("/save_emails", json=payload, content_type="application/json")
        result_data = loads(result.data)
        assert result.status_code == output
        assert set(result_data) == {"result", "message", "err", "data"}
        assert type(result_data["message"]) == str
        assert result_data["message"] == "Validation error"
        assert result_data["err"] is not "" or []
        assert type(result_data["data"]) == list
        assert result_data["data"] == []


    @pytest.mark.parametrize("event_id, email_subject, email_content, from_email, to_email, timestamp, output", [
        (1, "Test Subject", "Test Content", "sender@example.com", ["recipient@example.com"], "15 Dec 2015 23:12", 400),
        (1, "Test Subject", "Test Content", "sender@example.com", ["recipient@example.com"], "2016-09-08", 400),
        (1, "Test Subject", "Test Content", "sender@example.com", ["recipient@example.com"], "", 400),
    ])
    def test_fail_timestamp_wrong_data_format(self, server, event_id, email_subject, email_content, from_email, to_email, timestamp, output):
        payload: dict = {
            "event_id": event_id,
            "email_subject": email_subject,
            "email_content": email_content,
            "from_email": from_email,
            "to_email": to_email,
            "timestamp": timestamp
            }
        result = server.post("/save_emails", json=payload, content_type="application/json")
        result_data = loads(result.data)
        assert result.status_code == output
        assert set(result_data) == {"result", "message", "err", "data"}
        assert type(result_data["message"]) == str
        assert result_data["message"] == "Validation error"
        assert result_data["err"] is not "" or []
        assert type(result_data["data"]) == list
        assert result_data["data"] == []