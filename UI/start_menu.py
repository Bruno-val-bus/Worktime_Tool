import kivy
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewNode, TreeViewLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import Time_tool


class MyTreeView(TreeView):
    def __init__(self, **kwargs):
        super(MyTreeView, self).__init__(**kwargs)
        self.add_node(TreeViewLabel(text="Node 1"))
        self.add_node(TreeViewLabel(text="Node 2"))
        self.add_node(TreeViewLabel(text="Node 3"))


class TreeNode(TreeViewLabel):
    def __init__(self, **kwargs):
        super(TreeNode, self).__init__(**kwargs)
        self.btn = Button(text="Push Me !")
        self.add_widget(self.btn)


class TreeNodeInput(BoxLayout, TreeViewNode):
    def __init__(self, **kwargs):
        super(TreeNodeInput, self).__init__(**kwargs)
        self.text = kwargs.get('text', '')
        self.input = TextInput(text='', multiline=False)
        self.add_widget(self.input)


class StartMenuGrid(GridLayout):
    """"
    build with kv file: https://www.techwithtim.net/tutorials/kivy-tutorial/multiple-screens/
    TODO write necessary files to deploy app in other servers: nice workflow in requirements-versioning-rule file and in https://suyojtamrakar.medium.com/managing-your-requirements-txt-with-pip-tools-in-python-8d07d9dfa464
        you might need to first migrate to venv
    """

    def __init__(self, **kwargs):
        super(StartMenuGrid, self).__init__(**kwargs)
        self.time_manager = Time_tool.TimeManager()
        self.tree_view_widget = self.ids.todo_tree

        self.tree_view_widget.add_node(TreeViewLabel(text="TODO 1"))
        self.tree_view_widget.add_node(TreeViewLabel(text="TODO 2"))
        self.tree_view_widget.add_node(TreeViewLabel(text="TODO 3"))

    def add2selected_node(self):
        selected_node = self.tree_view_widget.selected_node
        current_input = self.ids.todo_input.text
        print(selected_node)
        if selected_node:
            new_tree_label = TreeViewLabel(text=current_input)
            self.tree_view_widget.add_node(new_tree_label, selected_node)
        else:
            print("Please select group to add TODO")

    def remove_selected_node(self):
        selected_node = self.tree_view_widget.selected_node
        if selected_node:
            self.tree_view_widget.remove_node(selected_node)
        else:
            print("Please select TODO to remove")

    def start_timer_btn(self, stop_timer_button, start_timer_button, time_task_button, task_input, subtask_input,
                        print_time_button):
        start_timer_button.disabled = True
        stop_timer_button.disabled = False
        time_task_button.disabled = False
        task_input.disabled = False
        subtask_input.disabled = False
        print_time_button.disabled = False
        self.time_manager.save_starting_time()
        print("Timer started")

    def stop_timer_btn(self, start_timer_button, stop_timer_button, time_task_button, task_input, subtask_input,
                       print_time_button):
        stop_timer_button.disabled = True
        time_task_button.disabled = True
        start_timer_button.disabled = False
        task_input.disabled = True
        subtask_input.disabled = True
        print_time_button.disabled = True
        self.time_manager.save_ending_time()
        total_elapsed_time = self.time_manager.get_total_elapsed_time()
        print(f"Timer stopped. You worked {total_elapsed_time} today")

    def time_task_btn(self, task_input, subtask_input):
        task = task_input.text
        if task == "":
            print("Unable to save task without task name.")
            return
        # save task only if there is input from user in task field
        subtask = subtask_input.text
        self.time_manager.save_task_time(task, subtask)
        print(f"Task saved: {task}. Subtask saved: {subtask}")
        # reset field
        task_input.text = ""
        subtask_input.text = ""

    def print_time(self):
        elapsed_time = self.time_manager.get_current_elapsed_time()
        print(f"You have worked {elapsed_time}")


class DesktopApp(App):
    """
    base Class of your App inherits from the App class.
    app:always refers to the instance of your application

    Creating a .kv File
    Naming: The name of your .kv file must follow the rules below in order for python/kivy to be able to see and load the file.
    1. It must be all lowercase
    2. It must match with the name of your main class. (The one that has the build method)
    3. If the name of your main class ends in "app" (lowercase or uppercase) you must not include "app" in your file name.
    File Location: The file must be in the same directory as your python script.
    """

    def build(self):
        return StartMenuGrid()


if __name__ == "__main__":
    app = DesktopApp()
    app.run()
