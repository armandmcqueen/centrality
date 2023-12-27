from typing import Optional, Annotated
from fastapi import APIRouter, Depends
from controlplane.rest.utils.auth import auth, security
from controlplane.datastore.client import DatastoreClient
from controlplane.datastore.config import DatastoreConfig

from fastapi.security import HTTPAuthorizationCredentials


# TODO: Remove this as soon as we have a real subcomponent
router = APIRouter(
    prefix="/example",
    tags=["example"],
    responses={404: {"description": "Not found"}},
)

datastore_config = DatastoreConfig.from_envvar()
datastore_client = DatastoreClient(config=datastore_config)


@router.get("/hello")
def hello():
    return {"Hello": "World"}


@router.get("/hello/auth")
@auth(datastore_client)
def hello_auth(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
):
    return {"Hello": "World"}
