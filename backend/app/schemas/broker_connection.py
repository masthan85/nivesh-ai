from pydantic import BaseModel, Field


class GrowwConnectRequest(BaseModel):
    access_token: str = Field(min_length=20, max_length=4096)
