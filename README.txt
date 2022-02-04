An interactive Python program for displaying juggle state diagrams, all possible transitions and closed paths between states, as well as  animating siteswap juggling sequences 
(see https://juggle.fandom.com/wiki/State_notation and https://juggle.fandom.com/wiki/Siteswap). Requires Python3 with numpy and matplotlib.  
If you have the pyinstaller package, you can create an executable version in ./dist/Main/ by running install.bat.
Each rectangle corresponds to a state and each arrow corresponds to a throw. Left-click to select a state. Only the states to which you can transition from the current state are clickable, they have blue frames. 
Once a loop is formed, a juggling diagram showing the trajectories of every ball is shown. To see an animation, press "a". To refresh, right-click anywhere in the window or click on "Refresh". 
You can increase the total number of balls and the maximum duration of throws by using buttons in the upper part of the window. Note that the maximum is not proportional to the duration, since a) the height of a ball scales 
with the duration of the ball in the air as height~duration^2 and b) the balls spend some time in the hands. By default, arrows that correspond to throws of zero height and states connected only by such arrowes are hidden, 
you can show them by toggling off "hide zeros". By default, the colors of the arrows are given by the loop (= the base of the periodic siteswap sequence), to which they belong, you can instead color them by height by toggling 
off "show loops". You can toggle on "reverse throws" to show throws from the outside in, instead of inside out as in the regular cascade. Happy/sad/meh toggle changes the face of the juggler.

#TODO: fix misaligned buttons
