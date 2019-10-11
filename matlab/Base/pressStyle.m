function [out] = pressStyle (const,out,act)


% setup mouse click functions
import java.awt.Robot;
import java.awt.event.*;
mouse = Robot;
fprintf ('pressStyle --> %i \n\n', act);
out.stylePressed = act;

const.pushbutton.AppActivate(char(const.gameLoc)); % make sure it is the same game
if const.press == 1
    switch act
        case  0
            mouse.keyPress(KeyEvent.VK_0);
            mouse.keyRelease(KeyEvent.VK_0);
            
        case  1
            mouse.keyPress(KeyEvent.VK_1);
            mouse.keyRelease(KeyEvent.VK_1);
            
        case  2
            mouse.keyPress(KeyEvent.VK_2);
            mouse.keyRelease(KeyEvent.VK_2);
        case  3
            mouse.keyPress(KeyEvent.VK_3);
            mouse.keyRelease(KeyEvent.VK_3);
        case  4
            mouse.keyPress(KeyEvent.VK_4);
            mouse.keyRelease(KeyEvent.VK_4);
        case  5
            mouse.keyPress(KeyEvent.VK_5);
            mouse.keyRelease(KeyEvent.VK_5);
        case  6
            mouse.keyPress(KeyEvent.VK_6);
            mouse.keyRelease(KeyEvent.VK_6);
            
        case  7
            mouse.keyPress(KeyEvent.VK_7);
            mouse.keyRelease(KeyEvent.VK_7);
            
        case  8
            mouse.keyPress(KeyEvent.VK_8);
            mouse.keyRelease(KeyEvent.VK_8);
        case  9
            mouse.keyPress(KeyEvent.VK_9);
            mouse.keyRelease(KeyEvent.VK_9);

        otherwise
            mouse.keyPress(KeyEvent.VK_9);
            mouse.keyRelease(KeyEvent.VK_9);
            
    end 
end
        
        
end 
  