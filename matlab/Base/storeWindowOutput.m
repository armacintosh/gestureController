function [store] = storeWindowOutput(const,out,store)

% replace store table 
store(1:end-1,:) = store(2:end,:); % moves the past data up a row, and drops oldest data (row 1)

for fieldIndex = 1:length(const.storeFieldNames) % is 3rd field of out. struct is time.

    field = char(const.storeFieldNames(fieldIndex)); % name of field.
    if isfield(out,field)
        
        % update the last row of store with out val.
        store(end,field) = {out.(field)};
    end

end

