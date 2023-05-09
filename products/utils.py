import time

def time_consuming_task():
    # some long running task like sending emails/sms, creating pdf, etc.
    time.sleep(2)
    print("Task completed")
    return True