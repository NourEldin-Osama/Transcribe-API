from sqlmodel import SQLModel, create_engine, Session

# Define the SQLite database file and connection URL
sqlite_file_name = "links.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Create the engine
engine = create_engine(sqlite_url, echo=True)

# Function to create the database and tables


def get_session():
    with Session(engine) as session:
        yield session
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
