#Dataloader code
from datetime import datetime
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
import os
import numpy as np
from sklearn.model_selection import train_test_split


def load_data(root_dir):
    data = []
    labels = []

    for label_folder in os.listdir(root_dir):
        print(label_folder)
        label_path = os.path.join(root_dir, label_folder)
        if os.path.isdir(label_path):
            label = int(label_folder.split('_')[1])
            for npy_file in os.listdir(label_path):
                if npy_file.endswith('.npy'):
                    npy_path = os.path.join(label_path, npy_file)
                    # Load data from npy file

                    window_data = np.load(npy_path)
                    print(window_data.shape)
                    data.append(window_data)
                    labels.append(label)


    data = np.array(data)
    labels = np.array(labels)
    print(data.shape)
    print(len(labels))


    return data, labels
def create_model(input_shape):

    model = models.Sequential([
        layers.Conv1D(32, 3, activation='relu', input_shape=input_shape),
        layers.MaxPooling1D(2),
        layers.Conv1D(64, 3, activation='relu'),
        layers.MaxPooling1D(2),
        layers.Conv1D(128, 3, activation='relu'),
        layers.GlobalAveragePooling1D(),
        layers.Dense(64, activation='relu'),
        layers.Dense(3, activation='softmax')  # Assuming there are 3 classes
    ])
    return model

    # Create and train the model
    model = create_model(input_shape)
    model.summary()

    model.fit(dataset, epochs=10)  # Adjust epochs as needed
def main():
    path_model = "D:\\Dizertatie\\Programare\\Python\\Models\\Incercarea1.h5"
    root_dir = 'D:\Dizertatie\Date\Date_Antrenare'  # Replace with the actual path to your data directory
    data, labels = load_data(root_dir)

    checkpoint = tf.keras.callbacks.ModelCheckpoint(path_model, verbose=1, save_best_only=True)
    # tensorboard --logdir logs/fit
    log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    # Split data into train and test sets
    train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2, random_state=42)
    train_labels_one_hot = to_categorical(train_labels, num_classes=3)
    test_labels_one_hot = to_categorical(test_labels, num_classes=3)

    # Assuming input shape should be [batch, 4, 300]
    input_shape = train_data.shape[1:]
    print(input_shape)

    # Proceed with model training or other tasks
    # Example:
    model = create_model(input_shape)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    print(train_data.shape)
    model.fit(train_data, train_labels_one_hot, batch_size=32, epochs=10, validation_data=(test_data, test_labels_one_hot),callbacks=[checkpoint, tensorboard_callback])


if __name__ == "__main__":
    main()


