function [listFile]  = listRead(listFile)
    fid=fopen(listFile,'rt');
    listFile = [];
    while ~feof(fid)
        str = fgetl(fid);   % ��ȡһ��, str���ַ���
        str=strcat(str,".csv");
        str=strcat("../python/", str);
        % disp(str);
        listFile = [listFile; str];
    end