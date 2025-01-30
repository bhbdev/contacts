from flask import render_template

class Page:
    def __init__(self,config:dict={}):
        self.title = "Untitled"
        self.template = "base/docframe.html"
        for key,val in config.items():
            setattr(self,key,val)
    
    def render(self):
        data = self.__dict__
        return render_template(self.template, **data)