# Character Detection

This method detects characters from a word in an image.

## ❌ Shortcomings

- This method only works when the letters are separated and are not joined together(cursive writing).
- This method works for only 1 line of string.

## 🔧 Procedure

Maximum and Minimum area of detection are defined.

![image](https://user-images.githubusercontent.com/38806897/236636041-6bb5f895-6357-42da-9ed5-fc5c4774160a.png)

<i>Input image</i>

The image is transposed

![image](https://user-images.githubusercontent.com/38806897/236636151-11f3dece-b0c9-4904-bb02-b1540a9ce444.png)

<i>Image after transpose</i>

The image is inverted

![image](https://user-images.githubusercontent.com/38806897/236636208-bf2643a4-d5fa-4a29-ba3b-a5ef6fd829a8.png)

<i>Inverted image</i>

Iterate through entire rows of the image. The current rows were originally the columns of the image. This implies that the image will be traversed from left to right of the correctly oriented string.

Count the number of non_zero elements in the row. As right now the image is in the form of black background and white text. Black has a value of 0 while white has a value of 255. Therefore, when the number of non_zero elements is not a 0, then it means that a letter has been encountered. Thus the index of this row is stored. That will act as the left most value of the particular character.

Then the first and last position of these non zero spots are taken and marked as the upper and lower limit of the character. These are updated as other values are encountered like increasing or decreasing of the vertical limits.

This is done until another completely black column is encountered or the end of image is reached.

Then the values are stored into a tuple like : `(top left X cord, top left Y cord, width, height)`

This tupple is then appended to a list of rects and that list is returned.

![image](https://user-images.githubusercontent.com/38806897/236636232-3cca6682-27c3-4455-a230-a79a57a7ce02.png)

<i>Output Image</i>

## ❓ Why ?

This is my college project. Having MSER in it means I might have to explain it to the teachers. And I don't really understand it myself. So, to avoid any unecessary trouble I wrote a separate method. But this was also a struggle.

The way I implemented the algorithm at first was not really nice performance wise. It was painfully slow. So, I studied up on various numpy methods and rewrote the implementation. This time around it was realllllly good.

A comparison on how much time various methods took on the same input : 

- MSER time : 0.046875s
- Alt time (unoptimized) : 1.859375s
- Alt time (optimized) : 0.015625s

So my method is superior (⌐■_■)
