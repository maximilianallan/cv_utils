function [] = save_frames( video_file, save_dir)

    v = VideoReader(video_file);

    i = 1;
    while hasFrame(v)
       
        frame = readFrame(v);
        if mod( i, 50 ) == 0
           imwrite(frame, sprintf('%s/frame%d.png', save_dir, i)); 
        end
        
        i = i + 1;                       
            
    end
    


end