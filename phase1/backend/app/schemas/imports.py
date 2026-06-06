from pydantic import BaseModel


class ImportResult(BaseModel):
    dataset: str
    imported: int
    failed: int
    errors: list[str]
