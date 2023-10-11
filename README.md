# Facial Recognition

## Table of Contents
- [Abstract](#abstract)
- [Concept](#concept)
- [Steps](#steps)
  - [Extract Image](#extract-image)
  - [Face Detection](#face-detection)
  - [Feature Extraction](#feature-extraction)
  - [Face Recognition](#face-recognition)
- [Challenges](#challenges)
  - [Lighting Conditions](#lighting-conditions)
    - [Low Light](#low-light)
    - [Harsh Shadows](#harsh-shadows)
    - [Mixed Lighting](#mixed-lighting)
  - [Face Orientation](#face-orientation)
    - [Variability in Pose](#variability-in-pose)
  - [Facial Components](#facial-components)
  - [Face Objects](#face-objects)
    - [Accessories and Obstructions](#accessories-and-obstructions)
  - [Facial Expressions](#facial-expressions)
  - [Privacy Concerns](#privacy-concerns)
  - [Security Vulnerabilities](#security-vulnerabilities)
- [Old Techniques (Classical)](#old-techniquesclassical)
  - [Eigenfaces](#eigenfaces)
  - [Local Binary Patterns (LBP)](#local-binary-patterns-lbp)
  - [HOG (Histogram of Oriented Gradients)](#hog-histogram-of-oriented-gradients)

## Abstract
How to accurately and effectively identify people has always been an interesting topic, both in research and in industry. With the rapid development of artificial intelligence in recent years, facial recognition gains more and more attention. In comparison to older (traditional) methods, **facial recognition** offers significant advantages, such as being faster, more efficient, and more reliable.

(...)

## Concept
**A facial recognition system** is a technology potentially capable of matching a human face from a digital image or a video frame against a database of faces based on the **features** and **characteristics** of their faces.

(...)

## Steps
Given a picture (taken from a digital camera, for example), we would like to know if there is any person inside, where his/her face is located, and who he/she is.

### Extract Image
(...)

### Face Detection
The main function of this step is to determine (1) whether human faces appear in a given image, and (2) where these faces are located at. The expected outputs of this step are patches containing each face in the input image. Use a face detection algorithm.

(...)

### Feature Extraction
Extract facial features from the patches. Common features include distances between eyes, the shape of the nose, and the contours of the face.

### Face Recognition
After formalizing the representation of each face, the last step is to recognize the identities of these faces. In order to achieve automatic recognition, a face database is required for that.

## Challenges

### Lighting Conditions

#### Low Light: Insufficient lighting

#### Harsh Shadows: Overhead lighting and shadows

#### Mixed Lighting: Environments with a mix of natural and artificial light

### Face Orientation

#### Variability in Pose: Faces can be captured from various angles

### Facial Components
Changes in facial components, like hairstyle, facial hair, or makeup, can significantly alter a person's appearance.

### Face Objects

#### Accessories and Obstructions: Wearing accessories like sunglasses, hats...

### Facial Expressions
Facial expressions can alter the geometry of facial features, making it challenging to match a face under different emotional states.

#### Privacy Concerns
(...)

#### Security Vulnerabilities
(...)

## Old Techniques (Classical)

### Eigenfaces

### Local Binary Patterns (LBP)

### HOG (Histogram of Oriented Gradients)
