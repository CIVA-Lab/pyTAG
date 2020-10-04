import cv2
import sys

#do not forget to change the three variables below
video_source = "/video/%04d.png"
groundtruth_report_dir = "/foo1/bar1.txt"
reviewed_GT_report_dir = "/foo1/bar2.txt"

ground_truth_data = {}
tmp_ground_truth_data = {}

def report_reviewedGT():
	reviewed_GT_file = open(reviewed_GT_report_dir, "w")

	for key in sorted(ground_truth_data.keys()):
		reviewed_GT_file.write(ground_truth_data[key])
		
	reviewed_GT_file.close()

if __name__ == '__main__':
	frameNumber = 0

	#set Ground truth bounding box coordinate text file
	ground_truth_file = open(groundtruth_report_dir, "r")
	
	gtf_line = ground_truth_file.readline()
	counter = 0
	# Parse ground truth and tracker bounding box files
	while gtf_line:
		#ground_truth_data[gtf_line.split()[0].replace('frame_','')] = gtf_line.split()[1:]
		ground_truth_data[counter] = gtf_line
		tmp_ground_truth_data[counter] = gtf_line.split()[0:]
		gtf_line = ground_truth_file.readline()
		counter = counter + 1
		
	
	# Read video
	video = cv2.VideoCapture(video_source)
	n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	while True:
		if n_frames < (frameNumber+1):
			break
		ok, frame = video.read()

		if not ok:
			print ('EOF')
			break
		
		if (frameNumber+1) < counter:
			p1_g = (int(tmp_ground_truth_data[frameNumber+1][0]), int(tmp_ground_truth_data[frameNumber+1][1]))
			p2_g = (int(tmp_ground_truth_data[frameNumber+1][0]) + int(tmp_ground_truth_data[frameNumber+1][2]), int(tmp_ground_truth_data[frameNumber+1][1]) + int(tmp_ground_truth_data[frameNumber+1][3]))
		
			# Draw ground truth bounding box
			cv2.rectangle(frame, p1_g, p2_g, (0,255,0), 2, 1)
		
		cv2.putText(frame, "Frame number: " + str('{0:04}'.format(frameNumber)), (100,80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2 )
		cv2.imshow("Tracking",frame)
		k = cv2.waitKey(1000) & 0xff
		if k == 32:
			bbox = cv2.selectROI(frame, False)
			coordinate = '{0} {1} {2} {3}'.format(int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]))
			if(str(coordinate) != "0 0 0 0"):
				print(str(coordinate))
				ground_truth_data[frameNumber] = str(coordinate)+"\n"
			cv2.destroyWindow("ROI selector")
		frameNumber = frameNumber + 1
	report_reviewedGT()
