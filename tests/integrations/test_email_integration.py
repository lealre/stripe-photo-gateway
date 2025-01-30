from src.integrations.email.email_integration import email, send_email


async def test_email_integration() -> None:
    email.config.SUPPRESS_SEND = 1

    subject_expected = 'Test Subject'
    recipients_expected = 'test@email.comn'

    with email.record_messages() as outbox:
        await send_email(subject=subject_expected, recipients=[recipients_expected])

        assert len(outbox) == 1
        assert outbox[0]['Subject'] == subject_expected
        assert outbox[0]['To'] == recipients_expected
