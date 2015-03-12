To run:

python interpreter.py fullTest.llp

or

python interpreter.py test.llp

if using test.llp change solver in main from line 255 to 256. Comment out 255 with "#" and remove "#" on line 256


Somebugs, need more work to get full functionality. At this moment finds one solution (multipletimes).
If change is made in the .llp file (i.e. from affine to linear) solution might change.
Example remove the "@" from "@emmaBecomesRuined" in init. at the bottom. 