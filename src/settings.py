from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Handy


class SettingRow(Handy.ActionRow):

    def __init__(self, title, subtitle, widget):
        Handy.ActionRow.__init__(self)

        self.__populate_widget(title, subtitle, widget)

    def __populate_widget(self, title, subtitle, widget):
        self.set_title(title)
        self.set_subtitle(subtitle)
        self.add_action(widget)


class SettingExpanderRow(Handy.ExpanderRow):
    toggled = GObject.Property(type=bool, default=False)

    def __init__(self, title, subtitle):
        Handy.ExpanderRow.__init__(self)

        self.__populate_widget(title, subtitle)

    def __populate_widget(self, title, subtitle):
        self.set_title(title)
        self.set_subtitle(subtitle)

        # Hackish solution until libhandy have a property for that
        expander_toggled_btn = self.get_children()[0].get_children()[3]
        expander_toggled_btn.bind_property("active", self, "toggled",
                                           GObject.BindingFlags.BIDIRECTIONAL)
