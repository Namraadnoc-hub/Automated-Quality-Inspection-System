# ============================================
# DecodeLabs Project 2
# Automated Quality Inspection System
# Author: Namra Saleem
# ============================================

import cv2
import numpy as np

# --------------------------------------------
# STEP 1: Load Image
# --------------------------------------------
image = cv2.imread("images/sample.jpg")

if image is None:
    print("Error: Image not found!")
    exit()

# Create a copy of the original image
result_image = image.copy()

# --------------------------------------------
# STEP 2: Convert to Grayscale
# --------------------------------------------
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# --------------------------------------------
# STEP 3: Apply Gaussian Blur
# --------------------------------------------
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# --------------------------------------------
# STEP 4: Apply Threshold
# --------------------------------------------
_, threshold = cv2.threshold(
    blur,
    120,
    255,
    cv2.THRESH_BINARY_INV
)

# --------------------------------------------
# STEP 5: Find Contours
# --------------------------------------------
contours, _ = cv2.findContours(
    threshold,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

bolt_found = False
contour_count = 0

# --------------------------------------------
# STEP 6: Detect Bolt
# --------------------------------------------
for contour in contours:

    area = cv2.contourArea(contour)

    if area > 800:

        contour_count += 1
        bolt_found = True

        x, y, w, h = cv2.boundingRect(contour)

        # Draw Green Rectangle
        cv2.rectangle(
            result_image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

        # Object Name
        cv2.putText(
            result_image,
            "Industrial Bolt",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # Area
        cv2.putText(
            result_image,
            f"Area: {int(area)} px",
            (x, y + h + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2
        )

# --------------------------------------------
# STEP 7: PASS / FAIL Decision
# --------------------------------------------
if bolt_found:

    status = "QUALITY CHECK : PASS"
    color = (0, 255, 0)

else:

    status = "QUALITY CHECK : FAIL"
    color = (0, 0, 255)

# --------------------------------------------
# STEP 8: Display Inspection Information
# --------------------------------------------
cv2.putText(
    result_image,
    "AUTOMATED QUALITY INSPECTION",
    (20, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 0, 0),
    2
)
cv2.putText(
    result_image,
    status,
    (20, 60),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    color,
    2
)

cv2.putText(
    result_image,
    f"Contours Detected : {contour_count}",
    (20, 90),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.6,
    (255, 255, 0),
    2
)

# --------------------------------------------
# STEP 9: Save Final Output
# --------------------------------------------
cv2.imwrite(
    "output/result.jpg",
    result_image
)

# --------------------------------------------
# STEP 10: Display All Images
# --------------------------------------------
cv2.imshow("Original Image", image)

cv2.imshow("Grayscale Image", gray)

cv2.imshow("Gaussian Blur", blur)

cv2.imshow("Threshold Image", threshold)

cv2.imshow("Final Inspection Result", result_image)

# --------------------------------------------
# STEP 11: Close Program
# --------------------------------------------
cv2.waitKey(0)
cv2.destroyAllWindows()