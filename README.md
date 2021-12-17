# itemis Coding Challenge

## Assumptions
* In case some information is missing, e.g. a mapping from an intergalactic to a roman number, the converter will ask to
  input the missing information.
* In case no amount is given as an intergalactic in a request, an amount of 1 is assumed.
* In case an invalid intergalactic / roman number is entered, a warning is printed and the input is ignored.
* In case an intergalactic number is defined a second time, the old value is simply overwritten. The same is true for
  changes in the value of materials.
* The same roman numeral can be represented by multiple intergalactic ones. 

## Other Notes
* Regarding the implementation of the validity check: For the purpose of the assignment, the implementation adheres to
  the given rules, even though simpler tests for the correctness of roman numerals exist.
* Furthermore, a library function could have been used for this (as for the conversion between Roman and decimal
  representation). This was not done, since it might have reduced the scope of the task too much.
* pyTest is used over the standard unit testing module for it's more convenient test definition.

## Build
* The code was written using a Python 3.9.7 interpreter, but lower versions should work fine.
* The necessary libraries are listed in the requirements.txt file. 