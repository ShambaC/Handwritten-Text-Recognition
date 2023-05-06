# Character Detection

This method detects characters from a word in an image.

## ❌ Shortcomings

- This method only works when the letters are separated and are not joined together(cursive writing).
- This method works for only 1 line of string.

## 🔧 Procedure

Maximum and Minimum area of detection are defined.

IMG PLACEHOLDER

<i>Input image</i>

The image is transposed

IMG PLACEHOLDER

<i>Image after transpose</i>

The image is inverted

IMG PLACEHOLDER

<i>Inverted image</i>

Iterate through entire rows of the image. The current rows were originally the columns of the image. This implies that the image will be traversed from left to right of the correctly oriented string.

Count the number of non_zero elements in the row. As right now the image is in the form of black background and white text. Black has a value of 0 while white has a value of 255. Therefore, when the number of non_zero elements is not a 0, then it means that a letter has been encountered. Thus the index of this row is stored. That will act as the left most value of the particular character.

Then the first and last position of these non zero spots are taken and marked as the upper and lower limit of the character. These are updated as other values are encountered like increasing or decreasing of the vertical limits.

This is done until another completely black column is encountered or the end of image is reached.

Then the values are stored into a tuple like : `(top left X cord, top left Y cord, width, height)`

This tupple is then appended to a list of rects and that list is returned.

IMG PLACEHOLDER

<i>Output Image</i>