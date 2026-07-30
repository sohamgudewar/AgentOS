from app.auth.hashing import hash_password, verify_password

password = "password123"

hashed = hash_password(password)

print(hashed)

print(
    verify_password(password, hashed)
)