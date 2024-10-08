import urllib.request
import os
import re
import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Function to sanitize the filename
def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

# Function to generate a unique filename from the URL
def generate_filename_from_url(url):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    url_basename = url.split('/')[-1]
    url_basename = sanitize_filename(url_basename)[:50]
    return f"{url_hash}_{url_basename}.jpg"

# Function to calculate the MD5 hash of file content
def calculate_file_hash(content):
    return hashlib.md5(content).hexdigest()

# Function to download files and prevent duplicates by content
def download_files(urls):
    total_urls = len(urls)
    duplicate_count = 0  # Initialize duplicate count
    downloaded_files_hashes = set()  # Store hashes of downloaded files

    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Ensure the URL is not empty
            try:
                filename = generate_filename_from_url(url)
                filepath = os.path.join('downloads', filename)

                response = urllib.request.urlopen(url)
                file_content = response.read()  # Read the file content

                # Calculate the hash of the file content
                file_hash = calculate_file_hash(file_content)

                if file_hash in downloaded_files_hashes:
                    duplicate_count += 1  # Increment duplicate count
                    # Update progress bar and counts without logging to console
                    progress_bar['value'] = (i + 1) / total_urls * 100  # Update progress bar
                    download_count_label.config(text=f"Downloaded: {i + 1}/{total_urls}")  # Update download count
                    duplicate_count_label.config(text=f"Duplicates: {duplicate_count}")  # Update duplicates count
                    root.update_idletasks()  # Update GUI
                    continue

                # Save the file since it is not a duplicate
                with open(filepath, 'wb') as f:
                    f.write(file_content)

                # Add the hash of this file content to the set of hashes
                downloaded_files_hashes.add(file_hash)

            except Exception:
                pass  # Handle errors silently

            # Update progress bar and counts after each download
            progress_bar['value'] = (i + 1) / total_urls * 100  # Update progress bar
            download_count_label.config(text=f"Downloaded: {i + 1}/{total_urls}")  # Update download count
            duplicate_count_label.config(text=f"Duplicates: {duplicate_count}")  # Update duplicates count
            root.update_idletasks()  # Update GUI

    messagebox.showinfo("Download Complete", f"All files have been downloaded.\nDuplicates encountered: {duplicate_count}")
    root.quit()  # Close the GUI

# Set up the main window
root = tk.Tk()
root.title("File Downloader")
root.geometry("400x250")  # Adjusted height to accommodate the new label

# Read URLs from the file
with open('list.txt', 'r') as file:
    urls = file.readlines()

# Create a directory to save the downloaded files
os.makedirs('downloads', exist_ok=True)

# Create a label to show the total number of items
total_items = len(urls)
total_items_label = tk.Label(root, text=f"Total items to download: {total_items}")
total_items_label.pack(pady=10)

# Create a progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20)

# Create a label to show the download count
download_count_label = tk.Label(root, text="Downloaded: 0/0")
download_count_label.pack(pady=5)

# Create a label to show the duplicate count
duplicate_count_label = tk.Label(root, text="Duplicates: 0")
duplicate_count_label.pack(pady=5)

# Create a start button
start_button = tk.Button(root, text="Start Download", command=lambda: download_files(urls))
start_button.pack(pady=10)

# Run the GUI
root.mainloop()
