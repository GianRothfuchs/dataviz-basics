%javaaddpath c:\blp\DAPI\blpapi3.jar

if false
    
    bb = blp;
    isconnection(bb)
    holdingStruc = struct();
    tnr = [1 2 3 4 7 8 10 15];
    for ii = tnr
        sec = "IGEEVC" + num2str(ii,'%02d')
        [d,sc] = history(bb,sec + " BVLI INDEX",'PX_LAST','1/01/2011','6/01/2021')
        
        if ~isstr(d) && ~isempty(d)
            holdingStruc.(sec) = array2table(d,'VariableNames',{'Date','Yld'})
        end
    end
    
    save('BB_data.mat','holdingStruc')
    close(bb)
    
else
    load('BB_data.mat')
end

df = table();
fn = fieldnames(holdingStruc);

for ii = 1:length(fn)
    if ii == 1
        
        
        tmp = holdingStruc.(fn{ii});
        tmp.Properties.VariableNames(2) = fn(ii);
        df = tmp;
    else
        tmp = holdingStruc.(fn{ii});
        tmp.Properties.VariableNames(2)= fn(ii);
        df = outerjoin(df,tmp,'Keys',[1],'MergeKeys',1);
    end
end
writetable(df,'EUR_IG_Curve.csv')