import os
import sys
import re as regex
import yaml
import models

class Utils(object):

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.add_constructors(self.get_tag_mappings())
        self.update_globals(self.get_content())

    def get_content(self):
        f = open(self.filepath, "r")
        return f.read()

    def get_globals(self):
        return self.__globalspecification

    def update_content_and_globals(self, content: str):
        f = open(self.filepath, "w")
        f.write(content)
        self.update_globals(content)

    def update_globals(self, content: str):
        expression = regex.compile(r"\/\*(.*)endglobals \*\/", flags=regex.S)
        matches = expression.match(content)
        specification_raw = matches.group(1)
        specification = yaml.load(specification_raw, Loader=yaml.FullLoader)

        self.__globalspecification = specification

    def get_variable_state(self):
        variable_objects = {key: value.__dict__ for key, value in self.__globalspecification.code.variables.items()}
        unresolved_variables = self.get_unresolved_variable_usages()
        all_resolved = len(unresolved_variables) == 0

        return variable_objects, unresolved_variables, all_resolved 

    def get_unresolved_variable_usages(self) -> set:
        content = self.get_content()
        expression = regex.compile(r'\{{2}([\w\d\.]+)\}{2}')
        unique_matches = set(expression.findall(content))
        
        return unique_matches
    
    def resolve_variables(self):
        variables, unresolved, done = self.get_variable_state()
        i = 0
        while not done:
            print(self.get_variable_state()[1])
            an_unresolved_element = unresolved.pop()
            transformation_output = self.resolve_variable(variables, an_unresolved_element)
            print(transformation_output)
            if transformation_output['status'] == 'RESOLVED': 
                self.replace_variable_usages(an_unresolved_element, transformation_output['output'])
            elif transformation_output['status'] == 'UNRESOLVED':
                print(unresolved)
                unresolved.update(set([an_unresolved_element]))
                print(unresolved)
            elif transformation_output['status'] == 'ERROR': 
                sys.exit(transformation_output['reason'])

            variables, unresolved_updated, done = self.get_variable_state()
            i = i + 1
            if i > 10: sys.exit("Too many tries to resolve variable. Exiting...")

    def resolve_variable(self, variable_objects: dict, input: str):
        tmp = variable_objects
        for property in input.split('.'):
            try:
                tmp = tmp.get(property)
            except: 
                return {'status': 'ERROR', 'reason': "Couldn't retrieve variable property from the global specification object"}
        
        if not self.has_brackets(tmp) and type(tmp) == str:
            return {'status': 'RESOLVED', 'output': tmp}
        else:
            return {'status': 'UNRESOLVED', 'input': input}

    def has_brackets(self, input: str):
        return False if input.find('{{') == -1 and input.find('}}') == -1 else True

    def replace_variable_usages(self, unresolved: str, resolved: str):
        content = self.get_content()
        new_content, replace_count = regex.subn(r'\{{2}%s\}{2}' % unresolved, resolved, content)
        self.update_content_and_globals(new_content)
        
        print("Nr replacements made: %s" % replace_count)
        return replace_count

    def add_constructors(self, models: list):
        for mapping in models:
            yaml.add_constructor(mapping['tag'], mapping['model'].custom_constructor)
    
    def get_tag_mappings(self) -> list:
        return [
            {'tag': u'!az-dw-view', 'model': models.AzureDWView},
            {'tag': u'!az-dw-table', 'model': models.AzureDWTable},
            {'tag': u'!az-dw-ext-table', 'model': models.AzureDWExternalTable},
            {'tag': u'!version', 'model': models.Version},
            {'tag': u'!todo', 'model': models.ToDo},
            {'tag': u'!report', 'model': models.Report},
            {'tag': u'!pbi-report', 'model': models.PowerBIReport},
            {'tag': u'!dependsOn', 'model': models.DependsOn},
            {'tag': u'!relation', 'model': models.Relation}
        ]