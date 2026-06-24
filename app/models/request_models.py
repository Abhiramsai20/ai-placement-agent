from pydantic import BaseModel


class PPTRequest(BaseModel):

    company: str
    days: int = 60