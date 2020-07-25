import cv2
import sys

#do not forget to change the three variables below
video_source = "/video/%04d.png"
groundtruth_report_dir = "/foo1/bar1.txt"
tracker_report_dir = "/foo2/bar2.txt"

if __name__ == '__main__':
	frameNumber = 0

	#set Ground truth bounding box coordinate text file
	ground_truth_file = open(groundtruth_report_dir, "r")
	
	#set Tracker bounding box coordinate text file
	tracker_file = open(tracker_report_dir, "r")

	ground_truth_data = {}
	tracker_data = {}
	gtf_line = ground_truth_file.readline()
	tf_line = tracker_file.readline()
	counter = 0
	# Parse ground truth and tracker bounding box files
	while gtf_line:
		#ground_truth_data[gtf_line.split()[0].replace('frame_','')] = gtf_line.split()[1:]
		counter = counter + 1
		ground_truth_data[counter] = gtf_line.split()[0:]
		#tracker_data[tf_line.split()[0].replace('frame_','')] = tf_line.split()[1:]
		tracker_data[counter] = tf_line.split()[0:]
		
		tf_line = tracker_file.readline()
		gtf_line = ground_truth_file.readline()
	
	# Read video
	video = cv2.VideoCapture(video_source)
	n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	while True:
		if n_frames < (frameNumber+1):
			break
		ok, frame = video.read()
		
		if (frameNumber+1) < counter:
		#len(ground_truth_data) needed if tracked item goes outside scene and never comes back
		# ground truth data point information
		#p1_g = (int(ground_truth_data[str(frameNumber+1)][0]), int(ground_truth_data[str(frameNumber+1)][1]))
		#p2_g = (int(int(ground_truth_data[str(frameNumber+1)][0]) + int(ground_truth_data[str(frameNumber+1)][2])), int(int(ground_truth_data[str(frameNumber+1)][1]) + int(ground_truth_data[str(frameNumber+1)][3])))
			p1_g = (int(ground_truth_data[frameNumber+1][0]), int(ground_truth_data[frameNumber+1][1]))
			p2_g = (int(ground_truth_data[frameNumber+1][0]) + int(ground_truth_data[frameNumber+1][2]), int(ground_truth_data[frameNumber+1][1]) + int(ground_truth_data[frameNumber+1][3]))
		
		
		# tracker data point information
		#p1_t = (int(tracker_data[str(frameNumber+1)][0]), int(tracker_data[str(frameNumber+1)][1]))
		#p2_t = (int(int(tracker_data[str(frameNumber+1)][0]) + int(tracker_data[str(frameNumber+1)][2])), int(int(tracker_data[str(frameNumber+1)][1]) + int(tracker_data[str(frameNumber+1)][3])))
		
			p1_t = (int(tracker_data[frameNumber+1][0]), int(tracker_data[frameNumber+1][1]))
			p2_t = (int(tracker_data[frameNumber+1][0]) + int(tracker_data[frameNumber+1][2]), int(tracker_data[frameNumber+1][1]) + int(tracker_data[frameNumber+1][3]))
		
		# Draw tracker bounding box
			cv2.rectangle(frame, p1_t, p2_t, (0,0,255), 2, 1)
		# Draw ground truth bounding box
			cv2.rectangle(frame, p1_g, p2_g, (0,255,0), 2, 1)
		
		cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
		cv2.imshow("Tracking",frame)
		k = cv2.waitKey(50) & 0xff
		if k == 32:
			bbox = cv2.selectROI(frame, False)
			cv2.destroyWindow("ROI selector")
		#	f.write(str(bbox)+"\n")
			continue
		#f.write(abcd)
		frameNumber = frameNumber + 1
