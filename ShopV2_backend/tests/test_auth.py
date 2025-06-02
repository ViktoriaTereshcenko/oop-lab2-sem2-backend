from app.auth.jwt_handler import create_access_token, verify_access_token
from datetime import timedelta

def test_jwt_token_cycle():
    user_id = 123
    token = create_access_token(data={"sub": str(user_id)}, expires_delta=timedelta(minutes=5))
    decoded_id = verify_access_token(token)
    assert decoded_id == str(user_id)
