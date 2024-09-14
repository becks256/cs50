This README file contains the results of the image classification project. The project was to create a convolutional neural network to classify images in the German Traffic Sign Recognition Benchmark dataset.  The project was completed using TensorFlow and Keras.

The first attempt showed dismal results simply copying the Model and Parameters from the lesson examples for handwritten digits.  The results were as follows:

## Results:

``` bash
  Epoch 1/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.0548 - loss: 13.7092         
  Epoch 2/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.0569 - loss: 3.6055  
  Epoch 3/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.0589 - loss: 3.5471  
  Epoch 4/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.0554 - loss: 3.5193  
  Epoch 5/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.0598 - loss: 3.5019  
  Epoch 6/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.0606 - loss: 3.4977  
  Epoch 7/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.0602 - loss: 3.5001  
  Epoch 8/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.0602 - loss: 3.4862  
  Epoch 9/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.0551 - loss: 3.4976  
  Epoch 10/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 9ms/step - accuracy: 0.0584 - loss: 3.4925  
```

## Model

``` python
  model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Conv2D(
            32,
            (3, 3),
            activation="relu",
            input_shape=(IMG_WIDTH, IMG_HEIGHT, 3),
        ),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),
    ]
  )
```

---

Second attempt tried a 9x9 kernel size for the convolutional layer, but the results were equally dismal. 

---

Subsequent attempts modified the Dropout, pool size and kernel size.  The results improved significantly, but still not satisfactory.  The best results were obtained with the following model and parameters:


## Results: 
    
``` bash
  500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 7ms/step - accuracy: 0.0696 - loss: 8.9955         
  Epoch 2/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 7ms/step - accuracy: 0.2071 - loss: 2.9314  
  Epoch 3/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 7ms/step - accuracy: 0.3477 - loss: 2.1910  
  Epoch 4/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 7ms/step - accuracy: 0.4560 - loss: 1.7678  
  Epoch 5/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 7ms/step - accuracy: 0.5319 - loss: 1.5023  
  Epoch 6/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 7ms/step - accuracy: 0.5572 - loss: 1.3844  
  Epoch 7/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 7ms/step - accuracy: 0.6002 - loss: 1.2358  
  Epoch 8/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 7ms/step - accuracy: 0.6308 - loss: 1.1563  
  Epoch 9/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 7ms/step - accuracy: 0.6427 - loss: 1.0818  
  Epoch 10/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 7ms/step - accuracy: 0.6632 - loss: 1.0260  
  333/333 - 1s - 3ms/step - accuracy: 0.7403 - loss: 0.8165
```

## Model
``` python
  model = tf.keras.models.Sequential(
      [
          tf.keras.layers.Conv2D(
              64,
              (3,3),
              activation="relu",
              input_shape=(IMG_WIDTH, IMG_HEIGHT, 3),
          ),
          tf.keras.layers.MaxPooling2D(pool_size=(9 ,9)),
          tf.keras.layers.Flatten(),
          tf.keras.layers.Dense(128, activation="relu"),
          tf.keras.layers.Dropout(0.2),
          tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),
      ]
  )
```

---

More random testing was done with the model and parameters.  Kernel was reduced back to 3 x 3, and the pool size was reduced to 2 x 2.  I also had the idea to change the number of nodes in the first dense layer to `255` to match the color range.  

Tinkering with the droipout rate, I tested with 0.5 and 0.2.  The results were better with 0.2.  The best results were obtained with the following model and parameters:

## Results

``` bash
  Epoch 1/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 15s 29ms/step - accuracy: 0.2975 - loss: 22.1610      
  Epoch 2/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 14s 28ms/step - accuracy: 0.7900 - loss: 0.7553
  Epoch 3/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 14s 27ms/step - accuracy: 0.8723 - loss: 0.4621
  Epoch 4/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 27ms/step - accuracy: 0.9000 - loss: 0.3629
  Epoch 5/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 27ms/step - accuracy: 0.9084 - loss: 0.3350
  Epoch 6/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.9283 - loss: 0.2779
  Epoch 7/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.9338 - loss: 0.2489
  Epoch 8/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.9447 - loss: 0.2174
  Epoch 9/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 26ms/step - accuracy: 0.9367 - loss: 0.2549
  Epoch 10/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 13s 25ms/step - accuracy: 0.9356 - loss: 0.2783
  333/333 - 1s - 4ms/step - accuracy: 0.9372 - loss: 0.2849
```

## Model
``` python
  model = tf.keras.models.Sequential(
      [
          tf.keras.layers.Conv2D(
              64,
              (3,3),
              activation="relu",
              input_shape=(IMG_WIDTH, IMG_HEIGHT, 3),
          ),
          tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
          tf.keras.layers.Flatten(),
          tf.keras.layers.Dense(255, activation="relu"),
          tf.keras.layers.Dropout(0.2),
          tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),
      ]
  )
```

Increasing to a 5x5 kernel, the accuracy quickly ramped to 91% in 4 epochs, 95% in 10. 


# Additional testing:

* Out of curiosity, I tried 3 Dense layers with 255 nodes (to reprepsent 3 full color channels).  By 3 epochs, the accuracy was at 90%; 97% by 10. In this instance, I only dropped out 20% from the final dense layer, no dropout on preceeding layers.

* In some additional testing, I also tried different optimizers, including `adamax` and `adamw`.  Both were dismal in accuracy, never surpassing 5%.

* Did additional digging in TF docs and found some augmentation preprocessing layers. Unfortunately, that didn't fare as well as I had hoped.  By the 7th epoch, it had consistently achieved 50-60% accuracy and loss was still high.

* Found documentation for BatchNormalziation and tried that with additional convolutional layers and slightly higher dropout.  This had the best results so far, achieving 94% accuracy by the 3rd epoch and 98% by the 10th.

``` bash
  Epoch 1/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 19s 35ms/step - accuracy: 0.4313 - loss: 2.2860    
  Epoch 2/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 34ms/step - accuracy: 0.8974 - loss: 0.3320
  Epoch 3/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 33ms/step - accuracy: 0.9412 - loss: 0.1940
  Epoch 4/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 34ms/step - accuracy: 0.9662 - loss: 0.1135
  Epoch 5/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 34ms/step - accuracy: 0.9739 - loss: 0.0975
  Epoch 6/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 33ms/step - accuracy: 0.9716 - loss: 0.1066
  Epoch 7/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 33ms/step - accuracy: 0.9719 - loss: 0.1113
  Epoch 8/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 33ms/step - accuracy: 0.9808 - loss: 0.0747
  Epoch 9/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 33ms/step - accuracy: 0.9802 - loss: 0.0851
  Epoch 10/10
  500/500 ━━━━━━━━━━━━━━━━━━━━ 17s 33ms/step - accuracy: 0.9782 - loss: 0.0774
  333/333 - 3s - 8ms/step - accuracy: 0.9880 - loss: 0.0488
```

``` python
  model = tf.keras.models.Sequential(
      [
          tf.keras.layers.Conv2D(
              64, (4, 4), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
          ),
          tf.keras.layers.BatchNormalization(),
          tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
          tf.keras.layers.Conv2D(128, (4, 4), activation="relu"),
          tf.keras.layers.BatchNormalization(),
          tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
          tf.keras.layers.Flatten(),
          tf.keras.layers.Dense(255, activation="relu"),
          tf.keras.layers.Dropout(0.3),
          tf.keras.layers.Dense(255, activation="relu"),
          tf.keras.layers.Dropout(0.3),
          tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),
      ]
  )
  ```