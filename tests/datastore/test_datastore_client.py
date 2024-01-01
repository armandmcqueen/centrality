from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient

from common import constants


def test_tokens(datastore: tuple[DatastoreConfig, DatastoreClient]):
    config, client = datastore
    client.reset_db()

    # Validate that create a new token works
    user_token = client.new_token()
    token_val = user_token.token
    assert client.validate_token(
        constants.CONTROL_PLANE_SDK_DEV_TOKEN
    ), "Dev token was not found"
    assert client.validate_token(
        token_val
    ), f"Newly added token {token_val} was not found"
    tokens = client.get_tokens()
    expected_tokens = {constants.CONTROL_PLANE_SDK_DEV_TOKEN, token_val}
    actual_tokens = set([token.token for token in tokens])
    assert (
        actual_tokens == expected_tokens
    ), f"get_tokens expected {expected_tokens}, got {actual_tokens}"

    client.reset_db()
    assert client.validate_token(
        constants.CONTROL_PLANE_SDK_DEV_TOKEN
    ), "After DB reset, dev token was not found"
    assert not client.validate_token(
        token_val
    ), "After DB reset, previously created token was found"

    # TODO: Add code to delete tokens and test it


def test_cpu_measurements(datastore: tuple[DatastoreConfig, DatastoreClient]):
    config, client = datastore
    client.reset_db()
