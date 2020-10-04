import cv2
import sys

traker_bounding_box_dictionary = {}

# Do not forget to modify the two variables below
video_source = "/video/%04d.png"
groundtruth_report_dir = "/foo1/bar1.txt"

tracker_type = 'CSRT'
tracker = cv2.TrackerCSRT_create()
selection = 0

def reinit_tracker(restart,frameNumber,video): 
	global tracker
	global tracker_type
	global selection
	# Max number of frames
	n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	ok, frame = video.read()
	
	print('#' + str('{0:04}'.format(frameNumber)))
	bbox = (0, 0, 0, 0)
	if not ok:
		print ('Cannot read video file')
		sys.exit()
    # Uncomment the line below to select a different bounding box
	if restart:
		#frameNumber = frameNumber - 1
		video.set(1,frameNumber)
		ret, frame = video.read()
		bbox = cv2.selectROI(frame, False)
		cv2.destroyWindow("ROI selector")
		tracker = selector(tracker_type)
		print (bbox)
	else:
		bbox = (284, 130, 63, 176)

    # Initialize tracker with first frame and bounding box
	#tracker = cv2.TrackerTLD_create()
	#tracker = cv2.TrackerCSRT_create()
	print (bbox)
	ok = tracker.init(frame, bbox)
	"""if (frameNumber == 1):
		#frameID = "frame_"+str(frameNumber)
		frameID = frameNumber
		traker_bounding_box_dictionary[frameID] = '{0} {1} {2} {3}'.format(int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]))
	else:
		#frameID = "frame_"+str(frameNumber)
		frameID = frameNumber
		traker_bounding_box_dictionary[frameID] = "0 0 0 01"
	"""

	frameID = frameNumber
	traker_bounding_box_dictionary[frameID] = '{0} {1} {2} {3}'.format(int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]))

	while True:
        # Read a new frame
		ok, frame = video.read()
		print('#' + str('{0:04}'.format(frameNumber)))
		if not ok:
			break

        # Start timer
		timer = cv2.getTickCount()

        # Update tracker
		ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
		fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
		if ok:
			frameNumber = frameNumber + 1
            # Tracking success
			p1 = (int(bbox[0]), int(bbox[1]))
			p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
			cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
			coordiante = '{0} {1} {2} {3}'.format(int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]))
			#frameID = "frame_"+str(frameNumber)
			frameID = frameNumber
			traker_bounding_box_dictionary[frameID] = str(coordiante)
		else :
            # Tracking failure
			cv2.putText(frame, "The tracker has failed, please reinitialise", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
			restart = True
			cv2.destroyWindow("pyTAG")
			print ("The tracker failed on frame number: " + str('{0:04}'.format(frameNumber)))
			ok, frame = video.read()
			reinit_tracker(restart,frameNumber,video)

        # Display tracker type on frame
		cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        # Display FPS on frame
		cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

		cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )

        # Display result
		cv2.imshow("pyTAG", frame)

        # Exit if ESC pressed
		k = cv2.waitKey(1) & 0xff
		if k == 32 :

			restart = True
			print ("(Manually restart) The tracker failed on frame number: " + str('{0:04}'.format(frameNumber)))
			#cv2.destroyWindow("ITAGGen")
			#ok, frame = video.read()

			while video.isOpened():
				#cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
				# Read video capture
				#ret, frame = video.read()
				
				# show one frame at a time
				key = cv2.waitKey(0)
				while key not in [32, ord('n'), ord('p'), ord('a')]:
					key = cv2.waitKey(0)
					
					
				if key == ord('n'):
					print(key)
					if frameNumber < n_frames:
						#frameID = "frame_"+str(frameNumber)
						frameID = frameNumber
						traker_bounding_box_dictionary[frameID] = "0 0 0 0"
						frameNumber = frameNumber + 1
						video.set(1,frameNumber)
						ret, frame = video.read()
						cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
						cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
				if key == ord('p'):
					print(key)
					if n_frames >= frameNumber and frameNumber != 0:
						#frameID = "frame_"+str(frameNumber)
						frameID = frameNumber
						traker_bounding_box_dictionary[frameID] = "XXX"
						frameNumber = frameNumber - 1
						video.set(1,frameNumber)
						ret, frame = video.read()
						cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
						cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
				# Quit when 'q' is pressed
				if key == ord('a'):
					print(key)
					selection = selection + 1
					selection=(selection%6)
					print(selection)
					if(selection == 0):
						tracker_type = 'CSRT'
						tracker = cv2.TrackerCSRT_create()
					elif(selection == 1):
						tracker_type = 'TLD'
						tracker = cv2.TrackerTLD_create()
					elif(selection == 2):
						tracker_type = 'KCF'
						tracker = cv2.TrackerKCF_create()
					elif(selection == 3):
						tracker_type = 'BOOSTING'
						tracker = cv2.TrackerBoosting_create()
					elif(selection == 4):
						tracker_type = 'MIL'
						tracker = cv2.TrackerMIL_create()
					elif(selection == 5):
						tracker_type = 'MEDIANFLOW'
						tracker = cv2.TrackerMedianFlow_create()
					"""elif(selection == 6):
						tracker_type = 'MOSSE'
						tracker = cv2.TrackerMOSSE_create()"""

					video.set(1,frameNumber)
					ret, frame = video.read()
					cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
					cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
				if key == 32:
					video.set(1,frameNumber)
					ret, frame = video.read()
					#frameNumber = frameNumber - 1
					#video.set(1,frameNumber)
					#frameID = "frame_"+str(frameNumber)
					# frameID = frameNumber
					#traker_bounding_box_dictionary[frameID] = "0 0 0 0"
					break
				# Display each frame
				cv2.imshow("pyTAG", frame)
				
			#cv2.destroyWindow("ROI selector")
			reinit_tracker(restart,frameNumber,video)

def selector(tracker_type):
	if(tracker_type == 'CSRT'):
		tracker = cv2.TrackerCSRT_create()
	elif(tracker_type == 'TLD'):
		tracker = cv2.TrackerTLD_create()
	elif(tracker_type == 'KCF'):
		tracker = cv2.TrackerKCF_create()
	elif(tracker_type == 'BOOSTING'):
		tracker = cv2.TrackerBoosting_create()
	elif(tracker_type == 'MIL'):
		tracker = cv2.TrackerMIL_create()
	elif(tracker_type == 'MEDIANFLOW'):
		tracker = cv2.TrackerMedianFlow_create()
	return tracker;

if __name__ == '__main__':


	frameNumber = 0
	restart = False
	
	video = cv2.VideoCapture(video_source)

	# Exit if video not opened.
	if not video.isOpened():
		print ("Could not open video")
		sys.exit()


	reinit_tracker(restart,frameNumber,video)

	# Write tracker ground truth file destination
	#track_file = open("C:/Users/Ekincan/Desktop/MU/testing-framework-tracking/final/csrt.txt", "w")
	track_file = open(ground_truth_report_dir, "w")
	
	for key in sorted(traker_bounding_box_dictionary.keys()):
		print(str(key)+" :: "+traker_bounding_box_dictionary[key])
		track_file.write(traker_bounding_box_dictionary[key]+"\n")
		
	track_file.close()
