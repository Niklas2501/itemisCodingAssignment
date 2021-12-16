# itemis Coding Challenge

## Assumptions and other notes

* Regarding the implementation of the sanity checks: For the purpose of the assignment, the implementation adheres to
  the given rules, even if a simpler test for the correctness of Roman numerals exists.
* Furthermore, a library function could have been used for this (as for the conversion between Roman and decimal
  representation). This was not done, since it might have reduced the scope of the task too much.
* In case some information is missing, e.g. a mapping from an intergalactic to a roman number, the converter will ask to
  input the missing information.
* In case no amount is given as an intergalactic in a request, an amount of 1 is assumed.
* In case an invalid intergalactic / roman number is entered a warning is printed and the input is ignored. 
* pyTest is used over the standard unit testing module for it's more convenient test definition.

## Build