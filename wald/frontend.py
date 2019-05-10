'''Frontends for documents.

TODO:

- edit content
- bug: does not save anything, collapse
- move up
- move down
- move left (make sibling of parent)
- move right (make child of sibling)
- copy node (with children)
- copy node (without children)
- cut node (with children)
- paste (as child of current node)
- paste (as root)
- find node (by name)
- find node (by content, full text search)
- find and replace
- find previous
- find next
- allow selecting multiple nodes
- select all
- confirm close without save
- multiple windows, copy & paste across
- undo & redo
- enter full screen
- expand (subtree of current node)
- expand (full tree)
'''

from wald.backend import Document, Node
import wx


class App(wx.App):
    NAME = 'wald'

    def OnInit(self):
        frame = Frame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


class Frame(wx.Frame):
    SIZE = wx.Size(450, 350)

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          App.NAME, wx.DefaultPosition, Frame.SIZE)

        self._window = SplitterWindow(self)
        self.treectrl = self._window.treectrl
        self.SetMenuBar(MenuBar({
            'File': FileMenu(self),
            'Edit': EditMenu(self),
            'Insert': InsertMenu(self),
            'Help': HelpMenu(self)
        }))

        self.Centre()


class MenuBar(wx.MenuBar):
    def __init__(self, menus):
        wx.MenuBar.__init__(self)
        for name, menu in menus.items():
            self.Append(menu, name)


class Menu(wx.Menu):
    def __init__(self, frame):
        wx.Menu.__init__(self)
        self.frame = frame

    def append_item(self, id, text, handler):
        item = self.Append(id, text)
        self.frame.Bind(wx.EVT_MENU, handler, item)


class FileMenu(Menu):
    def __init__(self, frame):
        Menu.__init__(self, frame)
        self.append_item(wx.ID_NEW, 'New\tCtrl+N', self.on_new)
        self.append_item(wx.ID_OPEN, 'Open File...\tCtrl+O', self.on_open)
        self.append_item(wx.ID_SAVE, 'Save File...\tCtrl+S', self.on_save)
        self.append_item(wx.ID_SAVEAS, 'Save File As...\tShift+Ctrl+S', self.on_save_as)

    def on_new(self, event):
        self.frame.treectrl.new_file()

    def on_open(self, event):
        with FileDialog(self.frame, '', '', '', '*.*', wx.FD_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.frame.treectrl.open_file(dialog.GetPath())

    def on_save(self, event):
        if not self.frame.treectrl.filename:
            return self.on_save_as(event)
        self.frame.treectrl.save_file()

    def on_save_as(self, event):
        with FileDialog(self.frame, '', '', '', '*.*',
                        wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.frame.treectrl.save_file_as(dialog.GetPath())


class EditMenu(Menu):
    ID_RENAME = wx.NewId()
    ID_DESELECT = wx.NewId()

    def __init__(self, frame):
        Menu.__init__(self, frame)
        self.append_item(self.ID_RENAME, 'Rename\tCtrl+R', self.on_rename)
        self.append_item(wx.ID_DELETE, 'Delete\tBack', self.on_delete)
        self.append_item(self.ID_DESELECT, 'Deselect All\tShift+Ctrl+A', self.on_deselect)

    def on_rename(self, event):
        self.frame.treectrl.rename_selected()

    def on_delete(self, event):
        self.frame.treectrl.delete_selected()

    def on_deselect(self, event):
        self.frame.treectrl.deselect()


class InsertMenu(Menu):
    ID_INSERT_CHILD = wx.NewId()
    ID_INSERT_SIBLING = wx.NewId()

    def __init__(self, frame):
        Menu.__init__(self, frame)
        self.append_item(self.ID_INSERT_CHILD, 'Insert Child\tCtrl+I', self.on_insert_child)
        self.append_item(self.ID_INSERT_SIBLING, 'Insert Sibling\tCtrl+J', self.on_insert_sibling)

    def on_insert_child(self, event):
        self.frame.treectrl.insert_child()

    def on_insert_sibling(self, event):
        self.frame.treectrl.insert_sibling()


class HelpMenu(Menu):
    def __init__(self, frame):
        Menu.__init__(self, frame)
        self.append_item(wx.ID_ABOUT, 'About', self.on_about)

    def on_about(self, event):
        with MessageDialog(self.frame, 'wald', 'About', wx.OK) as dialog:
            dialog.ShowModal()


class DialogContextManager(object):
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.Destroy()


class MessageDialog(wx.MessageDialog, DialogContextManager):
    pass


class FileDialog(wx.FileDialog, DialogContextManager):
    pass


class SplitterWindow(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, wx.ID_ANY)

        left, right = Panel(self), Panel(self)

        self.textctrl = TextCtrl(right)
        self.treectrl = TreeCtrl(left, self.textctrl)

        left.add_child(self.treectrl)
        right.add_child(self.textctrl)

        self.SplitVertically(left, right)


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

    def add_child(self, child):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(child, 1, wx.EXPAND)
        self.SetSizer(box)


class TreeCtrl(wx.TreeCtrl):
    SIZE = wx.Size(-1, -1)
    STYLE = (
        wx.TR_HIDE_ROOT |
        wx.TR_HAS_BUTTONS |
        wx.TR_EDIT_LABELS)

    def __init__(self, parent, textctrl):
        wx.TreeCtrl.__init__(self, parent,
                             wx.ID_ANY,
                             wx.DefaultPosition,
                             TreeCtrl.SIZE,
                             TreeCtrl.STYLE)

        self.textctrl = textctrl
        self.document = None
        self.filename = None

        self._set_document(Document())

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self._on_sel_changed)
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self._on_sel_changing)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self._on_end_label_edit)

    def _bind_all_events_to_popup(self):
        events = [
            'EVT_TREE_BEGIN_DRAG',
            'EVT_TREE_BEGIN_RDRAG',
            'EVT_TREE_END_DRAG',
            'EVT_TREE_BEGIN_LABEL_EDIT',
            'EVT_TREE_GET_INFO',
            'EVT_TREE_SET_INFO',
            'EVT_TREE_ITEM_ACTIVATED',
            'EVT_TREE_ITEM_COLLAPSED',
            'EVT_TREE_ITEM_COLLAPSING',
            'EVT_TREE_ITEM_EXPANDED',
            'EVT_TREE_ITEM_EXPANDING',
            'EVT_TREE_ITEM_RIGHT_CLICK',
            'EVT_TREE_ITEM_MIDDLE_CLICK',
            'EVT_TREE_SEL_CHANGING',
            'EVT_TREE_ITEM_MENU',
        ]

        def popup(text):
            def handler(event):
                with MessageDialog(self, text, 'Event', wx.OK) as dialog:
                    dialog.ShowModal()
            return handler

        for event in events:
            self.Bind(getattr(wx, event), popup(event))

    def new_file(self):
        document = Document()
        self._set_document(document)
        self.filename = None

    def open_file(self, filename):
        document = Document(filename)
        self._set_document(document)
        self.filename = filename

    def save_file(self):
        self.document.save()

    def save_file_as(self, filename):
        document = self.document.save_as(filename)
        self._set_document(document)
        self.filename = filename

    def insert_child(self):
        parent_item, parent_node = self._get_selected_item_with_node()
        self._create_node('New Node', parent_node, parent_item)

    def insert_sibling(self):
        item, node = self._get_selected_item_with_node()
        parent_item = self.GetItemParent(item) if item else None
        parent_node = node.parent if node else None
        self._create_node('New Node', parent_node, parent_item)

    def rename_selected(self):
        item, node = self._get_selected_item_with_node()
        if node:
            self.EditLabel(item)

    def delete_selected(self):
        item, node = self._get_selected_item_with_node()
        if node:
            self.document.remove(node)
            self.Delete(item)

    def deselect(self):
        self.UnselectAll()
        self.SelectItem(self.GetRootItem())

    def _get_selected_item_with_node(self):
        item = self.GetSelection()
        if item:
            return item, self.GetItemData(item)
        return None, None

    def _clear(self):
        self._submit_textctrl()
        self.DeleteAllItems()
        self.textctrl.SetValue('')

    def _set_document(self, document):
        self._clear()
        self._add_document(document)

    def _add_document(self, document):
        self.document = document
        self.AddRoot('')
        for root in document.roots:
            self._add_node(root)

    def _add_node(self, node, parent=None):
        item = self.AppendItem(parent or self.GetRootItem(), node.name, data=node)
        for child in node.children:
            self._add_node(child, item)
        return item

    def _create_node(self, name, parent_node=None, parent_item=None, **kwargs):
        node = Node(name, parent=parent_node, **kwargs)
        item = self._add_node(node, parent=parent_item)
        self.SelectItem(item)
        self.EnsureVisible(item)
        self.EditLabel(item)

    def _on_sel_changed(self, event):
        item = event.GetItem()
        node = self.GetItemData(item)
        self.textctrl.SetValue(node.content or '')

    def _on_sel_changing(self, event):
        self._submit_textctrl()

    def _on_end_label_edit(self, event):
        item = event.GetItem()
        node = self.GetItemData(item)
        node.name = event.GetLabel()

    def _submit_textctrl(self):
        print ('submit_textctrl. IsModified = "%s"' % ('y' if self.textctrl.IsModified() else 'n'))
        if self.textctrl.IsModified() or True:
            item, node = self._get_selected_item_with_node()
            node.content = self.textctrl.GetValue()
            print ('node.content = "%s"' % self.textctrl.GetValue())


class TextCtrl(wx.TextCtrl):
    SIZE = wx.Size(10, 10)

    def __init__(self, parent, label=''):
        wx.TextCtrl.__init__(self, parent,
                             wx.ID_ANY, label,
                             wx.DefaultPosition,
                             TextCtrl.SIZE,
                             wx.TE_MULTILINE)


def create_example_document():
    document = Document()

    os = Node('Operating Systems', content='An Operating System (OS) is a ...')
    pl = Node('Programming Languages')
    cl = Node('Compiled languages', parent=pl)
    sl = Node('Scripting languages', parent=pl)
    tk = Node('Toolkits')

    document.add(os)
    document.add(pl)
    document.add(tk)
    document.add(cl)
    document.add(sl)

    document.add(Node('Linux', parent=os))
    document.add(Node('FreeBSD', parent=os))
    document.add(Node('OpenBSD', parent=os))
    document.add(Node('NetBSD', parent=os))
    document.add(Node('Solaris', parent=os))

    document.add(Node('Java', parent=cl))
    document.add(Node('C++', parent=cl))
    document.add(Node('C', parent=cl))
    document.add(Node('Pascal', parent=cl))

    document.add(Node('Python', parent=sl))
    document.add(Node('Ruby', parent=sl))
    document.add(Node('Tcl', parent=sl))
    document.add(Node('PHP', parent=sl))

    document.add(Node('Qt', parent=tk))
    document.add(Node('MFC', parent=tk))
    document.add(Node('wxPython', parent=tk))
    document.add(Node('GTK+', parent=tk))
    document.add(Node('Swing', parent=tk))

    return document
