# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_navi_widget.ipynb (unless otherwise specified).

__all__ = ['Navi']

# Internal Cell
from ipywidgets import (AppLayout, Button, IntSlider,
                        HBox, Output,
                        Layout, Label)
from traitlets import Int, observe, link, HasTraits

# Internal Cell

class NaviGUI(HBox):
    max_im_number = Int(0)

    def __init__(self):
        self._im_number_slider = IntSlider(min=0, max=self.max_im_number-1,
                                           value=0, description='Image Nr.')

        self._prev_btn = Button(description='< Previous',
                               layout=Layout(width='auto'))

        self._next_btn = Button(description='Next >',
                               layout=Layout(width='auto'))

        super().__init__(children=[self._prev_btn, self._im_number_slider, self._next_btn],
                         layout=Layout(display='flex', flex_flow='row wrap', align_items='center'))

    @observe('max_im_number')
    def check_im_num(self, change):
        if not hasattr(self, '_im_number_slider'):
            return
        self._im_number_slider.max = change['new']-1

# Internal Cell

class NaviLogic(HasTraits):
    index = Int(0)
    max_im_number = Int(0)

    def __init__(self):
        super().__init__()

    def _increment_index(self, change):
        self.index = (((self.index + change) % self.max_im_number) + self.max_im_number) % self.max_im_number


# Cell

class Navi(NaviGUI):
    """
    Represents simple navigation module with slider.

    """
    def __init__(self, max_im_number=1):
        self.max_im_number = max_im_number

        super().__init__()

        self.model = NaviLogic()

        self._prev_btn.on_click(lambda c: self.model._increment_index(-1))
        self._next_btn.on_click(lambda c: self.model._increment_index(1))

        # link slider value to button increment logic
        link((self._im_number_slider, 'value'), (self.model, 'index'))
        link((self, 'max_im_number'), (self.model, 'max_im_number'))