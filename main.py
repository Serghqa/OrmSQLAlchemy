import asyncio

from sqlalchemy import BigInteger, String, ForeignKey, insert, select
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Trainer(Base):
    __tablename__ = 'trainer'

    trainer_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f'trainer_id: {self.trainer_id}, name: {self.name}'


class Group(Base):
    __tablename__ = 'group'

    client_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    trainer_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey('trainer.trainer_id'))


async def main():
    engine = create_engine(url='sqlite:///Fitnes.db', echo=False)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    trainer = Trainer(
        trainer_id=123456789,
        name='name'
    )
    client = Group(
        client_id=123654987,
        name='hdg',
        trainer_id=123456789
    )
    with Session(engine, expire_on_commit=False) as session:
        session.add_all([trainer, client])
        session.commit()
        result = session.get(Trainer, 123456789)
        print(result)


if __name__ == '__main__':
    asyncio.run(main())
