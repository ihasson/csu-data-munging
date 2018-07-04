from stuff_for_prof import *

df = pd.read_csv("data/hsdat.csv",
        dtype={'sid':'O','application_nbr':'O'
            ,'HS_subject':'O','HS_Crs_Nbr':'O'
            ,'HS_grade_level':'O','Descr':'O'
            ,'Fall_Gr':'O','Spr_Gr':'O','Sum_Gr':'O'
            ,'Honors':'O','Sum2_Gr':'O','CMan':'O'
            ,'High_School':'O','Course_Source':'O'}) 

df['grade'] = df.apply(get_weighted_grade,axis=1)
df[['sid','Descr','grade']].to_csv("data/hsgrades.csv")
