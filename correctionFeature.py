import cv2
import sys

#do not forget to change the three variables below
video_source = "/video/%04d.png"
groundtruth_report_dir = "/foo1/bar1.txt"
reviewed_GT_report_dir = "/foo1/bar2.txt"

def report_reviewedGT(ground_truth_data):
	reviewed_GT_file = open(reviewed_GT_report_dir, "w")

	for key in sorted(ground_truth_data.keys()):
		reviewed_GT_file.write(str(ground_truth_data[key][0])+" "+str(ground_truth_data[key][1])+" "+str(ground_truth_data[key][2])+" "+str(ground_truth_data[key][3])+"\n")
		
	reviewed_GT_file.close()


if __name__ == '__main__':
	frameNumber = 0
	editCount = 0
	#set Ground truth bounding box coordinate text file
	ground_truth_file = open(groundtruth_report_dir, "r")
	
	#set Tracker bounding box coordinate text file
	ground_truth_data = {}
	tracker_data = {}
	gtf_line = ground_truth_file.readline()

	counter = 0
	# Parse ground truth and tracker bounding box files
	while gtf_line:
		ground_truth_data[counter] = gtf_line.split()[0:]
		counter = counter + 1
		gtf_line = ground_truth_file.readline()
	
	# Read video
	video = cv2.VideoCapture(video_source)
	n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
	while True:
		ok, frame = video.read()
		if (frameNumber) < counter:
			p1_g = (int(ground_truth_data[frameNumber][0]), int(ground_truth_data[frameNumber][1]))
			p2_g = (int(ground_truth_data[frameNumber][0]) + int(ground_truth_data[frameNumber][2]), int(ground_truth_data[frameNumber][1]) + int(ground_truth_data[frameNumber][3]))
			cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
			cv2.rectangle(frame, p1_g, p2_g, (0,255,0), 2, 1)
		print('#' + str('{0:04}'.format(frameNumber)))
		if not ok:
			break

        # Start timer
		timer = cv2.getTickCount()

        # Update tracker
        # Calculate Frames per second (FPS)
		fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
		# Display result
		cv2.imshow("pyTAG", frame)
		# Exit if ESC pressed
		k = cv2.waitKey(1) & 0xff
		if k == 32 :
			restart = True
			#ok, frame = video.read()

			while video.isOpened():
				cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
				# Read video capture
				#ret, frame = video.read()
				
				# show one frame at a time
				key = cv2.waitKey(0)
				while key not in [32, ord('n'), ord('b'), ord('a'), ord('e')]:
					key = cv2.waitKey(0)
						
				if key == ord('n'):
					print(key)
					if frameNumber < n_frames-1:
						frameID = frameNumber
						frameNumber = frameNumber + 1
						p1_g = (int(ground_truth_data[frameNumber][0]), int(ground_truth_data[frameNumber][1]))
						p2_g = (int(ground_truth_data[frameNumber][0]) + int(ground_truth_data[frameNumber][2]), int(ground_truth_data[frameNumber][1]) + int(ground_truth_data[frameNumber][3]))
						video.set(1,frameNumber)
						ret, frame = video.read()
						cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
						cv2.rectangle(frame, p1_g, p2_g, (0,255,0), 2, 1)
					else:
						break
				if key == ord('b'):
					print(key)
					if n_frames >= frameNumber and frameNumber != 0:
						frameID = frameNumber
						frameNumber = frameNumber - 1
						p1_g = (int(ground_truth_data[frameNumber][0]), int(ground_truth_data[frameNumber][1]))
						p2_g = (int(ground_truth_data[frameNumber][0]) + int(ground_truth_data[frameNumber][2]), int(ground_truth_data[frameNumber][1]) + int(ground_truth_data[frameNumber][3]))
						video.set(1,frameNumber)
						ret, frame = video.read()
						cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
						cv2.rectangle(frame, p1_g, p2_g, (0,255,0), 2, 1)
				if key == ord('e'):
					break
				if key == 32:
					editCount = editCount + 1
					bbox = cv2.selectROI(frame, False)
					coordinate = '{0} {1} {2} {3}'.format(int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]))
					if(str(coordinate) != "0 0 0 0"):
						ground_truth_data[frameNumber] = (str(coordinate)+"\n").split()[0:]
					else:
						coordinate = "0 0 0 0"
						ground_truth_data[frameNumber] = (str(coordinate)+"\n").split()[0:]
						print(str(ground_truth_data[frameNumber]))
					cv2.destroyWindow("ROI selector")
					p1_g = (int(ground_truth_data[frameNumber][0]), int(ground_truth_data[frameNumber][1]))
					p2_g = (int(ground_truth_data[frameNumber][0]) + int(ground_truth_data[frameNumber][2]), int(ground_truth_data[frameNumber][1]) + int(ground_truth_data[frameNumber][3]))
					video.set(1,frameNumber)
					cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
					cv2.rectangle(frame, p1_g, p2_g, (0,255,0), 2, 1)
				# Display each frame
				cv2.imshow("pyTAG", frame)
		frameNumber = frameNumber + 1
	print("Total corrections: "+str(editCount))
	report_reviewedGT(ground_truth_data)