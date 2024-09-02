import rumps
import main
import copy

class StatusBarApp(rumps.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_profiles()
    
    def create_load_lambda(self, item):
        return lambda _ : main.load(item)
    
    @rumps.clicked("Save Profile")
    def save(self, _):
        name = rumps.Window(title="What should this profile be called?", cancel=True).run().text
        main.save(name)
        self.add_profiles()
        
    def add_profiles(self):
        items = list(main.profiles.keys())
        for item in self.menu.keys()[0:-3]:
            del self.menu[item]
        for item in items:
            try:
                self.menu.insert_before("Save Profile", rumps.MenuItem(f"Load '{item}'", lambda _, item=item: main.load(item)))
            except KeyError:
                self.menu.add(rumps.MenuItem(f"Load '{item}'", lambda _, item=item: main.load(item)))
        self.menu.insert_after(f"Load '{items[-1]}'", rumps.separator)


if __name__ == "__main__":
    app = StatusBarApp("DockSwitcher", icon="logo.svg")
    app.run()