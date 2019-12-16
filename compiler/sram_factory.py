# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from globals import OPTS

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
        A generic function to create a module with a given module_type.
        The args are passed directly to the module constructor.
        """
        try:
            from tech import tech_modules
            real_module_type = tech_modules[module_type]
        except ImportError:
            # If they didn't define these, then don't use the option types.
            # Primarily for backward compatibility and simplicity of tech files.
            pass
        
        if hasattr(OPTS, module_type):
            # Retrieve the name from OPTS if it exists,
            # otherwise just use the name
            real_module_type = getattr(OPTS, module_type)
            
        # Either retrieve the already loaded module or load it
        try:
            # Load a cached version from previous usage
            mod = self.modules[real_module_type]
        except KeyError:
            # Dynamically load the module
            import importlib
            c = importlib.reload(__import__(real_module_type))
            mod = getattr(c, real_module_type)
            self.modules[real_module_type] = mod
            self.module_indices[real_module_type] = 0
            self.objects[real_module_type] = []
            
        # Either retreive a previous object or create a new one
        for obj in self.objects[real_module_type]:
            (obj_kwargs, obj_item) = obj
            # Must have the same dictionary exactly (conservative)
            if obj_kwargs == kwargs:
                return obj_item

        # Use the default  name if there are default arguments
        # This is especially for library cells so that the
        # spice and gds files can be found.
        if len(kwargs) > 0:
            # Create a unique name and increment the index
            module_name = "{0}_{1}".format(real_module_type,
                                           self.module_indices[real_module_type])
            self.module_indices[real_module_type] += 1
        else:
            module_name = real_module_type

        # type_str = "type={}".format(real_module_type)
        # name_str = "name={}".format(module_name)
        # kwargs_str = "kwargs={}".format(str(kwargs))
        # import debug
        # debug.info(0, "New module:" + type_str + name_str + kwargs_str)
        obj = mod(name=module_name, **kwargs)
        self.objects[real_module_type].append((kwargs, obj))
        return obj

    def get_mods(self, module_type):
        """Returns list of all objects of module name's type."""
        if hasattr(OPTS, module_type):
            # Retrieve the name from OPTS if it exists,
            # otherwise just use the input
            module_type = getattr(OPTS, module_type)
        try:
            mod_tuples = self.objects[module_type]
            mods = [mod for kwargs, mod in mod_tuples]
        except KeyError:
            mods = []
        return mods

    
# Make a factory
factory = sram_factory()
