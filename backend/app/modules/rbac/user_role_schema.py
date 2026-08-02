from pydantic import BaseModel


class AssignRoleRequest(BaseModel):
    user_id: str
    role_id: str


class UserRoleResponse(BaseModel):
    id: str
    user_id: str
    role_id: str

    class Config:
        from_attributes = True