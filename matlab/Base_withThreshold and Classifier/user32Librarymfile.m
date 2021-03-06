function [methodinfo,structs,enuminfo,ThunkLibName]=user32Librarymfile
%USER32LIBRARYMFILE Create structures to define interfaces found in 'win32'.

%This function was generated by loadlibrary.m parser version  on Mon Apr 16 09:17:26 2018
%perl options:'win32.i -outfile=user32Librarymfile.m -thunkfile=user32_thunk_pcwin64.c -header=win32.h'
ival={cell(1,0)}; % change 0 to the actual number of functions to preallocate the data.
structs=[];enuminfo=[];fcnNum=1;
fcns=struct('name',ival,'calltype',ival,'LHS',ival,'RHS',ival,'alias',ival,'thunkname', ival);
MfilePath=fileparts(mfilename('fullpath'));
ThunkLibName=fullfile(MfilePath,'user32_thunk_pcwin64');
% int GetForegroundWindow ( void ); 
fcns.thunkname{fcnNum}='int32voidThunk';fcns.name{fcnNum}='GetForegroundWindow'; fcns.calltype{fcnNum}='Thunk'; fcns.LHS{fcnNum}='int32'; fcns.RHS{fcnNum}=[];fcnNum=fcnNum+1;
% int GetWindowTextA ( int hWnd , unsigned char * lpString , int nMaxCount ); 
fcns.thunkname{fcnNum}='int32int32voidPtrint32Thunk';fcns.name{fcnNum}='GetWindowTextA'; fcns.calltype{fcnNum}='Thunk'; fcns.LHS{fcnNum}='int32'; fcns.RHS{fcnNum}={'int32', 'uint8Ptr', 'int32'};fcnNum=fcnNum+1;
methodinfo=fcns;