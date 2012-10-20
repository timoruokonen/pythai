pythai
==========================================================================
Pythai is an artificial intellegence project. The ultimate goal is yet
unclear but it will hopefully clarify at some point :) Currently it only contains
some basic genetic programming and a nice car game. 

Main language in this project is python 2.x.

Install instructions:
==========================================================================
Python:
Version 2.7 (32Bit) or higher is required.

You will need following additional python libraries: pygame, numpy
http://www.pygame.org/download.shtml
http://numpy.scipy.org/

License:
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, December 2004 

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO.

Usage:
==========================================================================

**Playing the Game:**
You can play the great car game and try to beat the computer times!
1. python car_tester.py
* Arrows for moving and Esc to quit

**Executing Genetic Programming Process:**
Starts code generation process that tries to find the best possible solution for the car game.
1. Check the settings from the beginning of the file first then
2. python car_game_ai_generator.py
* Spacebar stops the code generation after the current generation is executed
* Esc quits the code generation without showing any results
* After code generation is finished the log can be found from "best_codes.txt" (if enabled)
