# face_recognition_app/views.py
import base64

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Users, FaceEmbeddings,AccessLogs
from .utils.face_recognition_utils import extract_single_face,extract_face,get_image_box, verify_person, save_image_to_file, getImage,get_embedding,draw_boxes_on_image
import cv2
import json
import numpy as np
from django.db.models import F

from django.core.exceptions import ObjectDoesNotExist
@csrf_exempt 
def add_user(request):
    if request.method == 'POST':
        try:
            # Assuming you pass user information in the request.POST
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            gender = request.POST.get('gender', '')
            date_of_birth = request.POST.get('date_of_birth', '')
            
            # Validate the required parameters
            if not first_name or not last_name or not gender or not date_of_birth:
                return JsonResponse({'result': 'Error', 'message': 'Incomplete user information.'})

            # Create a new user
            user = Users.objects.create(
                FirstName=first_name,
                LastName=last_name,
                Gender=gender,
                DateOfBirth=date_of_birth,
                IsActive=True  
            )

            # Extract a single face from the uploaded image
            uploaded_image = request.FILES.get('profile_picture', None)
            if not uploaded_image:
                return JsonResponse({'result': 'Error', 'message': 'Profile picture is missing.'})

            # Convert the image to a NumPy array
            image_array = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), cv2.IMREAD_COLOR)

            # Extract a single face from the processed image
            input_face, Box = extract_single_face(image_array)

            if input_face is None:
                return JsonResponse({'result': 'No face detected in the input image.'})

            # Get the face embedding
            _, embedding = get_embedding(user.UserID, input_face)

            # Save the face embedding
            face_embedding = FaceEmbeddings.objects.create(
                UserID=user,
                FaceEmbedding=embedding.tobytes()  # Convert the NumPy array to bytes
            )

            return JsonResponse({'result': 'Success', 'user_id': user.UserID})

        except Exception as e:
            return JsonResponse({'result': 'Error', 'message': str(e)})

    else:
        return JsonResponse({'result': 'Error', 'message': 'Invalid request method. Use POST.'})

@csrf_exempt
def verify_access(request):
    
    try:
        # Assuming you pass the imageSrc in the request data
        image_src = request.POST.get('imageSrc', None)
     
        if not image_src:
            return JsonResponse({'result': 'Error', 'message': 'Image source is missing.'})

        # Convert the data URI to a NumPy array
       
        encoded_data = image_src.split(',')[1]
        decoded_data = base64.b64decode(encoded_data)
        image_data = np.frombuffer(decoded_data, dtype=np.uint8)
        
        image_path = save_image_to_file(image_data)

        # Use the getImage function to get the image and label
        image, label = getImage(image_path)
        # Extract faces from the input image
        face_arrays, bounding_boxes = extract_face(image)
        if not face_arrays:
            return JsonResponse({'result': 'Error', 'message': 'No faces detected in the input image.'})

        # Load stored embeddings from the database
        stored_embeddings = {}
        face_embeddings = FaceEmbeddings.objects.values('UserID_id', 'FaceEmbedding')

        for face_embedding in face_embeddings:
            user_id = face_embedding['UserID_id']
            embedding_data = np.frombuffer(face_embedding['FaceEmbedding'], dtype=np.float32)
            stored_embeddings[user_id] = embedding_data

        # Initialize results list
        results = []

        # Perform face verification for each face
        for face_array, (x, y, width, height) in zip(face_arrays, bounding_boxes):
            # Verify the person using the provided verify_person function
            verified_user_id, similarity_score = verify_person(face_array, stored_embeddings)

            # Customize result based on verification outcome
            if verified_user_id:
                user = Users.objects.filter(UserID=verified_user_id).values('FirstName', 'LastName').first()
                name = f"{user['FirstName']} {user['LastName']}" if user else "Unknown"
                access_log_entry = AccessLogs.objects.create(
                    UserID_id=verified_user_id,
                    AccessResult='Granted',
                )
            else:
                name = "Unknown"

            similarity_score_f = float(similarity_score)

            # Append result to the list
            results.append({
                'user': name,
                'box': {'x': x, 'y': y, 'width': width, 'height': height},
                'threshold': similarity_score_f
            })
            
        
        annota=get_image_box(image_path,results)
        _, img_encoded = cv2.imencode('.png', annota)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        return JsonResponse({'result': 'Success', 'results': results,'image':img_base64})


    except Exception as e:
        return JsonResponse({'result': 'Error', 'message': str(e)})


def get_users_with_logs(request):
    try:
        users_with_access_logs = []
    
        # Fetch all users
        users = Users.objects.all()
    
        for user in users:
            # Fetch access logs for each user
            try:
                access_logs = AccessLogs.objects.filter(UserID=user)
            except ObjectDoesNotExist:
                access_logs = []  # Handle the case where there are no access logs for the user
            
            # Serialize user and access log data
            user_data = {
                'UserID': user.UserID,
                'FirstName': user.FirstName,
                'LastName': user.LastName,
                'Gender': user.Gender,
                'DateOfBirth': str(user.DateOfBirth),
                'IsActive': user.IsActive,
                'CreationTime': str(user.CreationTime),
                'AccessLogs': [
                    {
                        'LogID': log.LogID,
                        'AccessTime': str(log.AccessTime),
                        'AccessResult': log.AccessResult
                    }
                    for log in access_logs
                ]
            }
        
            users_with_access_logs.append(user_data)

        # Return the JSON response
        return JsonResponse({'users': users_with_access_logs})
    except Exception as e:
        return JsonResponse({'result': 'Error', 'message': str(e)}, status=500)


##################################################################
def add_user_with_embedding(request):
    if request.method == 'GET':
        # Assuming you pass user information as query parameters
        first_name = request.GET.get('first_name', '')
        last_name = request.GET.get('last_name', '')
        gender = request.GET.get('gender', '')
        date_of_birth = request.GET.get('date_of_birth', '')
        image_path = request.GET.get('image_path', '')

        # Validate the required parameters
        if not first_name or not last_name or not gender or not date_of_birth or not image_path:
            return JsonResponse({'result': 'Error', 'message': 'Incomplete user information.'})

        # Create a new user
        user = Users.objects.create(
            FirstName=first_name,
            LastName=last_name,
            Gender=gender,
            DateOfBirth=date_of_birth,
            IsActive=True  
        )

        # Get the image and label using getImage function
        image, label = getImage(image_path)


        # Extract a single face from the processed image
        input_face, Box = extract_single_face(image)

        if input_face is None:
            return JsonResponse({'result': 'No face detected in the input image.'})

        # Get the face embedding
        _, embedding = get_embedding(user.UserID, input_face)

        # Save the face embedding
        face_embedding = FaceEmbeddings.objects.create(
            UserID=user,
            FaceEmbedding=embedding.tobytes()  # Convert the NumPy array to bytes
        )

        return JsonResponse({'result': 'Success', 'user_id': user.UserID, 'label': label})

    else:
        return JsonResponse({'result': 'Error', 'message': 'Invalid request method. Use GET.'})
def face_recognition(request):
    try:
        # Assuming you pass the image_path in the request.GET['image_path']
        image_path = request.GET.get('image_path', None)

        if not image_path:
            return JsonResponse({'result': 'Error', 'message': 'Image path is missing.'})

        # Load stored embeddings from the database
        stored_embeddings = {}
        face_embeddings = FaceEmbeddings.objects.values('UserID_id', 'FaceEmbedding')

        for face_embedding in face_embeddings:
            user_id = face_embedding['UserID_id']
            embedding_data = np.frombuffer(face_embedding['FaceEmbedding'], dtype=np.float32)
            stored_embeddings[user_id] = embedding_data

        # Get image and label using getImage function
        image, label = getImage(image_path)

        # Extract faces from the input image
        face_arrays, bounding_boxes = extract_face(image)

        if not face_arrays:
            return JsonResponse({'result': 'No faces detected in the input image.'})

        # Initialize results list
        results = []

        # Perform face verification for each face
        for face_array, (x, y, width, height) in zip(face_arrays, bounding_boxes):
            # Verify the person using the provided verify_person function
            verified_user_id, similarity_score = verify_person(face_array, stored_embeddings)

            # Customize result based on verification outcome
            if verified_user_id:
                user = Users.objects.filter(UserID=verified_user_id).values('FirstName', 'LastName').first()
                name = f"{user['FirstName']} {user['LastName']}" if user else "Unknown"
                access_log_entry = AccessLogs.objects.create(
                    UserID_id=verified_user_id,
                    AccessResult='Granted',
                )
            else:
                name = "Unknown"

           
        
            similarity_score_f = float(similarity_score)

            # Append result to the list
            results.append({
                'user': name,
                'box': {'x': x, 'y': y, 'width': width, 'height': height},
                'threshold': similarity_score_f
            })

        return JsonResponse({'result': 'Success', 'results': results})

    except Exception as e:
        return JsonResponse({'result': 'Error', 'message': str(e)})

