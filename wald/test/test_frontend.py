'''Tests for wald.frontend.'''

from wald.frontend import Frame
import wx


def test_create_frame():
    '''Create a node.'''
    app = wx.App(False)
    frame = Frame()
    assert frame is not None
