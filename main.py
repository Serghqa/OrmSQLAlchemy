import asyncio

from sqlalchemy import BigInteger, String, ForeignKey, insert, select
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship


class Base(DeclarativeBase):
    pass


class Trainer(Base):
    __tablename__ = 'trainer'

    trainer_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    group: Mapped[list['Client']] = relationship(back_populates='clients')

    def __repr__(self):
        return f'trainer_id: {self.trainer_id}, name: {self.name}'


class Client(Base):
    __tablename__ = 'client'

    client_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    trainer_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey('trainer.trainer_id'))
    clients: Mapped['Trainer'] = relationship(back_populates='group')


async def main():
    engine = create_engine(url='sqlite:///Fitnes.db', echo=False)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    trainer = Trainer(
        trainer_id=123456789,
        name='name'
    )
    client1 = Client(
        client_id=123654987,
        name='hdg',
        trainer_id=123456789
    )
    client2 = Client(
        client_id=123654988,
        name='hdgcc',
        trainer_id=123456789
    )
    Session = sessionmaker(engine, expire_on_commit=False)
    with Session() as session:
        session.add_all([trainer, client1, client2])
        session.commit()
        stmt = select(Trainer).where(123456789==Trainer.trainer_id)
        res = session.execute(stmt)
        for client in res.scalar().group:
            print(client.name)


if __name__ == '__main__':
    asyncio.run(main())
