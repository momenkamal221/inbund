import sys
import os
import time
import threading
from datetime import datetime
import json

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m" 
WHITE = "\033[97m"
RED_BACKGROUND = "\033[41m"
BOLD = "\033[1m"
RESET_BOLD = "\033[0m"
class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()

class Log:
    
    is_task_in_progress=False
    class MessageLevel:
        SUCCESS="SUCCESS"
        ERROR="ERROR"
        WARNING="WARNING"
        INFO="INFO"
        IN_PROGRESS="IN_PROGRESS"
        CRITICAL="CRITICAL"
        DEBUG="DEBUG"
    
    def __init__(self,log_file_path="") -> None:
        if not log_file_path.strip() == "":
            self.log_file_path=self.set_log_file(log_file_path)
        self.logs=[]
        self.log_dir=""

    def log_to_file(self,log):
        if self.log_file_path == "":
            return
        strLog=self.string_log(log)
        with open(self.log_file_path, "a") as log_file:
            log_file.write(strLog + "\n")
        
        
    def set_log_file(self,log_file_path):
        print(log_file_path)
        if not os.path.exists(log_file_path):
            # Get the directory name from the file path
            directory = os.path.dirname(log_file_path)
            # Create parent directories if they don't exist
            if not os.path.exists(directory):
                os.makedirs(directory)

        self.log_file_path=log_file_path
    
        
    def make_log_message(task_name, message, message_level=MessageLevel.INFO):
        if message_level.upper() == Log.MessageLevel.ERROR:
            log_type_color=RED
        elif message_level.upper() == Log.MessageLevel.SUCCESS:
            log_type_color=GREEN
        elif message_level.upper() == Log.MessageLevel.WARNING:
            log_type_color=YELLOW
        elif message_level.upper() == Log.MessageLevel.IN_PROGRESS:
            log_type_color=CYAN
        elif message_level.upper() == Log.MessageLevel.DEBUG:
            log_type_color=BLUE
        elif message_level.upper() == Log.MessageLevel.CRITICAL:
            log_type_color= RED_BACKGROUND + WHITE
        else:
            log_type_color=WHITE
        
        task_name_colored = f"{BOLD}{log_type_color}[{task_name}]{RESET_BOLD}{RESET}"
        return f"{task_name_colored} {message}"


    def print_log(Log_message_colored):
        sys.__stdout__.write(Log_message_colored + "\n" )
        sys.__stdout__.flush()


    def log(self, task_name, message, message_level=MessageLevel.INFO,comment="",log_to_file=False):
        Log_message_colored = Log.make_log_message(task_name, message, message_level)
        Log.print_log(Log_message_colored)
        log={
            "time_stamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "task_name":task_name,
            "message":message,
            "message_level":message_level,
            "comment":comment
        }
        self.logs.append(log)
        if log_to_file:
            self.log_to_file(log)


    def remove_last_line():
        sys.__stdout__.write("\033[F") # Move cursor up one line
        sys.__stdout__.write("\033[K") # Clear the line
        sys.__stdout__.flush()
    
    def undo_log(self):
        Log.remove_last_line()
        self.logs.pop()
        
    def loading(self,task_name, message,message_level=MessageLevel.INFO,background_task=lambda:None,*args, **kwargs):
        """will make loading dots after the given log
        Note: this function will remove the log message after is being finished, it's up to you if you want to log the task result or not
        Args:
            background_task (function): once this task is finished will
        """
        return_value=None
        
        def loading_log_loop():
            dots_Count=0
            while not done_event.is_set():
                sys.stdout = sys.__stdout__
                self.log(task_name,f"{message}{''.join(["." for _ in range(dots_Count)])}" ,message_level)
                sys.stdout = None
                time.sleep(0.4)
                self.undo_log()
                dots_Count = (1 + dots_Count) % 4
                
        
        def do_task():
            # https://chatgpt.com/share/d39ff9da-d45a-4270-96dd-ba6e17bf8057
            Log.is_task_in_progress=True
            nonlocal return_value
            return_value = background_task(*args, **kwargs)
            Log.is_task_in_progress=False
            done_event.set()
        
        # Create an event to signal when the background task is done
        done_event = threading.Event()
        # Create thread objects for both tasks
        loading_thread = threading.Thread(target=loading_log_loop)
        background_thread = threading.Thread(target=do_task)
        # Start the loading dots thread
        loading_thread.start()
        # Start the background task thread
        background_thread.start()
        # Wait for the background task to finish
        background_thread.join()
        # Wait for the loading dots to finish
        loading_thread.join()
        
        sys.stdout = sys.__stdout__
        return return_value
    
    
    def get_report(self):
        report:str=""
        for log in self.logs:
            report += f"{self.string_log(log)}\n"
        return report
    

    def string_log(self,log):
        return f"[{log["time_stamp"]}] {log["message_level"].lower()} {  json.dumps({"task_name":log["task_name"],"message":log["message"],"comment":log["comment"]}) }"