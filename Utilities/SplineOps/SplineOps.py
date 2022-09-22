class CurveOps:
    
    def is_bezier(obj):
        return (obj.type == 'CURVE' and len(obj.data.splines) > 0
            and  obj.data.splines[0].type == 'BEZIER' 
            and  len(obj.data.splines[0].bezier_points) > 0)