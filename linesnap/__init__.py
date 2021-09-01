import shapely.geometry as geom
from shapely.ops import nearest_points
import pandas as pd

# Through changing the shape of the proper one of two line elements, realize the snapping processing. 
# g1 and g2 is the geometry in 'shapely', tolerance is a threshold.
def linesnap(g1,g2,tolerance):
    if g1.intersects(g2)==True:
        return (g1,g2,g1.intersection(g2))
    else:
        line1_head=geom.Point(list(g1.coords)[0])
        line1_tail=geom.Point(list(g1.coords)[-1])
        line2_head=geom.Point(list(g2.coords)[0])
        line2_tail=geom.Point(list(g2.coords)[-1])
        temp=[]
        head1_line2=line1_head.distance(g2)
        temp.append({"point":"line1_head","line":"line2","distance":head1_line2,"point_geo":line1_head,"line_geo":g2})
        tail1_line2=line1_tail.distance(g2)
        temp.append({"point":"line1_tail","line":"line2","distance":tail1_line2,"point_geo":line1_tail,"line_geo":g2})
        head2_line1=line2_head.distance(g1)
        temp.append({"point":"line2_head","line":"line1","distance":head2_line1,"point_geo":line2_head,"line_geo":g1})
        tail2_line1=line2_tail.distance(g1)
        temp.append({"point":"line2_tail","line":"line1","distance":tail2_line1,"point_geo":line2_tail,"line_geo":g1})
        temp_df=pd.DataFrame(temp)
        min_dist=temp_df[temp_df['distance']==temp_df['distance'].min()].reset_index(drop=True)
        #print(temp_df)
        if min_dist.loc[0,'distance']<=tolerance:
            another_point=nearest_points(min_dist.loc[0,'line_geo'], min_dist.loc[0,'point_geo'])[0]
            if min_dist.loc[0,'point']=='line1_head':
                g1=geom.LineString([another_point.coords[0]]+list(g1.coords))
                return (g1,g2,another_point)
            elif min_dist.loc[0,'point']=='line1_tail':
                g1=geom.LineString(list(g1.coords)+[another_point.coords[0]])
                return (g1,g2,another_point)
            elif min_dist.loc[0,'point']=='line2_head':
                g2=geom.LineString([another_point.coords[0]]+list(g2.coords))
                return (g1,g2,another_point)
            elif min_dist.loc[0,'point']=='line2_tail':
                g2=geom.LineString(list(g2.coords)+[another_point.coords[0]])
                return (g1,g2,another_point)
        else:
            #print('They may not have an intersection')
            return(g1,g2,None)