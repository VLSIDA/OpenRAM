import debug
from globals import OPTS
from importlib import reload
    

class sram_factory:
    """
    This is a factory pattern to create modules for usage in an SRAM.
    Since GDSII has a flat namespace, it requires modules to have unique
    names if their layout differs. This module ensures that any module
    with different layouts will have different names. It also ensures that
    identical layouts will share the same name to reduce file size and promote
    hierarchical sharing.
    """

    def __init__(self):
        # A dictionary of modules indexed by module type 
        self.modules = {}
        # These are the indices to append to name to make unique object names
        self.module_indices = {}
        # A dictionary of instance lists indexed by module type
        self.objects = {}

    def reset(self):
        """
        Clear the factory instances for testing.
        """
        self.__init__()
        
    def create(self, module_type, **kwargs):
        """
        A generic function to create a module with a given module_type. The args
        are passed directly to the module constructor.
        """
        # if name!="":
        #     # This is a special case where the name and type don't match
        #     # Can't be overridden in the config file
        #     module_name = name
        if hasattr(OPTS, module_type):
            # Retrieve the name from OPTS if it exists,
            # otherwise just use the name
            module_name = getattr(OPTS, module_type)
        else:
            module_name = module_type
        
        # Either retrieve the already loaded module or load it
        try:
            mod = self.modules[module_type]
        except KeyError:
            c = reload(__import__(module_name))
            mod = getattr(c, module_name)
            self.modules[module_type] = mod
            self.module_indices[module_type] = 0
            self.objects[module_type] = []
            
        # Either retreive a previous object or create a new one
        for obj in self.objects[module_type]:
            (obj_kwargs, obj_item) = obj
            # Must have the same dictionary exactly (conservative)
            if obj_kwargs == kwargs:
                debug.info(3, "Existing module: type={0} name={1} kwargs={2}".format(module_type, obj_item.name, str(kwargs)))
                return obj_item

        # Use the default  name if there are default arguments
        # This is especially for library cells so that the spice and gds files can be found.
        if len(kwargs)>0:
            # Create a unique name and increment the index
            module_name = "{0}_{1}".format(module_name, self.module_indices[module_type])
            self.module_indices[module_type] += 1
        #debug.info(1, "New module: type={0} name={1} kwargs={2}".format(module_type,module_name,str(kwargs)))
        obj = mod(name=module_name,**kwargs)
        self.objects[module_type].append((kwargs,obj))
        return obj

        
# Make a factory
factory = sram_factory()

