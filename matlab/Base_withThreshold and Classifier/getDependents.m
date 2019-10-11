function [] = getDependents(script)
% put dependents into folder.


[file, path] = uigetfile();
[fList, ~] = matlab.codetools.requiredFilesAndProducts(strcat(path,file));

% folder 
depFolder = uigetdir();

for f = 1:length(fList)
        copyfile(fList{f},depFolder);
end 

%%

% also copy dlls and const file
copyfile(strcat(path,'\user32.dll'),depFolder);
copyfile(strcat(path,'\user32_thunk_pcwin64.dll'),depFolder);
copyfile(strcat(path,'\constFile.txt'),depFolder);


