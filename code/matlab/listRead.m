function [listFile]  = listRead(listFile)
    fid=fopen(listFile,'rt');
    listFile = [];
    while ~feof(fid)
        str = fgetl(fid);   % 读取一行, str是字符串
        str=strcat(str,".csv");
        str=strcat("../python/", str);
        % disp(str);
        listFile = [listFile; str];
    end