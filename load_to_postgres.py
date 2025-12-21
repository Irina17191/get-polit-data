import pandas as pd
from sqlalchemy import create_engine


# налаштування підключення
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "db_politdata"


# підключення до postgres

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    connect_args={"client_encoding": "utf8"}
)


# заливка step_1_political_parties_all.py

def load_step_1():
    print("Починаю заливку step_1_political_parties_all ...")

    df = pd.read_excel("step_1_political_parties_all.xlsx", engine="openpyxl")

    df.to_sql(
        name="step_1_political_parties_all",
        con=engine,
        if_exists="replace",
        index=False,
        schema="public"
    )

    print("step_1_political_parties_all успішно залитий у PostgreSQL")




if __name__ == "__main__":
    load_step_1()