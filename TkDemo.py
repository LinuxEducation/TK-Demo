from tkinter import *


class MultiFrame(Frame):
    def __init__(self, app, rgb, col, row):
        Frame.__init__(self, bg=rgb)

        self.config(width=300, height=300)

        self.grid(column=col,row=row,
                  padx=(5,0),pady=(5,0),
                  ipadx=5,ipady=5,
                  sticky=NSEW)
        #self.grid_propagate(0)


class MovingLabel(Label):
    def __init__(self, container):
        Label.__init__(self, container)
        self.config(text='Label', font=('Havletica, 22'), relief=SOLID, borderwidth=1.5)
        self.pack(ipadx=10, ipady=10, padx=10, pady=10)

    def set_position(self, position):

        options = {'padx':'10', 'pady':'10'}

        if position[0] == 'n':
            self.pack(side=TOP, anchor=position, **options)
        if position[0] == 's':
            self.pack(side=BOTTOM, anchor=position, **options)
        if position[0] == 'w':
            self.pack(side=LEFT, anchor=position, **options)
        if position[0] == 'e':
            self.pack(side=RIGHT, anchor=position, **options)
        if position == 'center':
            self.pack(expand=True, anchor=CENTER, **options)

        self.config(text=position)

    def set_color(self, color):
        self.config(bg=color, text=color)


class MultiWidget():

    instance = {}

    def __init__(self, container, name):
        MultiWidget.instance[str(container)] = name

        options = {'font': ['Havletica', 18, 'bold'],
                   'width':'8',
                   'height':'4',
                   'relief': SOLID,
                   'borderwidth': 1,
                   'highlightbackground':'RoyalBlue3'}

        geometry = {'padx':[10,0], 'pady':[10,0]}
    
        if name == 'compass':
            compass = {0:['NW','N','NE'],
                       1:['W','CENTER','E'],
                       2:['SW','S','SE']}

            self.full_name = {'NW': ['NW', 'North-West' ],
                              'N':  ['N', 'North'],
                              'NE': ['NE', 'North-East'],
                              'W':  ['W', 'West'],
                              'E':  ['E','East'],
                              'SW': ['SW','South-West'],
                              'S':  ['S','South'],
                              'SE': ['SE','South-East'],
                              'CENTER': ['C', 'CENTER']}
           
            #_buttons = {}
            for x in range(3):
                for y in range(3):
                    Button(container, bg='gainsboro', text=compass[x][y], **options).grid(row=x,column=y, **geometry)
                    #_buttons[compass[x][y]] = bt

        if name == 'color':
            color = {0:['red','orange','yellow'],
                     1:['green','blue','navy'],
                     2:['purple','brown','gray']}
            
            for x in range(3):
                for y in range(3):
                    Button(container, text=color[x][y], bg=color[x][y], **options).grid(row=x,column=y, **geometry)


class Terminal(Text):
    def __init__(self, container):
        Text.__init__(self, container)
        self.config(width=0,height=0, bg='black', fg='white', font=('Havletica', 18), bd=0, highlightthickness=0)
        self.pack(side=LEFT, fill=BOTH, expand=True, padx=15, pady=10)
        self.insert(END, 'Tk _command:')
        self._font = 18
        self._trans = 10
        self.flag = False

    def insert_options(self, string):
        self.insert(END, string)

    def get_select_string(self):
        try:
            self.insert_info(self.get('sel.first', 'sel.last'))
        except:
            self.delete(0.0, END)
            self.insert(0.0, 'Najpierw zaznacz parametr z listy!')

    def insert_info(self, select_string):
        flag = False

        parameters = {'background|bg': 'kolor tła ramki, etykiety lub przycisku.',
                      'foreground|fg': 'kolor tekstu lub elementów wewnętrznych widgetu',
                      'command': "przywiązanie funkcj lub metody do widgetu: <<button>>\n-self.bt = Button(text='Quit', command=quit())",
                      'ipadx|ipady': "margines wewnątrz obiektu.\n-ipadx=[10,0], dic = {'ipady':[0,10]}",
                      'padx|pady': "margines na zewnątrz obiektu.\n-padx=[10,0], dic = {'pady':[0,10]}",
                      'borderwidth|bd': 'szerokość obramowania w okół widgetu',
                      'relief': 'trójwymiarowy efekt widgetu: <<button>>\n-typ: FLAT, RAISED, SUNKEN, GROOVE, RIDGE',
                      'activebackground': 'Kolor przycisku po najechaniu myszy',
                      'activeforeground': 'Kolor tekstu po najechaniu myszy',
                      'anchor': 'położenie obiektu zgodnie z parametrami:\n NW, N, NE, W, E, SW, S, SE',
                      'disabledforeground': 'Kolor tekstu przycisku w pozycji: Disabled\n configure(state=DISABLED, state=NORMAL)'

                      }

        for key in parameters.keys():
            for k in key.split('|'):
                if k == select_string:
                    self.delete(0.0, END)
                    self.insert(END, f'{k:15}\n' + '-'+parameters[key])
                    flag = True

        if not flag:
            self.delete(0.0, END)
            self.insert(0.0, 'Nie znaleziono tłumaczenia w bazie.')

    def font_up(self):
        self._font += 5
        self.config(font=('Havletica', self._font))

    def font_down(self):
        self._font -= 5
        self.config(font=('Havletica', self._font))

    def empty(self):
        self.delete(0.0, END)
        self.insert(0.0, 'Usługa chwilowo niedostępna')

    def trans(self):
        if self._trans > 2:
            self._trans -= 2
        app.attributes('-alpha', f'0.{self._trans}')


class TerminalWidget:
    def __init__(self, container):

        options = {'font':                  ['Havletica', 18, 'bold'],
                   'relief':                SOLID,
                   'borderwidth':           1,
                   'highlightbackground':   'orange',}

        geometry = {'padx':[0,8], 'pady':[0,8]}

        self._buttons = {}
        for n in ['trans','+','-','i']:
            bt = Button(container, text=n, **options)
            bt.pack(side=RIGHT, anchor=SE, **geometry)
            self._buttons[n] = bt

    def _enter(self, mouse):
        char = mouse.widget.cget('text')
        self._buttons[char].config(font=('Havletica', 22))

    def _leave(self, mouse):
        char = mouse.widget.cget('text')
        self._buttons[char].config(font=('Havletica', 18))


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('TkDemo1')
        self.geometry('1350x895')
        self.run()

    def run(self):      
        #Frame Widget
        terminal_frame = MultiFrame(self, 'black', 0,0)
        color_frame = MultiFrame(self, '#eff0f1', 1,0)
        label_frame = MultiFrame(self, 'green', 0,1)
        button_frame = MultiFrame(self, '#eff0f1', 1,1)
        
        #Terminal
        self.terminal = Terminal(terminal_frame)
        self.terminal_widget = TerminalWidget(terminal_frame)
        #commands
        self.terminal_widget._buttons['i']['command'] = self.terminal.get_select_string
        self.terminal_widget._buttons['-']['command'] = self.terminal.font_down
        self.terminal_widget._buttons['+']['command'] = self.terminal.font_up
        self.terminal_widget._buttons['trans']['command'] = self.terminal.trans
    
        #events
        for key in self.terminal_widget._buttons.keys():
            self.terminal_widget._buttons[key].bind('<Enter>', lambda mouse: self.terminal_widget._enter(mouse))
            self.terminal_widget._buttons[key].bind('<Leave>', lambda mouse: self.terminal_widget._leave(mouse))

        #gui
        self.colors = MultiWidget(color_frame, 'color')
        self.compas = MultiWidget(button_frame, 'compass')
        self.label = MovingLabel(label_frame)

        #footer
        source = MultiFrame(self, '#eff0f1', 0,3)
        Label(source, text='made in poland | created to create'+70*' ', font=('Havletica', 18, 'bold')).pack(side=LEFT, padx=5)
  
        
    def mouse_click(self, mouse):

        def get_options():
            i = 1
            self.terminal.delete(1.0, END)
            for x in mouse.widget.keys():
                self.terminal.insert_options(f'{i:2}.  {x}:  {mouse.widget[x]}' + '\n')
                i += 1

        for key in MultiWidget.instance.keys():
            if key in str(mouse.widget) and '.!button' in str(mouse.widget):
                if 'compass' in MultiWidget.instance[key]:
                    self.label.set_position(self.before_enter.lower())
                    get_options()
                    
                if 'color' in MultiWidget.instance[key]:
                    self.label.set_color(mouse.widget.cget('bg').lower())
                    get_options()

    
    def mouse_enter(self, mouse):
        for key in MultiWidget.instance.keys():
            if key in str(mouse.widget) and '.!button' in str(mouse.widget):
                        
                self.before_enter = mouse.widget.cget('text')           
                if 'compass' in MultiWidget.instance[key]:
                    mouse.widget['text'] = self.compas.full_name[mouse.widget.cget('text')][-1]

    def mouse_leave(self, mouse):
        for key in MultiWidget.instance.keys():
            if key in str(mouse.widget) and '.!button' in str(mouse.widget):
                mouse.widget['text'] = self.before_enter
                

app = App()
app.bind('<Button-1>', app.mouse_click)
app.bind('<Enter>', app.mouse_enter)
app.bind('<Leave>', app.mouse_leave)
app.mainloop()
