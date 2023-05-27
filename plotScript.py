from matplotlib import pyplot as plt
import csv

# Define path for the log data
unixTime = 1679036461
acc_path = f"Models/{unixTime}/tb_data/epoch_accuracy"
loss_path = f"Models/{unixTime}/tb_data/epoch_loss"

# Init variables storing all the scalar data
x_train_acc = []
y_train_acc = []
x_val_acc = []
y_val_acc = []

x_train_loss = []
y_train_loss = []
x_val_loss = []
y_val_loss = []

# Store data into the variables after reading from the csv files
with open(f"{acc_path}/train.csv") as csvfile :
    lines = csv.reader(csvfile)
    row_num = 0
    for row in lines :
        if row_num > 0 :
            x_train_acc.append(int(row[1]))
            y_train_acc.append(round(float(row[2]), 4))
        row_num += 1

with open(f"{acc_path}/validation.csv") as csvfile :
    lines = csv.reader(csvfile)
    row_num = 0
    for row in lines :
        if row_num > 0 :
            x_val_acc.append(int(row[1]))
            y_val_acc.append(round(float(row[2]), 4))
        row_num += 1

with open(f"{loss_path}/train.csv") as csvfile :
    lines = csv.reader(csvfile)
    row_num = 0
    for row in lines :
        if row_num > 0 :
            x_train_loss.append(int(row[1]))
            y_train_loss.append(round(float(row[2]), 4))
        row_num += 1

with open(f"{loss_path}/validation.csv") as csvfile :
    lines = csv.reader(csvfile)
    row_num = 0
    for row in lines :
        if row_num > 0 :
            x_val_loss.append(int(row[1]))
            y_val_loss.append(round(float(row[2]), 4))
        row_num += 1

# Plot the figures
plt.figure(0)
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.plot(x_train_acc, y_train_acc, label= "train", color= 'tab:orange')
plt.plot(x_val_acc, y_val_acc, label= "validation", color= 'c')
plt.legend()

plt.figure(1)
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.plot(x_train_loss, y_train_loss, label= "train", color= 'tab:orange')
plt.plot(x_val_loss, y_val_loss, label= "validation", color= 'c')
plt.legend()

plt.show()