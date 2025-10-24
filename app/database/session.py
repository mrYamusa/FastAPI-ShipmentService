from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import database_settings
from sqlmodel import SQLModel
from rich import panel, print
from fastapi import Depends
from typing import Annotated


engine = create_async_engine(url=database_settings.postgres_url, echo=True)


async def create_db_tables():
    async with engine.begin() as connection:
        print(panel.Panel(renderable="Creating database tables...", style="bold green"))
        await connection.run_sync(SQLModel.metadata.create_all)
    print(
        panel.Panel(
            renderable="Database tables created successfully...", style="bold green"
        )
    )


async def create_session():
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        print(
            panel.Panel(
                renderable="Session started successfully...", style="bold green"
            )
        )
        yield session
        print(
            panel.Panel(renderable="Session stopped successfully...", style="bold red")
        )


SessionDep = Annotated[AsyncSession, Depends(create_session)]
# session = Session(bind=engine)
# session.get(Shipments, 4)
# session.add(Shipments(content="Book", weight=2.5, status="Placed"))
# session.commit()
