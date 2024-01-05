DownloadIMAP.py is a Python script designed to download emails from a specified mailbox on an IMAP server and save them into a file.

PixelScanEmail.py is a Python script designed to scan downloaded emails for tracking pixels, which are typically used for tracking email opens and other analytics.
It's useful for analyzing emails to identify and report tracking pixels, which is helpful for privacy analysis, marketing insights, or email campaign tracking.
If executed with the correct arguments and user confirmation, the script scans the specified email file for tracking pixels. 
It does this by reading the file, extracting image URLs from the emails, and then processing these URLs according to the provided options (such as filtering by domain or ignoring embedded images).
The script outputs information about the scanned emails and the identified image URLs, along with associated data like reference counts and details about the emails containing these images.
