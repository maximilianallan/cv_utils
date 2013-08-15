from overlay import Overlay

o = Overlay('cv_utils/video.avi','cv_utils/poses.csv','cv_utils/mono_camera.xml','cv_utils/model.xyz',True)

o.plot_to_window()