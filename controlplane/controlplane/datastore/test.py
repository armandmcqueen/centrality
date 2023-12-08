from controlplane.datastore.client import DatastoreClient

from controlplane.datastore.config import DefaultDatastoreConfig
from sqlalchemy import create_engine, text
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import ForeignKey


def main():
    config = DefaultDatastoreConfig()
    client = DatastoreClient(config)
    # client.reset_db()
    generated_token = client.new_token()
    print(f"New token generated: {generated_token}")
    existing_tokens = client.get_tokens()
    for token in existing_tokens:
        print(f"Existing token: {token}")

    authed = client.validate_token("dev", "dev")
    print(f"Authed: {authed}")


if __name__ == '__main__':
    main()