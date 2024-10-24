import argparse
import os
import subprocess
import bcrypt


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Hash all password files with multiple hash algorithms")

    # Argument for the directory containing password files
    parser.add_argument('--directory', type=str, help="Directory containing password files")

    # Argument for the hash types (optional, defaults to md5, sha1, sha256)
    parser.add_argument('--hash_types', nargs='+', default=["md5", "sha1", "sha256", "sha512", "bcrypt", "pbkdf2"],
                        help="Hash types to apply (e.g., md5 sha1 sha256)")

    # Parse the arguments
    args = parser.parse_args()

    # Check if the directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: Directory {args.directory} not found.")
        return

    # Process all .txt files in the directory
    for filename in os.listdir(args.directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(args.directory, filename)
            print(f"\nProcessing file: {filename}")

            # Call the hashing script for each hash type
            for hash_type in args.hash_types:
                # Running the second script for each file and each hash type
                result = subprocess.run(
                    ['python', 'HashPassword.py', '--hash_type', hash_type, '--password_file', file_path],
                    capture_output=True, text=True
                )

                # Print stdout (output) and stderr (error messages)
                if result.stdout:
                    print(f"Output for {filename} with {hash_type}:\n{result.stdout}")
                if result.stderr:
                    print(f"Error for {filename} with {hash_type}:\n{result.stderr}")


if __name__ == "__main__":
    main()
