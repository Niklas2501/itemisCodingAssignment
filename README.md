# itemis Coding Challenge

## Assumptions

* In case some information is missing, e.g. a mapping from an intergalactic to a roman number, the converter will try
  and ask the user to input the missing information.
  ```console
  > pok is I
  > lok pok Iron is 30 Credits
  missing information / invalid input: How much is lok ?
  > lok is V
  ```
* In case no amount is given as an intergalactic numeral in a request, an amount of 1 is assumed.
    ```console
  > pok is I
  > pok Iron is 30 Credits
  > how many Credits is Iron ?
  Iron is 30 Credits
  ```

* In case an invalid intergalactic / roman number is entered, a warning is printed and the input is ignored.
* In case an intergalactic number is defined a second time, the old value is simply overwritten. The same is true for
  changes in the value of materials.
* The same roman numeral can be represented by multiple intergalactic ones.

## Other Notes

* Regarding the implementation of the validity check: For the purpose of the assignment, the implementation adheres to
  the given rules, even though simpler tests for the correctness of roman numerals exist.
* Furthermore, a library function could have been used for this (as for the conversion between Roman and decimal
  representation). This wasn't done, since it might have reduced the scope of the task too much.
* Contrary to the commit message, in [this commit](https://github.com/Niklas2501/itemisCodingAssignment/commit/528e3c52a3d4d43fbdba822897a840f9ae0c91c4) it was unintentionally forgotten to add the test cases for complete
  input sequences. This has been corrected in the [following commit](https://github.com/Niklas2501/itemisCodingAssignment/commit/a97f5ce4774363044c68bbb9e4e910a06b39a51c).
* pyTest is used over the standard unit testing package for it's more convenient test definition.

## Build

* The code was written using a Python 3.9.7 interpreter, but previous versions should also work.
* The necessary libraries are listed in the requirements.txt file.