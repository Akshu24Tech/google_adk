# Safe vs Unsafe Patterns

## SQL Injection

 UNSAFE:
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
```

 SAFE:
```python
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

---

## Hardcoded Secrets

 UNSAFE:
```python
API_KEY = "sk-abc123xyz"
DB_PASSWORD = "admin123"
```

 SAFE:
```python
API_KEY = os.getenv("API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")
```

---

## Shell Injection

 UNSAFE:
```python
os.system(f"ping {user_input}")
subprocess.run(f"ls {path}", shell=True)
```

 SAFE:
```python
subprocess.run(["ping", user_input], shell=False)
```

---

## Weak Hashing

 UNSAFE:
```python
import hashlib
hashlib.md5(password.encode()).hexdigest()
```

 SAFE:
```python
import bcrypt
bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```
