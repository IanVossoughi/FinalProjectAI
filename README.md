# CS4341-Final-Project

Full Lines:
   Main Program:
      fastLines.py

   Other Programs:
      bestLines.py
      lines.py

Line Segments:
   Main Program:
      bestSegs.py

   Other Programs:
      fastSegs.py
      segs.py

Usage and Description:
   python bestSegs.py [image path] [num lines] [time] [segment length] [optional output filename]
      Tries to approximate the image found at [image path] by drawing [num lines] line segments, with maximum length [segment length],
      int [time] seconds.  It saves the output to "output/[optional output filename]" if it is specified.  Each iteration, it tries to
      randomly replace one of the worst existing lines with a random new line, and only makes the replacement if the new line is better
      than the line it is trying to replace.

   python fastSegs.py [image path] [num lines] [time] [segment length] [optional output filename]
      Tries to approximate the image found at [image path] by drawing [num lines] line segments, with maximum length [segment length],
      int [time] seconds.  It saves the output to "output/[optional output filename]" if it is specified.  Each iteration, it tries to
      randomly replace an existing line with a new random line, and only makes the replacement if the new line is better than the line 
      it is trying to replace.

   python segs.py [image path] [num lines] [time] [optional output filename]
      Other than having a fixed segment length, it does the same thing as fastSegs.py, except much less efficiently.

   python fastLines.py [image path] [num lines] [time] [optional output filename]
      Tries to approximate the image using lines across the entire image.  Does this the same way as fastSegs.py

   python bestLines.py [image path] [num lines] [time] [optional output filename]
      Tries to approximate the image using lines across the entire image.  Does this the same way as bestSegs.py
      *Note that this actually performs worse than fastLines.py

   python lines.py [image path] [num lines] [time] [optional output filename]
      Does the same thing as fastLines.py, but much less efficiently.

*Note: bestSegs.py, fastSegs.py, bestLines.py, and fastLines.py take a .jpg or .jpeg as input.
       lines.py and segs.py take a .png, .jpg, or .jpeg as input and, if an output file is specified, it must be a .png.
       There are probably other filetypes that work.
