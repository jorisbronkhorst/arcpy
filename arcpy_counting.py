AFS = arcpy.da.SearchCursor("Afsluiters_rondom_T_stuk", ["Afsluiters_rondom_T_stuk.FUNCTIE"])
AFS_list = [row for row in AFS]
from collections import Counter

for x in sorted([[x[0], x[1]] for x in Counter(AFS_list).items()], key=lambda x:x[1], reverse=True):
    print([x[0], x[1], round(100.0*x[1]/len(AFS_list), 1)])
    

