# METHODS INCLUDED IN THIS MODULE
#
# cubic(coords, t)              # get point on bezier curve r(t)
# dt_cubic(coords, t)           # get point on r'(t)
# dt2_cubic(coords, t)          # get point on r''(t)
# dt3_cubic(coords, t)          # get point on r'''(t)
# deCasteljau(coords, t)        # calculate point using De Casteljau
# vectorMagnitude(vec)          # get magnitude of vector
# tangent_cubic(coords, t)      # get unit tangent vector at point of bezier
# binormal_cubic(coords, t)     # binormal vector at point
# normal_cubic(coords, t)       # cross product T x B
# curvature_cubic(coords, t)    # get curvature at point of bezier
# torsion(coords, t)            # get torsion at point
#
# moveSplinesTo_cubic(coords)       # move points of cubic bezier curve
# createBez_cubic(coords)           # create a cubic bezier curve
# pointOnBez_cubic(coords, t)       # place a point object in the scene
# 
