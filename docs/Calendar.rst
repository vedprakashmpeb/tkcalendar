.. _doc:

Calendar
========

.. currentmodule:: tkcalendar

Class
-----

.. autoclass:: tkcalendar.Calendar
    :show-inheritance:
    :members: calevent_cget, calevent_configure, calevent_create, calevent_lower, calevent_raise, calevent_remove, format_date, get_calevents, get_date, keys, selection_get, selection_set, tag_cget, tag_config, tag_delete, tag_names, get_displayed_month

    .. py:method:: __init__(master=None, **kw)

       Construct a :class:`Calendar` with parent master.

       **Standard Options**

       cursor : str
           cursor to display when the pointer is in the widget

       font : str or Tkinter Font instance
           font of the calendar

       borderwidth : int
           width of the border around the calendar

       state : str
           "normal" or "disabled" (unresponsive widget)

       **Widget-specific Options**

       year : int
          intinitially displayed year, default is current year.

       month : int
          initially displayed month, default is current month.

       day : int
          initially selected day, if month or year is given but not day, no initial selection, otherwise, default is today.

       firstweekday : str
          first day of the week: "monday" or "sunday"

       showweeknumbers : bool
          whether to display week numbers (default is True).

       showothermonthdays : bool
          whether to display the last days of the previous month and the first of the next month  (default is True).

       locale : str
          locale to use, e.g. 'en_US'

       selectmode : str
          "none" or "day" (default): whether the user can change the selected day with a mouse click.

       textvariable : StringVar
          connect the currently selected date to the variable.

       **Style Options**

       background : str
          background color of calendar border and month/year name

       foreground : str
          foreground color of month/year name

       bordercolor : str
          day border color

       headersbackground : str
          background color of day names and week numbers

       headersforeground : str
          foreground color of day names and week numbers

       selectbackground : str
          background color of selected day

       selectforeground : str
          foreground color of selected day

       disabledselectbackground : str
          background color of selected day in disabled state

       disabledselectforeground : str
          foreground color of selected day in disabled state

       normalbackground : str
          background color of normal week days

       normalforeground : str
          foreground color of normal week days

       weekendbackground : str
          background color of week-end days

       weekendforeground : str
          foreground color of week-end days

       othermonthforeground : str
          foreground color of normal week days belonging to the previous/next month

       othermonthbackground : str
          background color of normal week days belonging to the previous/next month

       othermonthweforeground : str
          foreground color of week-end days belonging to the previous/next month

       othermonthwebackground : str
          background color of week-end days belonging to the previous/next month

       disableddaybackground : str
          background color of days in disabled state

       disableddayforeground : str
          foreground color of days in disabled state

       **Tooltip Options (for calevents)**

       tooltipforeground : str
          tooltip text color

       tooltipbackground : str
          tooltip background color

       tooltipalpha : float
          tooltip opacity between 0 and 1

       tooltipdelay : int
          delay in ms before displaying the tooltip

Virtual Events
--------------

* A :obj:`\<\<CalendarSelected\>\>` event is generated each time the user selects a day with the mouse.

* A :obj:`<\<\CalendarMonthChanged\>\>` event is generated each time the user changes the displayed month.

.. _calevent:

Calendar Events
---------------

Special events (e.g. birthdays, ..) can be managed using the
:meth:`calevent_..` methods. The way they are displayed in the calendar is
determined with tags. An id is attributed to each event upon creation
and can be used to edit the event (*ev_id* argument).
