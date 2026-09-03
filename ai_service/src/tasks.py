from .message_broker import message_broker


@message_broker.task
async def test_task():
    return "done"
