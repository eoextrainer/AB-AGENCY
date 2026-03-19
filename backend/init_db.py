from app.db import Base, engine


def run() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    run()
