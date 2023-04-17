def extractAndRemoveModules(kwargs: dict) -> dict:
    """
    This function is used to process the modules passed to the app.
    It will extract the modules and return a kwarg without the module.
    """
    localKwargs = {**kwargs}
    if 'modules' in localKwargs:
        del localKwargs['modules']
    modules = kwargs.get('modules', {})
    return {'modules':modules, 'kwargs':localKwargs}

def validateModuleCompleteness(self: object) -> None:
    '''This function is used to validate that all the modules are provided'''
    if 'daw' not in self.modules or self.modules['daw'] is None:
        raise Exception('No DAW module provided')
    if 'songs' not in self.modules or self.modules['songs'] is None: 
        raise Exception('No Songs module provided')
    if 'setlist' not in self.modules or self.modules['setlist'] is None: 
        raise Exception('No Setlist module provided')
    
