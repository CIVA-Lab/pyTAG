import cv2
import sys

traker_bounding_box_dictionary = {}

# Do not forget to modify the three variables below
video_source = '/myImages/%04d.png'
ground_truth_report_dir = '/myReports/gt_reportx.txt'
skip_frame_rate = 5

def groundTruthGenerator(restart,frameNumber,video):
	# Max number of frames
	n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

	for i in range(0,n_frames):
		traker_bounding_box_dictionary[i] = "0 0 0 0"
	
	while True:
        # Read a new frame
		ok, frame = video.read()
		print('#' + str('{0:04}'.format(frameNumber)))
		if not ok:
			break

        	# Start timer
		timer = cv2.getTickCount()

        	# Calculate Frames per second (FPS)
		fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        	# Draw bounding box
		if ok:
			if(frameNumber == 0):
				bbox = cv2.selectROI(frame, False)
				cv2.destroyWindow("ROI selector")
				print (bbox)
				p1 = (int(bbox[0]), int(bbox[1]))
				p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
				cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
				coordiante = '{0} {1} {2} {3}'.format(int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]))
				#frameID = "frame_"+str(frameNumber)
				frameID = frameNumber
				traker_bounding_box_dictionary[frameID] = str(coordiante)

			frameNumber = frameNumber + 1 
			if(((frameNumber % skip_frame_rate) == 0) or (frameNumber == n_frames-1)):
				frameID = frameNumber
				if frameNumber == n_frames-1:
					frameID = n_frames-1

				video.set(1,frameID)
				cv2.imshow("Tracking", frame)
				bbox = cv2.selectROI(frame, False)
				cv2.destroyWindow("ROI selector")
				print (bbox)
				
				
		    # Tracking success
				p1 = (int(bbox[0]), int(bbox[1]))
				p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
				cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
				coordiante = '{0} {1} {2} {3}'.format(int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]))
				#frameID = "frame_"+str(frameNumber)
				
				traker_bounding_box_dictionary[frameID] = str(coordiante)

        # Display FPS on frame
		cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

		cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )

    
        # Exit if ESC pressed
		k = cv2.waitKey(1) & 0xff


def linear_interpolation():

	remainder = int(len(traker_bounding_box_dictionary))%skip_frame_rate
	intAmount = int(len(traker_bounding_box_dictionary)/skip_frame_rate)
	size = intAmount
	flag = False
	print(remainder)
	for frameID in range(0,size):

		if (remainder != 0):
			flag = True

		current = traker_bounding_box_dictionary[(frameID*skip_frame_rate)]
		bbox_1 = current.split()
		if(remainder == 0 and frameID == (size-1)):
			next = traker_bounding_box_dictionary[(frameID*skip_frame_rate)+skip_frame_rate-1]
		else:
			next = traker_bounding_box_dictionary[(frameID*skip_frame_rate)+skip_frame_rate]

		bbox_2 = next.split()			

		p1_1 = (int(bbox_1[0]), int(bbox_1[1])) 
		p1_2 = (int(bbox_1[0]), int(bbox_1[1])+int(bbox_1[3])) 
		p1_3 = (int(bbox_1[0])+int(bbox_1[2]), int(bbox_1[1])) 
		p1_4 = (int(bbox_1[0])+int(bbox_1[2]), int(bbox_1[1])+int(bbox_1[3])) 
		
		p2_1 = (int(bbox_2[0]), int(bbox_2[1])) 
		p2_2 = (int(bbox_2[0]), int(bbox_2[1])+int(bbox_2[3])) 
		p2_3 = (int(bbox_2[0])+int(bbox_2[2]), int(bbox_2[1])) 
		p2_4 = (int(bbox_2[0])+int(bbox_2[2]), int(bbox_2[1])+int(bbox_2[3]))

		# X values change
		x1 = p1_1[0]-p2_1[0]
		x2 = p1_2[0]-p2_2[0]
		x3 = p1_3[0]-p2_3[0]
		x4 = p1_4[0]-p2_4[0]

		# Y values change
		y1 = p1_1[1]-p2_1[1]
		y2 = p1_2[1]-p2_2[1]
		y3 = p1_3[1]-p2_3[1]
		y4 = p1_4[1]-p2_4[1]
	
		change_x1 = float(x1)/(skip_frame_rate)
		change_x4 = float(x4)/(skip_frame_rate)

		change_y1 = float(y1)/(skip_frame_rate)
		change_y4 = float(y4)/(skip_frame_rate)

		adder_x1 = 0
		adder_x4 = 0

		adder_y1 = 0
		adder_y4 = 0
		for frame in range(1,skip_frame_rate):
			adder_x1 = float(adder_x1) + change_x1 
			adder_x4 = float(adder_x4) + change_x4

			adder_y1 = float(adder_y1) + change_y1 
			adder_y4 = float(adder_y4) + change_y4
				
			new_bbox = str(p1_1[0]-int(adder_x1))+" "+str(p1_1[1]-int(adder_y1))+" "+str(abs(int(bbox_1[2])+int(adder_x1-adder_x4)))+" "+str(abs(int(bbox_1[3])+int(adder_y1-adder_y4)))
			traker_bounding_box_dictionary[(frameID*skip_frame_rate) + frame] = new_bbox

	if(flag):
		current = traker_bounding_box_dictionary[(size*skip_frame_rate)]
		bbox_1 = current.split()
		next = traker_bounding_box_dictionary[len(traker_bounding_box_dictionary)-1]
		bbox_2 = next.split()			

		p1_1 = (int(bbox_1[0]), int(bbox_1[1])) 
		p1_2 = (int(bbox_1[0]), int(bbox_1[1])+int(bbox_1[3])) 
		p1_3 = (int(bbox_1[0])+int(bbox_1[2]), int(bbox_1[1])) 
		p1_4 = (int(bbox_1[0])+int(bbox_1[2]), int(bbox_1[1])+int(bbox_1[3])) 
		
		p2_1 = (int(bbox_2[0]), int(bbox_2[1])) 
		p2_2 = (int(bbox_2[0]), int(bbox_2[1])+int(bbox_2[3])) 
		p2_3 = (int(bbox_2[0])+int(bbox_2[2]), int(bbox_2[1])) 
		p2_4 = (int(bbox_2[0])+int(bbox_2[2]), int(bbox_2[1])+int(bbox_2[3]))

		# X values change
		x1 = p1_1[0]-p2_1[0]
		x2 = p1_2[0]-p2_2[0]
		x3 = p1_3[0]-p2_3[0]
		x4 = p1_4[0]-p2_4[0]

		# Y values change
		y1 = p1_1[1]-p2_1[1]
		y2 = p1_2[1]-p2_2[1]
		y3 = p1_3[1]-p2_3[1]
		y4 = p1_4[1]-p2_4[1]
	
		change_x1 = float(x1)/(remainder)
		#change_x2 = float(x2)/9
		#change_x3 = float(x3)/9
		change_x4 = float(x4)/(remainder)

		change_y1 = float(y1)/(remainder)
		#change_y2 = float(y2)/9
		#change_y3 = float(y3)/9
		change_y4 = float(y4)/(remainder)

		adder_x1 = 0
		#adder_x2 = 0
		#adder_x3 = 0
		adder_x4 = 0

		adder_y1 = 0
		#adder_y2 = 0
		#adder_y3 = 0
		adder_y4 = 0
		for frame in range(0,remainder):
			adder_x1 = float(adder_x1) + change_x1 
			adder_x4 = float(adder_x4) + change_x4

			adder_y1 = float(adder_y1) + change_y1 
			adder_y4 = float(adder_y4) + change_y4
				
			new_bbox = str(p1_1[0]-int(adder_x1))+" "+str(p1_1[1]-int(adder_y1))+" "+str(abs(int(bbox_1[2])+int(adder_x1-adder_x4)))+" "+str(abs(int(bbox_1[3])+int(adder_y1-adder_y4)))
			traker_bounding_box_dictionary[(size*skip_frame_rate) + frame +1 ] = new_bbox
			print((size*skip_frame_rate) + frame + 1 )

if __name__ == '__main__':

	frameNumber = 0
	restart = False
	# Read video, set your image source
	video = cv2.VideoCapture(video_source)

	# Exit if video not opened.
	if not video.isOpened():
		print ("Could not open video")
		sys.exit()


	groundTruthGenerator(restart,frameNumber,video)

	track_file = open(ground_truth_report_dir, "w")
	#track_file2 = open(ground_truth_report_dir2, "w")
	
	"""for key in sorted(traker_bounding_box_dictionary.keys()):
		print(str(key)+" :: "+traker_bounding_box_dictionary[key])
		track_file2.write(traker_bounding_box_dictionary[key]+"\n")"""

	linear_interpolation()

	for key in sorted(traker_bounding_box_dictionary.keys()):
		print(str(key)+" :: "+traker_bounding_box_dictionary[key])
		track_file.write(traker_bounding_box_dictionary[key]+"\n")
		
	track_file.close()