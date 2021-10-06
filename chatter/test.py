import jwt
import time

claims = {"sub": "marcaron"}
data = jwt.encode(
    claims, 'f5da2edc-823a-4e72-ae98-c6de9714788e', algorithm="HS256")
