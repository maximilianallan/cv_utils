from visualizer import Visualizer

vis = Visualizer( (2,2) )

vis.add_3dplot("./poseplotter/data/estimated_results.csv","./poseplotter/data/ground_truth_results.csv",(0,0),2,1,title="Tracking 3D Plot")
vis.add_video("./poseplotter/data/video.avi",(0,1),1,1,title="Video File")
vis.add_video("./poseplotter/data/tracking.avi",(1,1),1,1,title="Tracking File")

vis.visualize()