import inbund
from inbund.utils.log import Log
import time
inbund.unpack("/home/momen/projects/inbund/inbund/.config/inbund_test/bundles/bundle_template")

# log=Log()
# result = log.loading(
#     "loading task",
#     "task is in progress",
#     Log.MessageLevel.IN_PROGRESS,
#     lambda:  f"hi {time.sleep(10)}"
# )
# print(result)