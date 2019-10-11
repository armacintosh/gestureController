function state = EnterInJumper(const, state)

import System.Diagnostics.Process.* 

% find the active window title
hWnd = calllib('user32','GetForegroundWindow');
[retVal, ~] = calllib('user32','GetWindowTextA', int32(hWnd), const.windowTitlePtr, int32(100));
activeWindowTitle = char(const.windowTitlePtr.Value(1:retVal));

% if jumper is active window return the Enter key state....
if contains(activeWindowTitle,'jumper','IgnoreCase',true)
     state.rtnStatus = System.Windows.Input.Keyboard.IsKeyToggled(state.keys(8));    
end   
