from pydantic import BaseModel, ConfigDict


class BaseSchemaMixin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
