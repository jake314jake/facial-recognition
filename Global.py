import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam

# Step 1: Prepare The  Dataset

# Dataset  directory structure like:
# - dataset
#   * train
#     - person1
#       - img1.jpg
#       - img2.jpg
#     - person2
#       - img1.jpg
#       - img2.jpg
#   * validation
#     - person1
#       (...)


train_data_dir = 'dataset/train'
validation_data_dir = 'pdataset/validation'

# Step 2: Choose a Pre-trained Model i chosee imagenet weights and ommit the last Dense  layer (include_top=False)

pretrained_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Step 3: Modify the Model Architecture

# Add your custom output layer for face recognition
# Add the last dense Layer (persons) 
num_classes = len(os.listdir(train_data_dir))
model = models.Sequential()
model.add(pretrained_model)
model.add(layers.GlobalAveragePooling2D())
model.add(layers.Dense(num_classes, activation='softmax'))

# Optionally, freeze some layers
pretrained_model.trainable = False

# Step 4: Fine-tune the Model (transfer learning)

# Use data augmentation during training
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

batch_size = 32

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='categorical'
)

validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='categorical'
)

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)

# Step 5: Evaluate and Tune Hyperparameters

# Evaluate the model on the test set
test_data_dir = 'dataset/test'
test_generator = validation_datagen.flow_from_directory(
    test_data_dir,
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='categorical'
)

test_loss, test_acc = model.evaluate(test_generator, steps=test_generator.samples // batch_size)
print(f'Test accuracy: {test_acc}')

# Optionally, save the fine-tuned model for future use
model.save('fine_tuned_face_recognition_model.h5')
