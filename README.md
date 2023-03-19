# Handwritten Text Recognition
 Handwritten text recognition using CNN with EMNIST dataset.

## Intro
A simple neural network with the following layers is used to recognise hadnwritten text.
- Flatten layer (784)
- Dense layer (256)(relu)
- Dense layer (128)(relu)
- Dense layer (62)(Output)(softmax)

### Model 2
- Conv2D layer (32)(kernel = 5)(relu)
- MaxPool2D layer
- Dropout (0.3)
- Flatten
- Dense Layer(128)(relu)
- Dense Layer (62)(output)(softmax)

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

### 🏃‍♂️ Run the model :
- Run the `tkRecogIndv.py` script to check for individual characters only.
- Run the `tkRecogAll.py` script to recognize words along with numbers.

IN BOTH CASES MAKE SURE TO EDIT THE `unixTime` VARIABLE TO YOUR MODEL'S FOLDER.

### 📸 Screenshots
![image](https://user-images.githubusercontent.com/38806897/225983444-f7001431-c7a4-4cd4-a7d2-6bf0b1e08d45.png)
![image](https://user-images.githubusercontent.com/38806897/225983496-fe8df897-bc10-4a55-b6d9-550b12c7d32e.png)

<i>As you can see, the model cannot differentiate between capital and small 'O'.</i>

### 📝 To do list :
- [ ] Make improved models to raise the accuracy
- [ ] Improve the preprocessing of images
