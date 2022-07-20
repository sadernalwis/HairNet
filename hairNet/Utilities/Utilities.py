import inspect
import logging, bpy
logger = logging.getLogger(__name__)
class Utilities:
    is_operator = lambda member: inspect.isclass(member) and member.__module__ and issubclass(member, bpy.types.Operator)

    def wrapper(wrapper_arguments):
        def factory(original_function):
            def modified(self, *args, **kwargs):
                print(*args)
            return modified
            # argNames = [argName for argName in inspect.getfullargspec(fn)[0] if argName != 'self']
            # [nameNarg for nameNarg in zip(argNames, args) if nameNarg[1] is not original]
        return factory

    def serial_get(kw, *args):
        retval = []
        for arg in args:
            if type(arg) in (list,tuple):
                for alt in arg:
                    found = False
                    alt_v = kw.get(alt)
                    if alt_v: 
                        retval.append(alt_v)
                        found = True
                        break
                if not found : retval.append(None)
            else:
                retval.append(kw.get(arg))
        return retval

    def serial_fill(kw, *args):
        return {arg:kw.get(arg) for arg in args}
        
    def mode(scope_mode, keep=False):
        def factory(original_function):
            def modified(*args, **kwargs):
                current_mode = bpy.context.object.mode if bpy.context.object else None
                if current_mode and current_mode is not scope_mode: bpy.ops.object.mode_set(mode=scope_mode)
                retval = None
                if  args and kwargs:      retval = original_function(*args, **kwargs)
                elif args and not kwargs: retval = original_function(*args)
                elif  not args and kwargs:retval = original_function(**kwargs)
                else:                     retval = original_function()
                if not keep and hasattr(bpy.context,'object') and current_mode and bpy.context.object and bpy.context.object.mode is not current_mode:
                    bpy.ops.object.mode_set(mode=current_mode)
                return retval
            return modified
        return factory
