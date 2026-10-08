from uuid import UUID

import structlog
from sqlalchemy import and_, select

from core.models.webhook import Webhook

log = structlog.get_logger()


async def register_webhook(
    db,
    user_id: UUID,
    url: str,
) -> Webhook:
    """
    Register a callback URL for the user.
    Returns the existing record if the user already registered this URL.
    """
    stmt = select(Webhook).where(and_(Webhook.user_id == user_id, Webhook.url == url))
    result = await db.execute(stmt)
    existing = result.scalars().first()
    if existing:
        return existing

    webhook = Webhook(user_id=user_id, url=url)
    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)
    return webhook
