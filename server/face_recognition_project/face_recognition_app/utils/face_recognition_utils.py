#check "Main function"  section above
import os
import cv2
from mtcnn.mtcnn import MTCNN
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
import h5py
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
def process_image(image):
    if image.shape[2] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    label = "user"
    return image, label
def getImage(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    label = os.path.splitext(os.path.basename(image_path))[0]
    return image,label
def save_image_to_file(image_data, file_path='uploads/latest_image.jpeg'):
    with open(file_path, 'wb') as file:
        file.write(image_data)

    return file_path
def extract_face(image, required_size=(224, 224)):
    detector = MTCNN()
    results = detector.detect_faces(image)
    face_arrays = []
    bounding_boxes = []

    for i, result in enumerate(results):
        x, y, width, height = result['box']
        x2, y2 = x + width, y + height
        face = image[y:y2, x:x2]
        face = Image.fromarray(face)
        face = face.resize(required_size)
        face_array = np.asarray(face)
        face_arrays.append(face_array)

        bounding_boxes.append((x, y, width, height))

    return face_arrays, bounding_boxes

    return face_arrays, bounding_boxes
def extract_single_face(image, required_size=(224, 224)):
    faces, bounding_boxes = extract_face(image, required_size)
    if len(faces) > 0:
        largest_face_index = np.argmax([w * h for _, _, w, h in bounding_boxes])
        return faces[largest_face_index], bounding_boxes[largest_face_index]
    else:
        return None, None

def get_embedding(employee_id, face_pixel):
    sample = np.expand_dims(face_pixel.astype('float32'), axis=0)
    sample = preprocess_input(sample, version=2)
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
    embedding = model.predict(sample)
    return employee_id, embedding


def save_embeddings(embeddings_list, file_path="embedding.h5"):
    try:
        with h5py.File(file_path, 'a') as hf:
            for id, embedding in embeddings_list:
                if id in hf:
                    # Existing dataset, overwrite
                    hf[id][:] = embedding
                else:
                    # Create a new dataset
                    hf.create_dataset(id, data=embedding)
    except Exception as e:
        print(f"Error saving embeddings to HDF5: {e}")

def load_embeddings(file_path="embedding.h5"):
    embeddings = {}
    try:
        with h5py.File(file_path, 'r') as hf:
            for employee_id in hf.keys():
                embedding = np.array(hf[employee_id])
                embeddings[employee_id] = embedding
    except Exception as e:
        print(f"Error loading embeddings from HDF5: {e}")
        return None

    return embeddings


def build(image_list, labels, hdf5_file_path="embedding.h5"):
    if len(image_list) != len(labels):
        print("Error: The number of images and labels must be the same.")
        return

    embedding_data = []

    for i, (image, label) in enumerate(zip(image_list, labels)):
        print(i)
        try:
            face_pixels, _ = extract_face(image)
            if not face_pixels:
                print(f"No face detected in image {i + 1} with label '{label}'. Skipping.")
                continue

            face_id = f"{label}"
            embedding = get_embedding(face_id, face_pixels[0])[1].flatten()

            embedding_data.append((face_id, embedding))
        except Exception as e:
            print(f"Error processing image {i + 1} with label '{label}': {e}")
            continue

    if not embedding_data:
        print("No valid embeddings were generated.")
        return

    save_embeddings(embedding_data, hdf5_file_path)




def similarity_function(embedding1, embedding2):
    normalized_embedding1 = embedding1 / np.linalg.norm(embedding1)
    normalized_embedding2 = embedding2 / np.linalg.norm(embedding2)
    return cosine_similarity([normalized_embedding1], [normalized_embedding2])[0][0]

def check_id_existence(employee_id, stored_embeddings):

    return employee_id in stored_embeddings

def verify_person(face_pixels, stored_embeddings , threshold=0.6):
    try:
        result = get_embedding("input_face", face_pixels)
        if result is None or len(result) != 2:
            print("Invalid input face embedding.")
            return None, None

        input_embedding = result[1].flatten()

        #stored_embeddings = load_embeddings("embedding.h5")

        if not stored_embeddings:
            print("No stored embeddings available.")
            return None, None

        verification_results = {}
        for id, stored_embedding in stored_embeddings.items():
            similarity = similarity_function(input_embedding, stored_embedding.flatten())
            verification_results[id] = similarity

        verified_employee = None
        max_similarity = max(verification_results.values())
        if max_similarity >= threshold:
            verified_employee = max(verification_results, key=verification_results.get)

        return verified_employee, max_similarity
    except Exception as e:
        print(f"Error during verification: {e}")
        return None, None


def visualize_verification(image, stored_embeddings, box_color=(0, 255, 0), box_thickness=2, text_size=0.5):
   
    face_arrays, bounding_boxes = extract_face(image, required_size=(224, 224))

    for face_array, (x, y, width, height) in zip(face_arrays, bounding_boxes):
        # Perform face verification for the current face array
        verified_employee, P = verify_person(face_array, stored_embeddings)

        # Customize box color based on verification result
        color = box_color if verified_employee is not None else (255, 0, 0)
        cv2.rectangle(image, (x, y), (x + width, y + height), color, box_thickness)

        # Customize text size and color
        text = f"E: {verified_employee}" if verified_employee is not None else "Unknown"
        text_color = (0, 255, 0) if verified_employee is not None else (255, 0, 0)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, text_size, text_color, box_thickness)

    plt.imshow(image)
    plt.axis('off')
    plt.show()


def draw_boxes_on_image(image_path, results):
    # Read the image from the given path
    image = cv2.imread(image_path)

    # Iterate over the results and draw boxes based on the conditions
    for result in results:
        user = result['user']
        box = result['box']
        threshold = result['threshold']

        # Define the color based on the threshold
        color = (0, 255, 0) if threshold > 0.6 else (0, 0, 255)  # Green for threshold > 0.6, red otherwise

        # Convert box coordinates to integers
        x, y, width, height = map(int, (box['x'], box['y'], box['width'], box['height']))

        # Draw the bounding box on the image with customization
        line_thickness = 2
        cv2.rectangle(image, (x, y), (x + width, y + height), color, line_thickness)

        # Customize font settings for the label
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_thickness = 1
        font_color = (0, 0, 0)  # White text color

        # Put the user's name and threshold on the image
        label = f"{user} ({threshold:.2f})"
        text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]

        # Draw a filled rectangle as the background for the text
        cv2.rectangle(image, (x, y - text_size[1] - 5), (x + text_size[0] + 5, y), color, cv2.FILLED)

        # Put text on the image
        cv2.putText(image, label, (x, y - 5), font, font_scale, font_color, font_thickness)

    # Plot the image with matplotlib
    ani = FuncAnimation(plt.gcf(), lambda x: plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)),
                        interval=100, blit=False)
    plt.axis('off')  # Turn off axis labels
    plt.show()

def get_image_box(image_path, results):
    # Read the image from the given path
    image = cv2.imread(image_path)

    # Iterate over the results and draw boxes based on the conditions
    for result in results:
        user = result['user']
        box = result['box']
        threshold = result['threshold']

        # Define the color based on the threshold
        color = (0, 255, 0) if threshold > 0.6 else (0, 0, 255)  # Green for threshold > 0.6, red otherwise

        # Convert box coordinates to integers
        x, y, width, height = map(int, (box['x'], box['y'], box['width'], box['height']))

        # Draw the bounding box on the image with customization
        line_thickness = 2
        cv2.rectangle(image, (x, y), (x + width, y + height), color, line_thickness)

        # Customize font settings for the label
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_thickness = 2
        font_color = (0, 0, 0)  # White text color

        # Put the user's name and threshold on the image
        label = f"{user} ({threshold:.2f})"
        text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]

        # Draw a filled rectangle as the background for the text
        cv2.rectangle(image, (x, y - text_size[1] - 5), (x + text_size[0] + 5, y), color, cv2.FILLED)

        # Put text on the image
        cv2.putText(image, label, (x, y - 5), font, font_scale, font_color, font_thickness)

    return image

