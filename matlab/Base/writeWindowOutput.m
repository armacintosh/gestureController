function [] = writeWindowOutput(const,out)
% writeWindowOutput to textfile

% write the current out values to .txt file (only the ones designated in store).
for fieldIndex = 1:length(const.storeFieldNames)
    
    field = char(const.storeFieldNames(fieldIndex));
        
    if isfield(out,field)
        
        % if it is the end dont put comma
        if fieldIndex == length(const.storeFieldNames) 
            val = out.(field);
            fprintf(const.fileID_STORE, '%f ', val) ; 
            
        % if it is time make a string not num    
        elseif strcmp(field,'time')                    
            val = datestr(out.time,const.dateFormat);
            fprintf(const.fileID_STORE, '%s,', val) ; 
            
        % if is any other do number and , seperator
        else                                           
            val = out.(field);                         
            fprintf(const.fileID_STORE, '%f,', val) ;
        end 
        
    end
end
 
% add new line when done row 
fprintf(const.fileID_STORE, ' \n') ;  
