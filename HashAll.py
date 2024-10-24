import argparse
import os
import subprocess


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Hash all password files with multiple hash algorithms")

    # Argument for the directory containing password files
    parser.add_argument('--directory', type=str, help="Directory containing password files")

    # Argument for the hash types (optional, defaults to md5, sha1, sha256)
    parser.add_argument('--hash_types', nargs='+', default=["md5", "sha1", "sha256", "sha512", "bcrypt", "pbkdf2"],
                        help="Hash types to apply (e.g., md5 sha1 sha256)")

    parser.add_argument('--output_directory', default="")    # Parse the arguments
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
                # Create an output file for each hash type
                output_file_name = f"{os.path.splitext(filename)[0]}_{hash_type}_output.txt"
                output_file_path = os.path.join(args.output_directory, output_file_name)

                # Running the second script for each file and each hash type
                result = subprocess.run(['python', 'HashPassword.py', '--hash_type', hash_type, '--password_file', file_path], capture_output=True, text=True)

                # print(hash_type, f" {filename}")
                # print(result.stdout)

                with open(output_file_path, 'w') as output_file:
                    if result.stdout:
                        output_file.write(f"{result.stdout}")
                    if result.stderr:
                        output_file.write(f"Error for {filename} with {hash_type}:\n{result.stderr}")

                # print(f"Results for {hash_type} saved to: {output_file_name}")

if __name__ == "__main__":
    main()
