from jose import jwt, JWTError


class JWTAuth:
    def __init__(self):
        self.secret_key = (
            "xpp01gjey2c4566bdq50edit0y2qarlsozkuho23s0omye0sw8q3r8djcyl2afwz"
        )
        self.algorithm = "HS256"

    def jwt_encode(self, data):
        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)

    def jwt_decode(self, jwt_code: str):
        try:
            return jwt.decode(jwt_code, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            return None
