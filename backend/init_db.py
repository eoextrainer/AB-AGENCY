from app.db import init_database


def run() -> None:
    init_database()


if __name__ == "__main__":
    run()
