from app.models.user import UserContext

# Mock users database
_USERS = {
    "userA": UserContext(username="UserA", role="customer"),
    "userB": UserContext(username="UserB", role="customer"),
    "admin": UserContext(username="admin", role="admin"),
}

def get_user_context(username: str) -> UserContext:
    """
    Recupera il contesto utente.
    """
    if username not in _USERS:
        raise ValueError(f"User '{username}' not found")

    return _USERS[username]