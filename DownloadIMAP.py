import imaplib
import email
import sys

def download_mailbox(username, password, server, mailbox, output_file):
    # Connect to the IMAP server
    try:
        imap = imaplib.IMAP4_SSL(server)
    except imaplib.IMAP4.error as e:
        print(f"IMAP connection error: {e}")
        return

    # Login to the server
    try:
        imap.login(username, password)
    except imaplib.IMAP4.error as e:
        print(f"Login failed: {e}")
        imap.logout()
        return

    # Select the mailbox
    try:
        imap.select(mailbox, readonly=True)  # Open the mailbox in read-only mode
    except imaplib.IMAP4.error as e:
        print(f"Failed to select mailbox '{mailbox}': {e}")
        imap.logout()
        return

    # Open the output file for writing
    try:
        mbox_file = open(output_file, 'w')
    except IOError as e:
        print(f"Failed to open MBOX file '{output_file}': {e}")
        imap.logout()
        return

    # Retrieve messages from the mailbox
    try:
        status, data = imap.search(None, 'ALL')
        if status == 'OK':
            message_ids = data[0].split()
            total_messages = len(message_ids)
            print(f"Total messages in mailbox: {total_messages}")
            for i, message_id in enumerate(message_ids, start=1):
                print(f"Downloading message {i}/{total_messages}")
                status, msg_data = imap.fetch(message_id, '(RFC822)')
                if status == 'OK':
                    message = email.message_from_bytes(msg_data[0][1])
                    mbox_file.write(str(message))
                    mbox_file.write('\n')
    except imaplib.IMAP4.error as e:
        print(f"Failed to retrieve messages: {e}")

    # Close the output file and logout from the server
    mbox_file.close()
    imap.logout()

    print("Mailbox download completed.")

print("Copyright (C) 2023 James Collings")
print("Disclaimer: By using this software, the user agrees and understands that the writer ", end="")
print("bears no responsibility for any consequences, direct or indirect, arising from its use. ", end="")
print("Use of this software is at your own risk and you agree to not use the software if this disclaimer cannot be fully applied. Caveat emptor applies.")

# Prompt the user to decide whether to proceed
proceed = input("Do you wish to proceed? (y/n): ").strip().lower()

if proceed == 'y':
    if __name__ == '__main__':
        if len(sys.argv) != 6:
            print("Usage: python script.py username password server mailbox output_file")
        else:
            username = sys.argv[1]
            password = sys.argv[2]
            server = sys.argv[3]
            mailbox = sys.argv[4]
            output_file = sys.argv[5]

            download_mailbox(username, password, server, mailbox, output_file)
else:
    print("Operation cancelled.")