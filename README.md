DownloadIMAP.py is a Python script designed to download emails from a specified mailbox on an IMAP server and save them into a file.
```
Usage: python DownloadIMAP.py username password server mailbox output_file
```

PixelScanEmail.py is a Python script designed to scan downloaded emails for tracking pixels, which are typically used for tracking email opens and other analytics.
It's useful for analyzing emails to identify and report tracking pixels, which is helpful for privacy analysis, marketing insights, or email campaign tracking.
If executed with the correct arguments and user confirmation, the script scans the specified email file for tracking pixels. 
It does this by reading the file, extracting image URLs from the emails, and then processing these URLs according to the provided options (such as filtering by domain or ignoring embedded images).
The script outputs information about the scanned emails and the identified image URLs, along with associated data like reference counts and details about the emails containing these images.
```
usage: python PixelScanEmail.py [-h] [-d DOMAIN] [-e] [-u] [-m MAX_UNIQUE_NAMES] [-i] file_path
```
Parameters

    file_path: The path to the RFC822 formatted file containing emails. It's the primary input for the tool, specifying where the email data is located.

    -d, --domain: Filters the emails to be scanned based on the specified domain. Only emails from this domain will be considered in the scan.

    -e, --ignore-embedded: When set, this flag instructs the scanner to ignore embedded images in emails. This can be useful for focusing on external tracking pixels.

    -u, --unique-names: Activates the search for images with unique names only. This is particularly useful when trying to identify specific tracking pixels or unique image URLs.

    -m, --max-unique-names: Sets the maximum number of unique image names to track. It takes an integer value and is useful for limiting the scope of the scan to avoid performance issues with large datasets.

    -i, --image-domain: When enabled, the scanner processes only images that come from a different domain than the sender's domain. This helps in focusing on third-party tracking pixels.

Example use
```
$ python PixelScanEmail.py INBOX
or
$ python PixelScanEmail.py INBOX -d example.com -e -u -m 500 -i
```

