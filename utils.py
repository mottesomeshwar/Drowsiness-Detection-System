from scipy.spatial import distance as dist

def eye_aspect_ratio(eye):
    # Vertical distances
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # Horizontal distance
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def mouth_aspect_ratio(mouth):
    # Vertical distances between internal lips
    # 68-point model inner lip indices are 61-67
    A = dist.euclidean(mouth[13], mouth[19]) # 62, 68
    B = dist.euclidean(mouth[14], mouth[18]) # 63, 67
    C = dist.euclidean(mouth[15], mouth[17]) # 64, 66
    # Horizontal distance
    D = dist.euclidean(mouth[12], mouth[16]) # 61, 65
    mar = (A + B + C) / (2.0 * D)
    return mar