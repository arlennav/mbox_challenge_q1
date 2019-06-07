# mbox_challenge_q1
Goal is to take this mbox file with your script and generate another mbox file with all the email messages.

# Dependencies

pip install tqdm

pip install asyncio

pip install aiofiles


# Quick note about aiofiles

Ordinary local file IO is blocking, and cannot easily and portably made asynchronous. This means doing file IO may interfere with asyncio applications, which shouldn't block the executing thread. aiofiles helps with this by introducing asynchronous versions of files that support delegating operations to a separate thread pool.

The Asynchronous I/O feature enhances performance by allowing applications to overlap processing with I/O operations.

![alt text](https://github.com/arlennav/Asyncio/blob/master/Asyncio.PNG) 

# Main python file
mbox.ipynb

# The script does:
1.	Reads the large mbox file asynchronously (from \Resources\mbox\mobox_filename).
2.	Splits by SPLIT_SIGNATURE into separate email files (\Resources\Split).
3.	Reads each individual email file asynchronously (from \Resources\Split).
4.	Separates email header and message body.
5.	Reverses message body and adds email signature.
6.	Merge email header and message body.
7.	Writes content into file asynchronously (\Resources\mbox\mobox_filename _reversed).
