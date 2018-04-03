listFile = listRead('../python/lists.txt');
force = [];
r = [[]];
g = [[]];
b = [[]];
figure(1);
for i=1:1:length(listFile)
    disp(listFile(i));
    [force_temp,r_temp,g_temp,b_temp] = csvDataLoad(listFile(i));
    hold on
    if i<=3
        plot(force_temp, g_temp,'r.');
    elseif i<=6
        plot(force_temp, g_temp,'g.');
    else
        plot(force_temp, g_temp,'b.');
    end
    %figure(i)
    %plot(force_temp, g_temp,'.');
end