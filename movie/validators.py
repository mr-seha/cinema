from rest_framework.exceptions import ValidationError


# import cv2
# import mediapipe as mp
# import numpy as np
# from PIL import Image
#
#
# # from django.core.exceptions import ValidationError
#
#
# def check_if_character_picture_contains_face(file):
#     pil_image = Image.open(file)
#     image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
#     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
#     mp_face_detection = mp.solutions.face_detection
#     with mp_face_detection.FaceDetection(
#             min_detection_confidence=0.5
#     ) as face_detection:
#         results = face_detection.process(rgb_image)
#         if not results.detections:
#             raise ValidationError("هیچ چهره ای در تصویر وارد شده یافت نشد")


def film_thumbnail_size_validator(image):
    max_size = 800 * 1024
    if image.size > max_size:
        error_msg = f"اندازه تصویر از {max_size} کیلوبایت بیشتر می باشد"
        raise ValidationError(error_msg)
