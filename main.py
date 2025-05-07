from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder
from kivy.metrics import dp

# Define the UI using Kivy language
Builder.load_string('''
<CalculatorButton@Button>:
    font_size: '20sp'
    background_normal: ''
    background_color: app.get_color(self.text)
    color: [1, 1, 1, 1] if self.background_color[0:3] == [1, 0.584, 0] else [0, 0, 0, 1]
    
<CalculatorUI>:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)
    
    # Display area
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: dp(100)
        padding: dp(10)
        canvas.before:
            Color:
                rgba: 0.973, 0.973, 0.973, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            id: expression_label
            text: root.total_expression
            font_size: '16sp'
            halign: 'right'
            color: 0.5, 0.5, 0.5, 1
            size_hint_y: 0.4
            text_size: self.width, None
            
        Label:
            id: result_label
            text: root.current_expression
            font_size: '30sp'
            halign: 'right'
            size_hint_y: 0.6
            text_size: self.width, None
            bold: True
    
    # Buttons area
    GridLayout:
        cols: 4
        spacing: dp(2)
        size_hint_y: 0.5
        
        CalculatorButton:
            text: 'C'
            on_press: root.button_click('C')
            
        CalculatorButton:
            text: '⌫'
            on_press: root.button_click('⌫')
            
        CalculatorButton:
            text: ''  # Empty button
            background_color: 0.9, 0.9, 0.9, 1
            
        CalculatorButton:
            text: '÷'
            on_press: root.button_click('÷')
            
        CalculatorButton:
            text: '7'
            on_press: root.button_click('7')
            
        CalculatorButton:
            text: '8'
            on_press: root.button_click('8')
            
        CalculatorButton:
            text: '9'
            on_press: root.button_click('9')
            
        CalculatorButton:
            text: '×'
            on_press: root.button_click('×')
            
        CalculatorButton:
            text: '4'
            on_press: root.button_click('4')
            
        CalculatorButton:
            text: '5'
            on_press: root.button_click('5')
            
        CalculatorButton:
            text: '6'
            on_press: root.button_click('6')
            
        CalculatorButton:
            text: '-'
            on_press: root.button_click('-')
            
        CalculatorButton:
            text: '1'
            on_press: root.button_click('1')
            
        CalculatorButton:
            text: '2'
            on_press: root.button_click('2')
            
        CalculatorButton:
            text: '3'
            on_press: root.button_click('3')
            
        CalculatorButton:
            text: '+'
            on_press: root.button_click('+')
            
        CalculatorButton:
            text: '0'
            on_press: root.button_click('0')
            size_hint_x: 2
            
        CalculatorButton:
            text: '.'
            on_press: root.button_click('.')
            
        CalculatorButton:
            text: '='
            on_press: root.button_click('=')
    
    # History area
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.3
        
        Label:
            text: 'Calculation History'
            size_hint_y: None
            height: dp(30)
            halign: 'left'
            text_size: self.width, None
            
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            
            Label:
                id: history_label
                text: root.history_text
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
                halign: 'left'
                valign: 'top'
                padding: dp(5), dp(5)
''')

class CalculatorUI(BoxLayout):
    current_expression = StringProperty("")
    total_expression = StringProperty("")
    history_text = StringProperty("")
    history = ListProperty([])
    is_result_displayed = False
    
    def button_click(self, button_text):
        if button_text == "=":
            self.calculate()
        elif button_text == "C":
            self.clear()
        elif button_text == "⌫":
            self.backspace()
        elif button_text in ["×", "÷", "+", "-"]:
            self.append_operator(button_text)
        else:
            self.append_digit(button_text)
        
        # Update the display
        self.update_display()
    
    def append_digit(self, digit):
        # If a result is currently displayed and we're entering a new digit, 
        # clear the display first
        if self.is_result_displayed:
            self.current_expression = ""
            self.is_result_displayed = False
        
        if digit == "." and "." in self.current_expression:
            return
        
        self.current_expression += digit
        
    def append_operator(self, operator):
        # Reset the result flag since we're starting a new operation
        self.is_result_displayed = False
        
        if not self.current_expression and not self.total_expression:
            return
            
        if not self.current_expression:
            # Replace the last operator
            self.total_expression = self.total_expression[:-1] + operator
            return
            
        if self.total_expression:
            self.calculate(update_history=False)
            
        # Standardize operators
        op_map = {"×": "*", "÷": "/"}
        self.total_expression += self.current_expression + (op_map.get(operator, operator))
        self.current_expression = ""
    
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.is_result_displayed = False
    
    def calculate(self, update_history=True):
        if not self.current_expression and not self.total_expression:
            return
            
        expression = self.total_expression + self.current_expression
        
        # Replace display operators with Python operators
        expression = expression.replace("×", "*").replace("÷", "/")
        
        try:
            # Evaluate the expression
            result = str(eval(expression))
            
            # Add to history
            if update_history:
                history_entry = f"{expression.replace('*', '×').replace('/', '÷')} = {result}"
                self.history.append(history_entry)
                self.update_history_display()
            
            # Update current display
            self.total_expression = ""
            self.current_expression = result
            self.is_result_displayed = True
            
        except ZeroDivisionError:
            self.current_expression = "Error: Division by zero"
            
        except Exception as e:
            self.current_expression = "Error"
            print(f"Calculation error: {str(e)}")
    
    def update_display(self):
        # KV binding will automatically update the UI
        pass
    
    def update_history_display(self):
        # Only show the last 10 history entries
        recent_history = self.history[-10:] if len(self.history) > 10 else self.history
        self.history_text = "\n".join(recent_history)
    
    def backspace(self):
        # If we're removing from a result, start fresh instead
        if self.is_result_displayed:
            self.current_expression = ""
            self.is_result_displayed = False
        elif self.current_expression:
            self.current_expression = self.current_expression[:-1]

class CalculatorApp(App):
    def build(self):
        self.title = "Calculator"
        return CalculatorUI()
    
    def get_color(self, text):
        # Return colors based on button type
        if text in ["×", "÷", "+", "-", "=", "C", "⌫"]:
            return [1, 0.584, 0, 1]  # #FF9500
        elif text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            return [0.878, 0.878, 0.878, 1]  # #E0E0E0
        else:
            return [0.9, 0.9, 0.9, 1]  # Empty button or others

    def on_start(self):
        # Set up keyboard input
        Window.bind(on_key_down=self.on_keyboard_down)
    
    def on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        # Map keyboard input to calculator buttons
        if text.isdigit() or text == ".":
            self.root.button_click(text)
        elif text == "+" or text == "-":
            self.root.button_click(text)
        elif text == "*":
            self.root.button_click("×")
        elif text == "/":
            self.root.button_click("÷")
        elif keycode == 13:  # Enter key
            self.root.button_click("=")
        elif keycode == 8:  # Backspace key
            self.root.button_click("⌫")
        elif keycode == 27:  # Escape key
            self.root.button_click("C")
        return True

if __name__ == "__main__":
    CalculatorApp().run()
