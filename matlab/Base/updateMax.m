function [const, out, store] = updateMax(const,out,store)

% start with max and then trip based on historical max and baseline
out.currentMaxF = max(store.mavF);
out.currentMaxE = max(store.mavE);

% updated based on last window
            
    % update the forever maxs
    if (out.currentMaxE*0.75) > const.AllTimeMaxE
        const.AllTimeMaxE = out.currentMaxE*0.75;        
    else 
        const.AllTimeMaxE = const.AllTimeMaxE ;
    end 

    if (out.currentMaxF*0.75) > const.AllTimeMaxF
        const.AllTimeMaxF = out.currentMaxF*0.75;
    else 
        const.AllTimeMaxF = const.AllTimeMaxF ;
    end     
    
    % if have not done any flexion....(here you get really low F thresh...)
    % so have to assum E and F sensor activity are comperable.
    if out.currentMaxF < out.currentBaseF*10
        out.currentMaxF = out.currentMaxE ;
    end
    
    % ensure it is not too low. 
    % too low = near threshold, near base
    if out.currentMaxE <= const.AllTimeMaxE % 
        out.currentMaxE = const.AllTimeMaxE;
    end

    if out.currentMaxF <= const.AllTimeMaxF % 
        out.currentMaxF = const.AllTimeMaxF;
    end

