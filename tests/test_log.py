from inbund.utils import Log
import pprint
import time
delay=0.05

logs=Log()

logs.log("Test","this is an normal message test")
time.sleep(delay)
logs.undo_log()


logs.log("Test","this is an info message","info")
time.sleep(delay)
logs.log("Test","this is a warning message","warning")
time.sleep(delay)
logs.log("Test","this is a success message","success")
time.sleep(delay)
logs.log("Test","this is an error message","error")
time.sleep(delay)
logs.log("Test","this is a critical message","CRITICAL")
time.sleep(delay)
logs.log("Test","this is a debug message","debug")
time.sleep(delay)
logs.log("Test","this is a in progress message","IN_PROGRESS")

def callback():
    time.sleep(3)
    return False


print("--------------------------------------------")
callback_output=logs.loading("Testing","this is a loading test1","IN_PROGRESS",callback)
if callback_output:
    logs.log("Test","loading is finished successfully","success")
else:
    logs.log("Test","loading is failed","error")

def callback():
    time.sleep(3)
    return True
print("--------------------------------------------")
callback_output=logs.loading("Testing","this is a loading test2","IN_PROGRESS",callback)
if callback_output:
    logs.log("Test","test loading is finished successfully","success")
else:
    logs.log("Test","test loading is failed","error")
print("--------------------------------------------")
callback_output=logs.loading("Testing","this is a loading test2","IN_PROGRESS")


pprint.pprint(logs.logs)
print(logs.report())
