from pyzbar import pyzbar
import argparse
import cv2
import time



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# load the input image
image = cv2.imread(args["image"])



start = time.time()

# find the QR codes in the image and decode them
qrcodes = pyzbar.decode(image)

end = time.time()

print("Time taken to detect and decode QR codes: {}".format(end - start))

# loop over detected QR codes
for qrcode in qrcodes:

	# extract the bounding box location of the qr code and draw the
	# bounding box on the image
	(x, y, w, h) = qrcode.rect
	cv2.rectangle(image, (x,y), (x+w, y+h), (0, 0, 255), 2)

	# the qr code data is a bytes object so if we want to draw it on
	# the image we need to convert it to a string first
	qrcodeData = qrcode.data.decode("utf-8")
	qrcodeType = qrcode.type

	# draw the qr code data and qr code type on the image
	text = "{} ({})".format(qrcodeData, qrcodeType)
	cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
		(0, 0, 255), 2)

	# print the qr code data and type to the terminal
	print("[INFO] Found {} QR code: {}".format(qrcodeType, qrcodeData))

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)


cam = cv2.VideoCapture(0)


while(1):
	_, frame = cam.read()

	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
		cv2.THRESH_BINARY, 11, 2)

	# find the QR codes in the image and decode them
	qrcodes = pyzbar.decode(frame)

	if qrcodes is not None:

		# loop over detected QR codes
		for qrcode in qrcodes:

			# extract the bounding box location of the qr code and draw the
			# bounding box on the image
			(x, y, w, h) = qrcode.rect
			cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)

			# the qr code data is a bytes object so if we want to draw it on
			# the image we need to convert it to a string first
			qrcodeData = qrcode.data.decode("utf-8")
			qrcodeType = qrcode.type

			# draw the qr code data and qr code type on the image
			text = "{} ({})".format(qrcodeData, qrcodeType)
			cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
				(0, 0, 255), 2)

			# print the qr code data and type to the terminal
			print("[INFO] Found {} QR code: {}".format(qrcodeType, qrcodeData))

	cv2.imshow("Cam", frame)

	cv2.waitKey(5)



