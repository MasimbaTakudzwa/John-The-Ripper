import hashlib
import bcrypt
import argparse
import sys


# Hashing functions
def hash_md5(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def hash_sha1(password: str) -> str:
    return hashlib.sha1(password.encode()).hexdigest()


def hash_sha256(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def hash_sha512(password: str) -> str:
    return hashlib.sha512(password.encode()).hexdigest()


def hash_bcrypt(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def hash_pbkdf2(password: str, salt: str = "somesalt") -> str:
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return dk.hex()


# Function to choose hash based on user input
def hash_password(hash_type: str, password: str):
    if hash_type == "md5":
        return hash_md5(password)
    elif hash_type == "sha1":
        return hash_sha1(password)
    elif hash_type == "sha256":
        return hash_sha256(password)
    elif hash_type == "sha512":
        return hash_sha512(password)
    elif hash_type == "bcrypt":
        return hash_bcrypt(password)
    elif hash_type == "pbkdf2":
        return hash_pbkdf2(password)
    else:
        raise ValueError(f"Unsupported hash type: {hash_type}")


# Command-line argument parsing
def main():
    parser = argparse.ArgumentParser(description="Hash a password using the specified hash algorithm.")
    parser.add_argument("--hash_type", choices=["md5", "sha1", "sha256", "sha512", "bcrypt", "pbkdf2"],
                        help="The type of hash algorithm to use. ")
    parser.add_argument("--password_file", help="The file containing the passwords that need to be hashed")

    # Optional salt for PBKDF2
    parser.add_argument("--salt", help="Salt for PBKDF2 (optional, defaults to 'somesalt').", default="somesalt")

    # Parse the arguments
    args = parser.parse_args()


    try:
        with open(args.password_file, "r") as file:
            passwords = file.readlines()
            if args.hash_type == "pbkdf2":
                for password in passwords:
                    password = password.strip() # Remove any leading/trailing whitespace
                    hashed_password = hash_password(password=password, hash_type="pbkdf2")
                    # print(f"{password} : {hashed_password}")
                    print(f"{hashed_password}")

    # Perform the hashing
            else:
                for password in passwords:
                    password = password.strip() # Remove any leading/trailing whitespace
                    hashed_password = hash_password(password=password, hash_type=args.hash_type)
                    # print(f"{password} : {hashed_password}")
                    print(f"{hashed_password}")

    except FileNotFoundError:
        print(f"Error: File {args.password_file} not found.")
        sys.exit(1)
    # Output the result



if __name__ == "__main__":
    main()
