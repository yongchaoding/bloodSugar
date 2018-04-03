function [force, r, g, b]  = csvDataLoad(csvFile)
    M = csvread(csvFile,2,0);
    force = M(:,2);
    r = M(:,4);
    g = M(:,3);
    b = M(:,1);
    