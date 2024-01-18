import npyscreen
from subprocess import Popen, PIPE

class Theme(npyscreen.ThemeManager):
    default_colors = {
    'DEFAULT'     : 'WHITE_BLACK',
    'FORMDEFAULT' : 'WHITE_BLACK',
    'NO_EDIT'     : 'BLUE_BLACK',
    'STANDOUT'    : 'CYAN_BLACK',
    'CURSOR'      : 'WHITE_BLACK',
    'CURSOR_INVERSE': 'BLACK_WHITE',
    'LABEL'       : 'GREEN_BLACK',
    'LABELBOLD'   : 'WHITE_BLACK',
    'CONTROL'     : 'YELLOW_BLACK',
    'IMPORTANT'   : 'GREEN_BLACK',
    'SAFE'        : 'GREEN_BLACK',
    'WARNING'     : 'YELLOW_BLACK',
    'DANGER'      : 'RED_BLACK',
    'CRITICAL'    : 'BLACK_RED',
    'GOOD'        : 'GREEN_BLACK',
    'GOODHL'      : 'GREEN_BLACK',
    'VERYGOOD'    : 'BLACK_GREEN',
    'CAUTION'     : 'YELLOW_BLACK',
    'CAUTIONHL'   : 'BLACK_YELLOW',
    }

    def _define_pairs(self):
        super(Theme, self)._define_pairs()
        # Define your color pairs here
        self._defined_pairs[self._names['DEFAULT']] = (npyscreen.WHITE, npyscreen.BLUE)

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(Theme)
        self.addForm("MAIN", MainForm, name="Academy Management System")


class MainForm(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.TitleText, name="Command:", rely=1, relytext=4)
        self.command_input = self.add(npyscreen.TitleText, name="Enter command:", value="python3 octplex.py", rely=5, relytext=4)
        self.output_area = self.add(npyscreen.MultiLineEdit, editable=False, rely=8)

    def on_ok(self):
        command = self.command_input.value
        result = self.run_command(command)
        self.output_area.value = result
        self.output_area.display()

    def run_command(self, command):
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        output, error = process.communicate()
        result = f"Output:\n{output}\n\nError:\n{error}"
        return result

if __name__ == "__main__":
    MyApp = App().run()
