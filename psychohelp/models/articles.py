import uuid

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID

from psychohelp.config.config import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False, comment="Уникальный URL")
    image = Column(String(1024), nullable=True)
    date = Column(DateTime(timezone=True), nullable=True)
    author = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    text = Column(Text, nullable=False)