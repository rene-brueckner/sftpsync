import ftplib
import os
import time

FTP_HOST = os.environ.get("FTP_HOST", "localhost")
FTP_USER = os.environ.get("FTP_USER", "user")
FTP_PASS = os.environ.get("FTP_PASS", "password")
REMOTE_DIR = os.environ.get("REMOTE_DIR", "/")
EXCLUDE_DIR = os.environ.get("EXCLUDE_DIR", "")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "60"))
LOCAL_DOWNLOAD_DIR = os.environ.get("LOCAL_DOWNLOAD_DIR", "./data")


def connect_to_ftp():
    """Establish an FTP connection."""
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    return ftp

def download_files(ftp, remote_dir="/"):
    """
    Download all files from the remote directory,
    excluding files in the EXCLUDE_DIR.
    """
    try:
        ftp.cwd(remote_dir)
        items = ftp.nlst()

        for item in items:
            if item == EXCLUDE_DIR or item == "." or item == "..":
                print(f"Skipping directory: {item}")
                continue

            try:
                ftp.cwd(item)
                print(f"Entering directory: {item}")
                download_files(ftp, item)
                ftp.cwd("..")
            except ftplib.error_perm:
                local_file_path = os.path.join(LOCAL_DOWNLOAD_DIR, item)
                if not os.path.exists(LOCAL_DOWNLOAD_DIR):
                    os.makedirs(LOCAL_DOWNLOAD_DIR)

                if not os.path.exists(local_file_path):
                    print(f"Downloading file: {item}")
                    with open(local_file_path, "wb") as f:
                        ftp.retrbinary(f"RETR {item}", f.write)
                else:
                    print(f"File already exists: {item}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True: 
        try:
            print("Connecting to FTP server...")
            ftp = connect_to_ftp()
            print("Connected.")
            download_files(ftp, REMOTE_DIR)
            ftp.quit()
            print(f"Sleeping for {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
