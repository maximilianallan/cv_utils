from visualizer import Visualizer

vis = Visualizer( (1,2) )

vis.add_3dplot("../../data/estimated_results.csv","../../data/ground_truth_results.csv",(0,0),1,1)
vis.add_video("../../data/video.avi",(0,1),1,1)

vis.visualize()