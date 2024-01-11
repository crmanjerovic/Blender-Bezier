# METHODS INCLUDED IN THIS MODULE

cubic(coords, t)              # get point on bezier curve r(t)<br />
dt_cubic(coords, t)           # get point on r'(t)<br />
dt2_cubic(coords, t)          # get point on r''(t)<br />
dt3_cubic(coords, t)          # get point on r'''(t)<br />
deCasteljau(coords, t)        # calculate point using De Casteljau<br />
vectorMagnitude(vec)          # get magnitude of vector<br />
tangent_cubic(coords, t)      # get unit tangent vector at point of bezier<br />
binormal_cubic(coords, t)     # binormal vector at point<br />
normal_cubic(coords, t)       # cross product T x B<br />
curvature_cubic(coords, t)    # get curvature at point of bezier<br />
torsion(coords, t)            # get torsion at point<br />

moveSplinesTo_cubic(coords)       # move points of cubic bezier curve<br />
createBez_cubic(coords)           # create a cubic bezier curve<br />
pointOnBez_cubic(coords, t)       # place a point object in the scene<br />

