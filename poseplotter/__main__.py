from visualizer import Visualizer

vis = Visualizer( (1,1) )

vis.add_3dplot("./poseplotter/data/video2/new_stereo_results.csv","./poseplotter/data/video2/ground_truth_results_.csv",(0,0),2,1,xrange=(-20,20),yrange=(-20,20),zrange=(20,110))
#vis.add_video("./poseplotter/data/video.avi",(0,1),1,1,title="Video File")
#vis.add_video("./poseplotter/data/tracking.avi",(1,1),1,1,title="Tracking File")

vis.visualize()