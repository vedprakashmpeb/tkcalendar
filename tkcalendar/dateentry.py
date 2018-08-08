# -*- coding: utf-8 -*-
"""
tkcalendar - Calendar and DateEntry widgets for Tkinter
Copyright 2017-2018 Juliette Monsel <j_4321@protonmail.com>
with contributions from:
  - Neal Probert (https://github.com/nprobert)
  - arahorn28 (https://github.com/arahorn28)

tkcalendar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkcalendar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


DateEntry widget
"""


from sys import platform
import locale
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from tkcalendar.calendar_ import Calendar


class DateEntry(ttk.Entry):
    """Date selection entry with drop-down calendar."""

    entry_kw = {'exportselection': 1,
                'invalidcommand': '',
                'justify': 'left',
                'show': '',
                'cursor': 'xterm',
                'style': '',
                'state': 'normal',
                'takefocus': 'ttk::takefocus',
                'textvariable': '',
                'validate': 'none',
                'validatecommand': '',
                'width': 12,
                'xscrollcommand': ''}

    def __init__(self, master=None, **kw):
        """
        Create an entry with a drop-down calendar to select a date.

        When the entry looses focus, if the user input is not a valid date,
        the entry content is reset to the last valid date.

        KEYWORDS OPTIONS

            usual ttk.Entry options and Calendar options

        VIRTUAL EVENTS

            A <<DateEntrySelected>> event is generated each time
            the user selects a date.
        """
        # sort keywords between entry options and calendar options
        kw['selectmode'] = 'day'
        entry_kw = {}

        for key in self.entry_kw:
            entry_kw[key] = kw.pop(key, self.entry_kw[key])
        entry_kw['font'] = kw.get('font', None)

        # set locale to have the right date format
        loc = kw.get('locale', '')
        locale.setlocale(locale.LC_ALL, loc)

        ttk.Entry.__init__(self, master, **entry_kw)
        # down arrow button bbox (to detect if it was clicked upon)
        self._down_arrow_bbox = [0, 0, 0, 0]

        self._determine_bbox_after_id = ''

        # drop-down calendar
        self._top_cal = tk.Toplevel(self)
        self._top_cal.withdraw()
        if platform == "linux":
            self._top_cal.attributes('-type', 'DROPDOWN_MENU')
        self._top_cal.overrideredirect(True)
        self._calendar = Calendar(self._top_cal, **kw)
        self._calendar.pack()

        # style
        self.style = ttk.Style(self)
        self._setup_style()
        self.configure(style='DateEntry')

        # add validation to Entry so that only date in the locale '%x' format
        # are accepted
        validatecmd = self.register(self._validate_date)
        self.configure(validate='focusout',
                       validatecommand=validatecmd)

        # initially selected date
        self._date = self._calendar.selection_get()
        if self._date is None:
            today = self._calendar.date.today()
            year = kw.get('year', today.year)
            month = kw.get('month', today.month)
            day = kw.get('day', today.day)
            try:
                self._date = self._calendar.date(year, month, day)
            except ValueError:
                self._date = today
        self._set_text(self._date.strftime('%x'))

        self._theme_change = True

        # --- bindings
        # reconfigure style if theme changed
        self.bind('<<ThemeChanged>>',
                  lambda e: self.after(10, self._on_theme_change))
        # determine new downarrow button bbox
        self.bind('<Configure>', self._determine_bbox)
        self.bind('<Map>', self._determine_bbox)
        # handle appearence to make the entry behave like a Combobox but with
        # a drop-down calendar instead of a drop-down list
        self.bind('<Leave>', lambda e: self.state(['!active']))
        self.bind('<Motion>', self._on_motion)
        self.bind('<ButtonPress-1>', self._on_b1_press)
        # update entry content when date is selected in the Calendar
        self._calendar.bind('<<CalendarSelected>>', self._select)
        # hide calendar if it looses focus
        self._calendar.bind('<FocusOut>', self._on_focus_out_cal)

    def __getitem__(self, key):
        """Return the resource value for a KEY given as string."""
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def _setup_style(self, event=None):
        """Style configuration."""
        self.style.layout('DateEntry', self.style.layout('TCombobox'))
        fieldbg = self.style.map('TCombobox', 'fieldbackground')
        self.style.map('DateEntry', fieldbackground=fieldbg)
        try:
            self.after_cancel(self._determine_bbox_after_id)
        except ValueError:
            # nothing to cancel
            pass
        self._determine_bbox_after_id = self.after(10, self._determine_bbox)

    def _determine_bbox(self, event=None):
        """Determine downarrow button bbox."""
        try:
            self.after_cancel(self._determine_bbox_after_id)
        except ValueError:
            # nothing to cancel
            pass
        if self.winfo_ismapped():
            self.update_idletasks()
            h = self.winfo_height()
            w = self.winfo_width()
            y = h // 2
            x = 0
            if self.identify(x, y):
                while x < w and 'downarrow' not in self.identify(x, y):
                    x += 1
                if x < w:
                    self._down_arrow_bbox = [x, 0, w, h]
            else:
                self._determine_bbox_after_id = self.after(10, self._determine_bbox)

    def _on_motion(self, event):
        """Set widget state depending on mouse position to mimic Combobox behavior."""
        x, y = event.x, event.y
        x1, y1, x2, y2 = self._down_arrow_bbox
        if 'disabled' not in self.state():
            if x >= x1 and x <= x2 and y >= y1 and y <= y2:
                self.state(['active'])
                self.configure(cursor='arrow')
            else:
                self.state(['!active'])
                if 'readonly' not in self.state():
                    self.configure(cursor='xterm')

    def _on_theme_change(self):
        if self._theme_change:
            self._theme_change = False
            self._setup_style()
            self.after(50, self._set_theme_change)

    def _set_theme_change(self):
        self._theme_change = True

    def _on_b1_press(self, event):
        """Trigger self.drop_down on downarrow button press and set widget state to ['pressed', 'active']."""
        x, y = event.x, event.y
        x1, y1, x2, y2 = self._down_arrow_bbox
        if (('disabled' not in self.state()) and
                x >= x1 and x <= x2 and y >= y1 and y <= y2):
            self.state(['pressed'])
            self.drop_down()

    def _on_focus_out_cal(self, event):
        """Withdraw drop-down calendar when it looses focus."""
        if self.focus_get() is not None:
            if self.focus_get() == self:
                x, y = event.x, event.y
                x1, y1, x2, y2 = self._down_arrow_bbox
                if (type(x) != int or type(y) != int or
                        not (x >= x1 and x <= x2 and y >= y1 and y <= y2)):
                    self._top_cal.withdraw()
                    self.state(['!pressed'])
            else:
                self._top_cal.withdraw()
                self.state(['!pressed'])
        else:
            x, y = self._top_cal.winfo_pointerxy()
            xc = self._top_cal.winfo_rootx()
            yc = self._top_cal.winfo_rooty()
            w = self._top_cal.winfo_width()
            h = self._top_cal.winfo_height()
            if xc <= x <= xc + w and yc <= y <= yc + h:
                # re-focus calendar so that <FocusOut> will be triggered next time
                self._calendar.focus_force()
            else:
                self._top_cal.withdraw()
                self.state(['!pressed'])

    def _validate_date(self):
        """Date entry validation: only dates in locale '%x' format are accepted."""
        try:
            self._date = self._calendar.strptime(self.get(), '%x').date()
            return True
        except ValueError:
            self._set_text(self._date.strftime('%x'))
            return False

    def _select(self, event=None):
        """Display the selected date in the entry and hide the calendar."""
        date = self._calendar.selection_get()
        if date is not None:
            self._set_text(date.strftime('%x'))
            self.event_generate('<<DateEntrySelected>>')
        self._top_cal.withdraw()
        if 'readonly' not in self.state():
            self.focus_set()

    def _set_text(self, txt):
        """Insert text in the entry."""
        if 'readonly' in self.state():
            readonly = True
            self.state(('!readonly',))
        else:
            readonly = False
        self.delete(0, 'end')
        self.insert(0, txt)
        if readonly:
            self.state(('readonly',))

    def destroy(self):
        try:
            self.after_cancel(self._determine_bbox_after_id)
        except ValueError:
            # nothing to cancel
            pass
        ttk.Entry.destroy(self)

    def drop_down(self):
        """Display or withdraw the drop-down calendar depending on its current state."""
        if self._calendar.winfo_ismapped():
            self._top_cal.withdraw()
        else:
            self._validate_date()
            date = self._calendar.strptime(self.get(), '%x')
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            self._top_cal.geometry('+%i+%i' % (x, y))
            self._top_cal.deiconify()
            self._calendar.focus_set()
            self._calendar.selection_set(date.date())

    def state(self, *args):
        """
        Modify or inquire widget state.

        Widget state is returned if statespec is None, otherwise it is
        set according to the statespec flags and then a new state spec
        is returned indicating which flags were changed. statespec is
        expected to be a sequence.
        """
        if args:
            # change cursor depending on state to mimic Combobox behavior
            states = args[0]
            if 'disabled' in states or 'readonly' in states:
                self.configure(cursor='arrow')
            elif '!disabled' in states or '!readonly' in states:
                self.configure(cursor='xterm')
        return ttk.Entry.state(self, *args)

    def keys(self):
        """Return a list of all resource names of this widget."""
        keys = list(self.entry_kw)
        keys.extend(self._calendar.keys())
        return list(set(keys))

    def cget(self, key):
        """Return the resource value for a KEY given as string."""
        if key in self.entry_kw:
            return ttk.Entry.cget(self, key)
        else:
            return self._calendar.cget(key)

    def configure(self, **kw):
        """
        Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method keys.
        """
        entry_kw = {}
        keys = list(kw.keys())
        for key in keys:
            if key in self.entry_kw:
                entry_kw[key] = kw.pop(key)
        font = kw.get('font', None)
        if font is not None:
            entry_kw['font'] = font
        ttk.Entry.configure(self, **entry_kw)
        self._calendar.configure(**kw)

    def config(self, **kw):
        """
        Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method keys.
        """
        self.configure(**kw)

    def set_date(self, date):
        """
        Set the value of the DateEntry to date.

        date can be a datetime.date, a datetime.datetime or a string
        in locale '%x' format.
        """
        try:
            txt = date.strftime('%x')
        except AttributeError:
            txt = str(date)
            try:
                self._calendar.strptime(txt, '%x')
            except Exception as e:
                raise type(e)("%r is not a valid date." % date)
        self._set_text(txt)

    def get_date(self):
        """Return the content of the DateEntry as a datetime.date instance."""
        self._validate_date()
        date = self.get()
        return self._calendar.strptime(date, '%x').date()
