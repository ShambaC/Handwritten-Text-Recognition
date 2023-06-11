# Handwritten Text Recognition
 Handwritten text recognition using Neural Networks with EMNIST dataset.
 Main model is not a ConvNet.

## Intro
Handwritten text recognition using various neural networks. 

I am trying out multiple variations right now.

To check the details of the models, refer to [Model Details](https://github.com/ShambaC/Handwritten-Text-Recognition/blob/main/Model_Details.md)

The Extended MNIST or [EMNIST dataset](https://www.nist.gov/itl/products-and-services/emnist-dataset) is used to train the model.
Specifically the byclass set is used as it had data for all the digits and both capital and small letters

All the scripts have comments to help people understand what the hell is going on.

## 🔎 How to use ?
Clone the repo and then do the following

### 📚 Get the EMNIST dataset :
- Download the dataset from [here](http://www.itl.nist.gov/iaui/vip/cs_links/EMNIST/gzip.zip)
- Extract the `gzip.zip` file.
- Now from inside the `gzip` folder, extract the following .gz files : 
    - emnist-byclass-train-images-idx3-ubyte.gz
    - emnist-byclass-train-labels-idx1-ubyte.gz
    - emnist-byclass-test-images-idx3-ubyte.gz
    - emnist-byclass-test-labels-idx1-ubyte.gz
- Keep the binary files and delete every other file.
    - <i>You can keep the `emnist-byclass-mapping.txt` file if you want to check out the label mapping. Its in the format of `Label<space>ASCII`.</i>
- Move the files remaining to the following folder in your project root : `Dataset/EMNIST/`

Now you are good to go with the data 👍

### ⚙ Install the dependencies :
- install the requirements
- Do in the terminal : `pip install -r requirements.txt`
- Required packages are :
    - idx2numpy
    - matplotlib
    - numpy
    - opencv_python
    - Pillow
    - scikit_learn
    - tensorflow

### 🧾 Edit the configurations :
The config variables are located in line 18 of `model.py`.
Change them to whatever you feel like.

### ⛹️‍♀️ Train the model :
Run the `model.py` script to train the model.

I trained the model on my PC with the following parameters :
- learning_rate = 0.0005
- train_epochs = 50
- train_workers = 20
- val_split = 0.1
- batch_size = 100

I trained it with my GTX 1650. It used 2132 MB of GPU memory.  Usage was around 7-8 %. Took about 39-44 seconds each epoch. It took 23 minutes to finish training. It stopped at 34 epochs as the validation loss wasn't improving.

CPU usage was around 55%. My CPU is Ryzen 7 3750H.

Python used 5 gigs of RAM 😥. I don't remember for which values but once the RAM usage went up to 10 gigs 😱.

You can visualise the training using tensorboard. Run `tensorboard --logdir = path_to_logs` in terminal to start the server.

The logs are located at the following folder : `Models/{timestamp}/logs`

~~<i>With this model I have been unable to increase the accuracy beyond 84%.</i>~~
<i>Model 2 increases accuracy to 86%</i>

### ⬇️ Download pre-trained models :
| Model      |    Type   | Test Loss | Test Accuracy | Download |
|------------|-----------|-----------|---------------|----------|
| 1679033527 |     1     |  0.4489   | 0.8467        |[Download](https://cdn.discordapp.com/attachments/559309816640831489/1086345880170418236/Models1.zip)|
| 1679036461 |     1     |  0.4381   | 0.8480        |[Download](https://cdn.discordapp.com/attachments/559309816640831489/1086345880585638039/Models2.zip)|
| 1679220168 |     2     |  0.3837   | 0.8616        |[Download](https://cdn.discordapp.com/attachments/559309816640831489/1086956826173640724/Models3.zip)|
| 1679378923 |     3     |  0.3655   | 0.8679        |[Download](https://cdn.discordapp.com/attachments/559309816640831489/1100994180001566801/Models4.zip)|

### 🏃‍♂️ Run the model :
- Run the `tkRecogIndv.py` script to check for individual characters only.
- Run the `tkRecogAll.py` script to recognize words along with numbers.
- Run the `textrecog_ui.py` script for realtime results.
    - But this needs `recogScript.py` to be configured.

IN BOTH CASES MAKE SURE TO EDIT THE `unixTime` VARIABLE TO YOUR MODEL'S FOLDER.

### 📸 Screenshots
All screenshots are taken with best results. Totally not biased screenshotting.

![image](https://user-images.githubusercontent.com/38806897/225983444-f7001431-c7a4-4cd4-a7d2-6bf0b1e08d45.png)
![image](https://user-images.githubusercontent.com/38806897/226276782-a4c3e7aa-879a-4daa-8cd5-fbe0c993b9a4.png)

<i>Space detection between words</i>

![image](https://user-images.githubusercontent.com/38806897/226188252-80c297ec-045f-4927-922f-36b163679cf6.png)

<i>As you can see, the model cannot differentiate between capital and small 'O'.</i>
 
![image](https://github.com/ShambaC/Handwritten-Text-Recognition/assets/38806897/45801d83-013e-4d82-87fe-016b1c48cfe3)

<i>NEW UI !!</i>

### 👨‍🏫 A little explanation on the pre-processing of images during inference :
- First of all each characters in the image are separated into different images.
    - This is done as the model recognizes individual letters and complete words
    - This done using a [method](https://github.com/ShambaC/Handwritten-Text-Recognition/blob/main/Character_Detection_Method.md) that makes it so that words where the letters are joined together won't work (like cursive writing)
- Then a list is created with the 4 corners co-ordinates of each character.
- Then a check is performed to detect detection rects within characters.
    - This happens with characters having a loop. For example :
        - e, the whole character is detected and the white space as well inside the loop.
        - same goes for a, p or any character with loops.
- Then we sort the detected character co-ordinates in the order in which they appear from left to right.
- Then the original image is cropped to separate the characters and store them in a list.
- Then we detect spaces. The logic is ;
    - First calculate the space between each characters.
    - Find the mean spacing.
    - Any space greater than mean spacing is a space between two words.
- Pad the character images with white pixels to make them as close to a square as possible.
- Resize image to 20x20.
- Transpose image.
- Negate image.
- Pad image on all sides with 4 pixels, resulting in a 28x28 image.

### ❌ Flaws in pre-processing :
- ~Small 'i' is not detected properly as the dot of the 'i' and the bar count as separate characters.~ Fixed with the alternate method to MSER
- Space detection will result in wrong output if the input is a single word.
    - It will add spaces even though they are not needed.

### 📝 To do list :
- [x] Make improved models to raise the accuracy
- [x] Improve the preprocessing of images
- [x] Remove MSER completely
- [x] Make a better UI
 
✔️ All goals reached 🎉
