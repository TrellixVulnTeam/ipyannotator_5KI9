# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_navi_widget.ipynb (unless otherwise specified).

__all__ = ['Navi']

# Internal Cell
from ipywidgets import Button, IntSlider, HBox, Layout
import warnings

# Internal Cell

class NaviGUI(HBox):
    def __init__(self, max_im_number: int = 0):
        self._im_number_slider = IntSlider(
            min=0,
            max=max_im_number,
            value=0,
            description='Image Nr.'
        )

        self._prev_btn = Button(description='< Previous',
                               layout=Layout(width='auto'))

        self._next_btn = Button(description='Next >',
                               layout=Layout(width='auto'))

        super().__init__(children=[self._prev_btn, self._im_number_slider, self._next_btn],
                         layout=Layout(display='flex', flex_flow='row wrap', align_items='center'))

# Internal Cell

class NaviLogic:
    """
    Acts like an intermediator between GUI and its interactions
    """
    def __init__(self, gui: NaviGUI):
        self._gui = gui

    def slider_updated(self, change: dict):
        self._gui._index = change['new']
        self.set_slider_value(change['new'])

    def set_slider_value(self, index: int):
        self._gui._im_number_slider.value = index

    def set_slider_max(self, max_im_number: int):
        self._gui._im_number_slider.max = max_im_number

    def _increment_state_index(self, index: int):
        max_im_number = self._gui._max_im_num
        safe_index = (self._gui._index + index) % max_im_number
        self._gui._index = (safe_index + max_im_number) % max_im_number
        self.set_slider_value(self._gui._index)

    def check_im_num(self, max_im_number: int):
        if not hasattr(self._gui, '_im_number_slider'):
            return
        self._gui._im_number_slider.max = max_im_number-1


# Cell

class Navi(NaviGUI):
    """
    Represents simple navigation module with slider.

    navi_callable: callable
        A callback that runs after every navigation
        change. The callback should have, as a
        parameter the navi's index.
    """
    def __init__(self, max_im_num: int = 1, navi_callable: callable = None):
        super().__init__(max_im_num)
        self._max_im_num = max_im_num
        self.navi_callable = navi_callable
        self._index = 0

        self.model = NaviLogic(gui=self)

        self._listen_next_click()
        self._listen_prev_click()
        self._listen_slider_changes()

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        self.model.set_slider_value(value)
        self._index = value
        self._external_call()

    @property
    def max_im_num(self) -> int:
        return self._max_im_num

    @max_im_num.setter
    def max_im_num(self, value: int):
        self.model.set_slider_max(value-1)
        self._max_im_num = value

    def _next_clicked(self, *args):
        self.model._increment_state_index(1)

    def _slider_updated(self, value: dict):
        self.model.slider_updated(value)
        self._external_call()

    def _prev_clicked(self, *args):
        self.model._increment_state_index(-1)

    def _listen_slider_changes(self):
        self._im_number_slider.observe(
            self._slider_updated, names='value'
        )

    def _listen_next_click(self):
        self._next_btn.on_click(self._next_clicked)

    def _listen_prev_click(self):
        self._prev_btn.on_click(self._prev_clicked)

    def _external_call(self):
        if self.navi_callable:
            self.navi_callable(self._index)
        else:
            warnings.warn(
                "Navi callable was not defined." +
                "The navigation will not trigger any action!"
            )