import time
import os
from datetime import datetime
import psutil

file_path = os.getcwd() + '\\Zeiterfassung.txt'
date_format = "%d.%m.%Y"


class TaskTime:
    """
    Linked List to save time lapses for each task
    """

    def __init__(self):
        self.time_epoch = time.time()
        local_struct = time.localtime()
        self.time_local = time.strftime("%H:%M:00", local_struct)
        self.task = None
        self.subtask = None
        self.next_time = None

    def append(self, new_node):
        node = self
        while True:
            if node.next_time is None:
                break
            node = node.next_time
        node.next_time = new_node

    def get_tail(self):
        node = self
        while True:
            if node.next_time is None:
                break
            node = node.next_time
        return node

    def insert_node(self):
        pass

class TimeManager:

    def __init__(self):
        self.starting_time_epoch: float
        self.ending_time_epoch: float
        self.starting_time_local: str
        self.ending_time_local: str
        self.head_task = TaskTime()

    def save_starting_time(self):
        self.starting_time_epoch = time.time()
        starting_time_local_struct = time.localtime()
        self.starting_time_local = time.strftime("%H:%M:00", starting_time_local_struct)
        # save times in head of linked list
        self.head_task.time_epoch = self.starting_time_epoch
        self.head_task.time_local = self.starting_time_local

    def save_ending_time(self):
        self.ending_time_epoch = time.time()
        ending_time_local_struct = time.localtime()
        self.ending_time_local = time.strftime("%H:%M:00", ending_time_local_struct)
        # add last node to tail
        last_node = TaskTime()
        tail_task = self.head_task.get_tail()
        tail_task.append(last_node)

    def save_task_time(self, task, subtask):
        # save task
        tail_task = self.head_task.get_tail()
        tail_task.task = task
        tail_task.subtask = subtask
        # add next node which saves time of next task
        next_task = TaskTime()
        tail_task.append(next_task)

    def get_total_elapsed_time(self) -> str:
        return get_time_as_str(self.ending_time_epoch - self.starting_time_epoch)

    def get_current_elapsed_time(self):
        reference_time = time.time()
        return get_time_as_str(reference_time - self.starting_time_epoch)

    def write_tasks(self):
        """
        TODO write to file linked list from self.head_task. if self.head_task.time_epoch < epoch from daily starting time, write daily time lapse and continue with next node in linked list. Same applies for regeltermin.
            Implement way to select in dropdown menu if daily/regeltermin has to be considered for writing and if the ending times have to defined by user
        :return:
        """
        pass
    @staticmethod
    def __get_time_as_str(elapsed_time_sec) -> str:
        if elapsed_time_sec < 60:
            # return in seconds
            return str(round(elapsed_time_sec)) + "sec"
        elif 60 <= elapsed_time_sec < 3600:
            # return in minutes
            return str(round(elapsed_time_sec / 60.0, 2)) + "min"
        elif elapsed_time_sec >= 3600:
            # return in hours
            return str(round(elapsed_time_sec / 3600, 2)) + "hr"

def start_timer():
    global last_session_text
    text_file_lines = []
    topics = []
    text_to_write = ''
    global_starting_time = time.localtime()
    global_starting_time_str = time.strftime("%H:%M", global_starting_time) + ":00"
    global_starting_time = time.time()
    print('Timer initiated. To stop press ENTER.')
    time_reference = global_starting_time
    while True:
        if input() == "":  # every time is waiting for input it stops at this line
            break
        else:
            elapsed_time = time.time() - time_reference
            time_reference = time.time()
            if elapsed_time > 5:
                print('Current time spent in task ' + get_time_as_str(time.time() - global_starting_time))
            continue


    print('Do you want to input starting time manually (H:M)?')
    manual_input_starting_time = input()
    if ":" in manual_input_starting_time:
        global_starting_time_str = manual_input_starting_time + ":00"
        # get struct_time tuple with time.strptime() and pass as param in time.mktime() to convert to seconds (float)
        global_starting_time = time.mktime(time.strptime(global_starting_time_str + "-" + time.strftime(date_format, time.localtime()), "%H:%M:%S" + "-" + date_format))  # default year of 1900 is to early to convert, input 2000 instead

    global_ending_time = time.localtime()
    global_ending_time_str = time.strftime("%H:%M", global_ending_time) + ":00"
    global_ending_time = time.time()
    time_spend_in_task = get_time_as_str(global_ending_time - global_starting_time)

    date = time.strftime(date_format, time.localtime())
    text_file_lines.append(date)

    print('Timer stopped. Please enter title of tasks in session or enter "-last" to use last session.')
    task_title = input()  # todo handle exception for when just enter is input
    last_session_defined = False
    if task_title == "-last":  # if user wants to use last session text, save text in topics and mark session as defined
        text_to_write = last_session_text  # todo if last_session_text == "" star new input for task_title
        last_session_defined = True

    if not last_session_defined:  # if session has not been defined, use a new session with new task topic and topics
        print('Please enter topic in session or press ENTER to save session.')
        task_topic = input()
        while task_topic != "":
            topics.append(task_topic)
            task_topic = input()

        # add topics to time window and title
        text_to_write = task_title + " "
        for topic in topics:
            text_to_write = text_to_write + topic + " "
        # current text to write is saved in global variable if it is not the "D/-daily" task
        if "aily" not in text_to_write:
            last_session_text = text_to_write

    # define default starting and end times
    internal_appointment_starting_time = '08:30:00'
    internal_appointment_end_time = '09:00:00'
    daily_starting_time = '09:00:00'
    daily_end_time = '09:30:00'

    # modify starting and en times via user input
    print('Regeltermin timer started at 08:30. Enter end time or use default (ENTER)')
    input_end_time = input()
    if input_end_time != '':
        internal_appointment_end_time = input_end_time + ':00'
    print('Regeltermin timer started at 09:30. Enter end time or use default (ENTER)')
    input_end_time = input()
    if input_end_time != '':
        daily_end_time = input_end_time + ':00'

    time_spend_in_internal_appointment = get_elapsed_time_from_str(internal_appointment_starting_time, internal_appointment_end_time)
    time_spend_in_daily = get_time_as_str(get_elapsed_time_from_str(daily_starting_time, daily_end_time))

    morning_period = False
    # if it is less than 12 o'clock it is morning period
    if int(time.strftime("%H", time.localtime())) < 12:
        morning_period = True
    # append modified or unmodified starting and end times in list to print
    if time_spend_in_internal_appointment == 0 and morning_period:
        # no internal appointment conducted
        text_file_lines.append(global_starting_time_str + '-' + daily_starting_time + ' : ' + text_to_write)
        text_file_lines.append(daily_starting_time + '-' + daily_end_time + ' : ' + "Daily")
        text_file_lines.append(daily_end_time + '-' + global_ending_time_str + ' : ' + text_to_write)
        text_file_lines.append("Total time spend: " + time_spend_in_task)
    elif time_spend_in_daily == 0 and morning_period:
        # no daily appointment conducted
        text_file_lines.append(global_starting_time_str + '-' + internal_appointment_starting_time + ' : ' + text_to_write)
        text_file_lines.append(internal_appointment_starting_time + '-' + internal_appointment_end_time + ' : ' + "Regeltermin Norbert/Matti")
        text_file_lines.append(internal_appointment_end_time + '-' + global_ending_time_str + ' : ' + text_to_write)
        text_file_lines.append("Total time spend: " + time_spend_in_task)
    elif (time_spend_in_internal_appointment == 0 and time_spend_in_daily == 0) or not morning_period:
        # no daily nor internal appointment conducted
        text_file_lines.append(global_starting_time_str + '-' + global_ending_time_str + ' : ' + text_to_write)
        text_file_lines.append("Total time spend: " + time_spend_in_task)
    else:
        # internal and daily appointment conducted
        text_file_lines.append(global_starting_time_str + '-' + internal_appointment_starting_time + ' : ' + text_to_write)
        text_file_lines.append(internal_appointment_starting_time + '-' + internal_appointment_end_time + ' : ' + "Regeltermin Norbert/Matti")
        text_file_lines.append(internal_appointment_end_time + '-' + daily_starting_time + ' : ' + text_to_write)
        text_file_lines.append(daily_starting_time + '-' + daily_end_time + ' : ' + "Daily")
        text_file_lines.append(daily_end_time + '-' + global_ending_time_str + ' : ' + text_to_write)
        text_file_lines.append("Total time spend: " + time_spend_in_task)

    # check if text file is empty
    if os.stat(file_path).st_size == 0:
        with open(file_path, mode='w') as f:  # only write mode
            for new_line in text_file_lines:
                f.write(new_line)
                f.write('\n')
        f.close()
    else:
        new_day = True
        with open(file_path, mode='r') as f:  # only read mode
            for existing_line in f.readlines():
                if date in existing_line:  # line with date exists, it is not a new day
                    new_day = False
                    break
        with open(file_path, mode='a+') as f:  # only append mode that jumps to the end
            f.write('\n')
            start_index = 1
            if new_day:
                start_index = 0
            for new_line in text_file_lines[start_index:]:
                f.write(new_line)
                f.write('\n')

    print('Time session has been written successfully. Do you want to start another timer? y/n')
    start_new_timer = input()
    if start_new_timer == 'y':
        start_timer()
    elif start_new_timer == 'n':
        print('Timer tool finalized')


def get_time_as_str(elapsed_time_sec):
    if elapsed_time_sec < 60:
        # return in seconds
        return str(round(elapsed_time_sec)) + "sec"
    elif 60 <= elapsed_time_sec < 3600:
        # return in minutes
        return str(round(elapsed_time_sec/60.0, 2)) + "min"
    elif elapsed_time_sec >= 3600:
        # return in hours
        return str(round(elapsed_time_sec/3600, 2)) + "hr"

def get_elapsed_time_from_str(start_time_str, end_time_str):
    '''

    :param start_time_str:
    :param end_time_str:
    :return:
    '''
    (h, m, s) = start_time_str.split(':')
    start_time = int(h) * 3600 + int(m) * 60 + int(s)
    (h, m, s) = end_time_str.split(':')
    end_time = int(h) * 3600 + int(m) * 60 + int(s)
    return end_time - start_time

def monitor_open_apps():
    """
    TODO Monitors open apps and closes if currently in deep work session: https://stackoverflow.com/questions/7787120/check-if-a-process-is-running-or-not-on-windows . If deep work session is over, programm can be opened again

    :return:
    """
    for p in psutil.process_iter():
        p.name() # .exe string
        p.name()

if __name__ == "__main__":
    monitor_open_apps()
    start_timer()
