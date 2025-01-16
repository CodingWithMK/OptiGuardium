import tkinter
import keyboard

class KeyboardBlocker:
    def __init__(self, parent_window):

        self.parent_window = parent_window

        self.keyboard_block_var = tkinter.BooleanVar(value=False)

    def toggle_keyboard_input(self):
        for i in range(150):
            if self.keyboard_block_var.get():
                keyboard.block_key(i)
            else:
                keyboard.unblock_key(i)
    
    def get_block_var(self):
        return self.keyboard_block_var
            

if __name__ == "__main__":
    KeyboardBlocker()