import cv2
import pandas as pd

# Taking the dataset
colours = pd.read_csv('colorsWIKI.csv')

# Remove '%' symbol and extra spaces, and convert columns to float
colours["R"] = colours["Red"].str.replace('%', '').str.strip().astype(float)
colours["G"] = colours["Green"].str.replace('%', '').str.strip().astype(float)
colours["B"] = colours["Blue"].str.replace('%', '').str.strip().astype(float)

# Scale Red, Green, and Blue columns to 0-255
colours["R"] = colours["R"] * 255 / 100
colours["G"] = colours["G"] * 255 / 100
colours["B"] = colours["B"] * 255 / 100

colours["Sat"] = colours["SaturationHSL"].str.replace('%', '').str.strip().astype(float)


# Video Camera
cap = cv2.VideoCapture(0)

#Rescale Frame
def rescale_frame(frame,scale=1):
    height = int(frame.shape[0]*scale)
    width = int(frame.shape[1]*scale)
    dimentions = (width,height)
    return cv2.resize(frame,dimentions,interpolation=cv2.INTER_AREA)

# Find Colour
def get_color_name(B, G, R):
    minimum = 1000
    for i in range(len(colours)):
        d = abs(R - int(colours.loc[i, "R"])) + abs(G - int(colours.loc[i, "G"])) + abs(B - int(colours.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = colours.loc[i, "Name"]
    return cname

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()

    # Making the mid point as the indicator
    height, width = frame.shape[:2]

    cx = int(width/2)
    cy = int(height/2)

    pixel_center = frame[cy, cx]

    # Determining Name from the Dataset
    b = int(pixel_center[0])
    g = int(pixel_center[1])
    r = int(pixel_center[2])
    colourname = get_color_name(b,g,r)
    
    if b+g+r < 382:
        cv2.putText(frame, colourname, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    else:
        cv2.putText(frame, colourname, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
    cv2.circle(frame, (cx,cy), 5, (250,250,20), 2)

    if not ret:
        print("Error: Could not read frame.")
        break

    frame_resized = rescale_frame(frame,scale=2)
    cv2.imshow("Frame", frame_resized)

    # Exit the loop when the 'esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
