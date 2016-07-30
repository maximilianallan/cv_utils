function [clean_poses, num_cleaned] = flip_bad_rotations(dirty_poses)

flip = zeros(1,3);
do_flip = zeros(1,3);

for n = 2:length(dirty_poses)
    
    for i = 1:3
        if (dirty_poses(n).rotation(i)/abs(dirty_poses(n).rotation(i)) ~= dirty_poses(n-1).rotation(i)/abs(dirty_poses(n-1).rotation(i))) && abs(dirty_poses(n).rotation(i)) > 1
            if flip(i) == 1
                flip(i) = 0;
            else
                flip(i) = 1;
            end
        end
    end
    do_flip = [do_flip; flip];
    
    
end

num_cleaned = 0;

for i = 2:length(dirty_poses)
    
    for n = 1:3
        if do_flip(i,n) == 1 
            dirty_poses(i).rotation(n) = dirty_poses(i).rotation(n) * -1; 
            num_cleaned = num_cleaned + 1;
        end
    end
    
end 

clean_poses = dirty_poses;

end