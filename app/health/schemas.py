from pydantic import BaseModel, Field
from typing import Literal


class HealthResponse(BaseModel):
    status: Literal["ok"] = Field("ok")
    version: str = Field("v0.1.0")
    time_utc: str = Field("2025-09-27T19:44:35Z")
