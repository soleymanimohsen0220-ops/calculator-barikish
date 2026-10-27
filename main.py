"""
Calculator Barikish — Built with Kivy
=====================================

Four basic operations: + − × ÷
- Dark/Light theme toggle
- English digits
- Circular "=" button
- Mobile-friendly layout (responsive on phone, 9:16 preview on desktop)
"""

import math
import re
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.metrics import dp


# ============================================================
#  Mobile-friendly dimensions (desktop preview only)
#  On a real phone these are ignored and the app goes full-screen.
# ============================================================
# A typical Android phone portrait size used for desktop preview.
# 9:16 aspect ratio — looks like a phone on desktop.
MOBILE_PREVIEW_WIDTH = 393   # ≈ Pixel 6 / Galaxy S22 logical width
MOBILE_PREVIEW_HEIGHT = 851  # 9:16-ish portrait


# ============================================================
#  Theme palette
# ============================================================
THEMES = {
    'dark': {
        'bg':        (0.00, 0.00, 0.00, 1),
        'num':       (0.13, 0.13, 0.14, 1),
        'num_press': (0.20, 0.20, 0.22, 1),
        'op':        (1.00, 0.58, 0.00, 1),
        'op_press':  (0.85, 0.48, 0.00, 1),
        'func':      (0.18, 0.18, 0.20, 1),
        'func_press':(0.28, 0.28, 0.30, 1),
        'text':      (1, 1, 1, 1),
        'dim':       (0.55, 0.55, 0.55, 1),
        'toggle':    (0.18, 0.18, 0.20, 1),
    },
    'light': {
        'bg':        (0.95, 0.95, 0.97, 1),
        'num':       (1.00, 1.00, 1.00, 1),
        'num_press': (0.90, 0.90, 0.92, 1),
        'op':        (1.00, 0.58, 0.00, 1),
        'op_press':  (0.85, 0.48, 0.00, 1),
        'func':      (0.85, 0.85, 0.88, 1),
        'func_press':(0.75, 0.75, 0.78, 1),
        'text':      (0.05, 0.05, 0.08, 1),
        'dim':       (0.45, 0.45, 0.48, 1),
        'toggle':    (0.85, 0.85, 0.88, 1),
    },
}


def _is_mobile():
    """Detect whether we're running on Android/iOS (via Buildozer)."""
    return 'ANDROID_PRIVATE_STORAGE' in os.environ or \
           'ANDROID_ARGUMENT' in os.environ or \
           os.environ.get('KIVY_BUILD', '').lower() in ('android', 'ios')


# ============================================================
#  Custom button with rounded corners or circular shape
# ============================================================
class CalcButton(Button):
    """Calculator button.
    kind: 'number' | 'operator' | 'function' | 'toggle'
    The '=' button is drawn as a circle.
    """

    def __init__(self, text, kind='number', callback=None, app=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = '26sp'
        self.bold = False
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.border = (0, 0, 0, 0)
        self._kind = kind
        self._callback = callback
        self._app = app
        self._circular = (text == '=')
        self._pressed = False
        self.bind(pos=self._redraw, size=self._redraw, state=self._on_state)
        self._redraw()

    def _get_theme(self):
        if self._app is not None:
            return THEMES[self._app.theme]
        return THEMES['dark']

    def _on_state(self, inst, state):
        self._pressed = (state == 'down')
        self._redraw()

    def _redraw(self, *args):
        self.canvas.before.clear()
        t = self._get_theme()

        # Text color
        if self._kind in ('operator', 'function'):
            self.color = (1, 1, 1, 1)
        else:
            self.color = t['text']

        radius = [dp(28)]
        with self.canvas.before:
            if self._circular:
                Color(*(t['op_press'] if self._pressed else t['op']))
                d = min(self.width, self.height)
                Ellipse(
                    pos=(self.center_x - d / 2, self.center_y - d / 2),
                    size=(d, d)
                )
                self.color = (1, 1, 1, 1)
            elif self._kind == 'operator':
                Color(*(t['op_press'] if self._pressed else t['op']))
                RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
            elif self._kind == 'function':
                Color(*(t['func_press'] if self._pressed else t['func']))
                RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
            elif self._kind == 'toggle':
                Color(*(t['func_press'] if self._pressed else t['toggle']))
                RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
            else:
                Color(*(t['num_press'] if self._pressed else t['num']))
                RoundedRectangle(pos=self.pos, size=self.size, radius=radius)


# ============================================================
#  Main app
# ============================================================
class CalculatorBarikishApp(App):
    """Calculator Barikish — Kivy app, mobile-ready."""

    def build(self):
        # ----- internal state -----
        self.expr = ''
        self.result = None
        self.error = False
        self.just_evaluated = False
        self.theme = 'dark'
        self._buttons = []

        # ----- desktop preview size (mobile portrait 9:16) -----
        # On a real phone the OS forces full-screen, so this is ignored.
        if not _is_mobile():
            try:
                Window.size = (MOBILE_PREVIEW_WIDTH, MOBILE_PREVIEW_HEIGHT)
            except Exception:
                pass

        self._apply_window_color()

        root = BoxLayout(orientation='vertical', padding=0, spacing=0)
        root.add_widget(self._build_top_bar())
        root.add_widget(self._build_display())
        root.add_widget(self._build_buttons())
        return root

    def _apply_window_color(self):
        try:
            Window.clearcolor = THEMES[self.theme]['bg']
        except Exception:
            pass

    def _th(self, key):
        return THEMES[self.theme][key]

    # ---------- top bar (title + theme toggle) ----------
    def _build_top_bar(self):
        bar = BoxLayout(orientation='horizontal', size_hint_y=None,
                        height=dp(50), padding=[dp(16), dp(8)])
        self.title_label = Label(text='Barikish', font_size='18sp',
                                 color=self._th('dim'),
                                 halign='left', valign='middle')
        self.title_label.bind(size=self._update_text_size)

        self.theme_btn = CalcButton('🌙', kind='toggle',
                                    callback=self.toggle_theme, app=self)
        self.theme_btn.font_size = '22sp'
        self.theme_btn.size_hint_x = None
        self.theme_btn.width = dp(50)
        self.theme_btn.height = dp(40)

        bar.add_widget(self.title_label)
        bar.add_widget(Widget())
        bar.add_widget(self.theme_btn)
        return bar

    # ---------- display ----------
    def _build_display(self):
        box = BoxLayout(orientation='vertical',
                        padding=[dp(24), dp(8), dp(24), dp(20)], spacing=4)
        self.history_label = Label(text='', font_size='18sp',
                                   color=self._th('dim'),
                                   halign='right', valign='middle',
                                   size_hint_y=None, height=dp(36))
        self.history_label.bind(size=self._update_text_size)
        self.display_label = Label(text='0', font_size='58sp',
                                   color=self._th('text'),
                                   halign='right', valign='middle')
        self.display_label.bind(size=self._update_text_size)
        box.add_widget(Widget())
        box.add_widget(self.history_label)
        box.add_widget(self.display_label)
        return box

    # ---------- buttons ----------
    def _build_buttons(self):
        grid = GridLayout(cols=4, spacing=dp(8), padding=[dp(12), dp(4), dp(12), dp(18)],
                           size_hint_y=None)
        grid.bind(minimum_height=lambda inst, val: setattr(grid, 'height', val))
        buttons = [
            ('AC',  'function'), ('⌫',  'function'), ('%',  'operator'), ('÷', 'operator'),
            ('7',   'number'),    ('8',  'number'),    ('9',  'number'),    ('×', 'operator'),
            ('4',   'number'),    ('5',  'number'),    ('6',  'number'),    ('−', 'operator'),
            ('1',   'number'),    ('2',  'number'),    ('3',  'number'),    ('+', 'operator'),
            ('( )', 'function'),  ('0',  'number'),    ('.',  'number'),    ('=', 'operator'),
        ]
        for label, kind in buttons:
            btn = CalcButton(label, kind=kind, callback=self.on_button, app=self)
            btn.size_hint_y = None
            btn.height = dp(76)
            self._buttons.append(btn)
            grid.add_widget(btn)
        return grid

    def _update_text_size(self, inst, val):
        inst.text_size = (val[0], val[1])

    # ---------- theme toggle ----------
    def toggle_theme(self, *args):
        self.theme = 'light' if self.theme == 'dark' else 'dark'
        self.theme_btn.text = '☀' if self.theme == 'light' else '🌙'
        self._apply_window_color()
        self.title_label.color = self._th('dim')
        self.history_label.color = self._th('dim')
        self.display_label.color = self._th('text')
        for btn in self._buttons:
            btn._redraw()
        self.theme_btn._redraw()

    # ============================================================
    #  Button handler
    # ============================================================
    def on_button(self, label):
        if label == 'AC':
            self.reset_all()
        elif label == '⌫':
            self.backspace()
        elif label == '=':
            self.evaluate()
        elif label == '( )':
            self.toggle_paren()
        elif label == '%':
            self.apply_percent()
        elif label in ('+', '−', '×', '÷'):
            self.add_operator(label)
        elif label == '.':
            self.input_dot()
        else:
            self.input_digit(label)
        self.refresh_display()

    # ============================================================
    #  Calculation logic
    # ============================================================
    def reset_all(self):
        self.expr = ''
        self.result = None
        self.error = False
        self.just_evaluated = False

    def input_digit(self, d):
        if self.just_evaluated or self.error:
            self.reset_all()
        self.expr += d

    def input_dot(self):
        if self.just_evaluated or self.error:
            self.reset_all()
        last_num = re.search(r'[\d.]*$', self.expr)
        if last_num:
            if '.' not in last_num.group():
                if not last_num.group():
                    self.expr += '0.'
                else:
                    self.expr += '.'

    def add_operator(self, op_label):
        py_op = {'+': '+', '−': '-', '×': '*', '÷': '/'}[op_label]
        if self.error:
            self.reset_all()
        if self.just_evaluated and self.result is not None:
            self.expr = self.format_number(self.result)
            self.just_evaluated = False
            self.result = None
        if self.expr and self.expr[-1] in '+-*/':
            self.expr = self.expr[:-1] + py_op
        elif self.expr:
            self.expr += py_op
        else:
            if op_label == '−':
                self.expr = '-'

    def toggle_paren(self):
        if self.just_evaluated or self.error:
            self.reset_all()
        open_count = self.expr.count('(') - self.expr.count(')')
        if open_count > 0 and self.expr and (
            self.expr[-1].isdigit() or self.expr[-1] == '.' or self.expr[-1] == ')'
        ):
            self.expr += ')'
        elif not self.expr or self.expr[-1] in '+-*/(':
            self.expr += '('
        else:
            self.expr += '*('

    def apply_percent(self):
        if self.error:
            self.reset_all()
            return
        if self.just_evaluated and self.result is not None:
            val = self.result
            self.expr = self.format_number(val / 100.0)
            self.result = val / 100.0
            return
        last_num_match = re.search(r'[\d.]+$', self.expr)
        if not last_num_match:
            return
        try:
            val = float(last_num_match.group())
            self.expr = self.expr[:last_num_match.start()] + self.format_number(val / 100.0)
        except Exception:
            self.error = True

    def backspace(self):
        if self.error:
            self.reset_all()
            return
        if self.just_evaluated:
            self.reset_all()
            return
        if self.expr:
            self.expr = self.expr[:-1]

    def evaluate(self):
        if not self.expr:
            return
        try:
            safe = re.sub(r'[^0-9+\-*/().\s]', '', self.expr)
            if not safe:
                return
            result = eval(safe, {'__builtins__': {}}, {'math': math})
            if isinstance(result, float) and result == int(result):
                result = int(result)
            self.result = result
            self.just_evaluated = True
        except ZeroDivisionError:
            self.error = True
        except Exception:
            self.error = True

    def format_number(self, value):
        if isinstance(value, float):
            if value == int(value):
                return str(int(value))
            return f"{value:.8f}".rstrip('0').rstrip('.')
        return str(value)

    def _format_expr_for_display(self, expr):
        out = expr.replace('*', '×').replace('-', '−').replace('/', '÷')
        return out

    def refresh_display(self):
        if self.error:
            self.display_label.text = 'Error'
            self.history_label.text = ''
            return
        if self.just_evaluated and self.result is not None:
            self.display_label.text = self.format_number(self.result)
            self.history_label.text = self._format_expr_for_display(self.expr) + ' ='
        elif not self.expr:
            self.display_label.text = '0'
            self.history_label.text = ''
        else:
            last_num = re.search(r'[\d.]+$', self.expr)
            if last_num:
                self.display_label.text = last_num.group()
            else:
                nums = re.findall(r'[\d.]+', self.expr)
                self.display_label.text = nums[-1] if nums else '0'
            if re.search(r'[+\-*/]', self.expr) or '(' in self.expr:
                self.history_label.text = self._format_expr_for_display(self.expr)
            else:
                self.history_label.text = ''


if __name__ == '__main__':
    CalculatorBarikishApp().run()
