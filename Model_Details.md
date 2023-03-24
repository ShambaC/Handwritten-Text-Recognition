## Model 1
- Flatten layer (784)
- Dense layer (256)(relu)
- Dense layer (128)(relu)
- Dropout (0.45)
- Dense layer (62)(Output)(softmax)

## Model 2
- Conv2D layer (32)(kernel = 5)(relu)
- MaxPool2D layer
- Dropout (0.3)
- Flatten
- Dense Layer(128)(relu)
- Dense Layer (62)(output)(softmax)

## Model 3
- Conv2D (32)(kernel = 3)
- MaxPool2D
- BatchNormalization()
- Conv2D (64)(kernel = 3)
- BatchNormalization()
- MaxPool2D
- BatchNormalization()
- Conv2D (256)(kernel = 3)
- BatchNormalization()
- Conv2D (256)(kernel = 3)
- GlobalAvgPool2D
- Dense (256)(relu)
- Dense (62)(softmax)

## Future
I am planning on doing a ResNet but the concept seems scary.

<details>
<summary>PS</summary>

I have heard that LSTM RNN is good for this. But again that's scary.

<details>
<summary>PS PS</summary>

I deleted model 4 because it was faulty. IDK why tho and can't be bothered to check.

I am slowly coming to the conclusion that with this dataset I cannot get past the 84% threshold. The conv nets produce weird results in inference despite having better stats.

</details>

</details>