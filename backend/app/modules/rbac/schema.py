from pydantic import BaseModel, ConfigDict


# ==========================
# Role Schemas
# ==========================

class RoleCreate(BaseModel):
    name: str
    description: str | None = None
    organization_id: str | None = None
    is_system: bool = False


class RoleResponse(BaseModel):
    id: str
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)


# ==========================
# Permission Schemas
# ==========================

class PermissionCreate(BaseModel):
    key: str
    resource: str
    action: str
    description: str | None = None


class PermissionResponse(BaseModel):
    id: str
    key: str
    resource: str
    action: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)


# ==========================
# Assign Permission Schema
# ==========================

class AssignPermission(BaseModel):
    permission_key: str