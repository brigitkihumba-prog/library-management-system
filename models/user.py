from models.person import Person


class User(Person):
    """A library user with a role and password hash."""

    def __init__(self, user_id, name, email, password_hash, role="borrower"):
        super().__init__(name, email)
        self.id = user_id
        self.password_hash = password_hash
        self._role = role

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value not in ("admin", "borrower"):
            raise ValueError("Invalid role")
        self._role = value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data["email"],
            data["password_hash"],
            data["role"],
        )