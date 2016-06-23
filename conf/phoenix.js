function bindLaunch( key, modifiers, appName ) {
  api.bind( key, modifiers, function() {
      try {
        app = Window.focusedWindow().app()
        if (app.title() == appName) {
          app.hide()
        }
        else {
          api.launch( appName );
        }
      } catch (err) {
          api.launch( appName );
      }
    } );
}

actCmd = ['alt', 'ctrl']

bindLaunch('i', actCmd, 'Messages')
bindLaunch('t', actCmd, 'Terminal')
bindLaunch('s', actCmd, 'Safari')
bindLaunch('p', actCmd, 'Preview')
bindLaunch('x', actCmd, 'xCode')
bindLaunch(',', ['cmd', 'alt'], 'System Preferences')

win = Window.visibleWindowsMostRecentFirst()[0]
if (win) win.focusWindow();
