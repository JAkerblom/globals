import yaml

class Entity(yaml.YAMLObject):
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
    
    @classmethod
    def custom_constructor(cls, loader, node):
        value = loader.construct_scalar(node)
        return cls.__init__(value)

class Dataset(Entity):
    yaml_tag = u'!dataset'
    def __init__(self, name: str, type: str):
        super().__init__(name, type)

class AzureDWView(Dataset):
    yaml_tag = u'!az-dw-view'
    def __init__(self, name: str):
        super().__init__(name, 'az-dw-view')
        schema, table = map(str, name.split('.', 1))
        self.schema = schema
        self.table = table
    
    @staticmethod
    def custom_constructor(loader, node):
        value = loader.construct_scalar(node)
        return AzureDWView(value)

class AzureDWTable(Dataset):
    yaml_tag = u'!az-dw-table'
    def __init__(self, name: str):
        super().__init__(name, 'az-dw-table')
        schema, table = map(str, name.split('.', 1))
        self.schema = schema
        self.table = table

    @staticmethod
    def custom_constructor(loader, node):
        value = loader.construct_scalar(node)
        return AzureDWTable(value)

class AzureDWExternalTable(Dataset):
    yaml_tag = u'!az-dw-ext-table'
    def __init__(self, name: str):
        super().__init__(name, 'az-dw-ext-table')
        schema, table = map(str, name.split('.', 1))
        self.schema = schema
        self.table = table

    @staticmethod
    def custom_constructor(loader, node):
        value = loader.construct_scalar(node)
        return AzureDWExternalTable(value)

class Report(Entity):
    yaml_tag = u'!report'
    def __init__(self, name: str, type: str):
        super().__init__(name, type)

    @staticmethod
    def custom_constructor(loader, node):
        values = loader.construct_mapping(node, deep=True)
        return Report(**values)

class PowerBIReport(Report):
    yaml_tag = u'!pbi-report'
    def __init__(self, name: str):
        super().__init__(name, 'pbi-report')

    @staticmethod
    def custom_constructor(loader, node):
        value = loader.construct_scalar(node)
        return PowerBIReport(value)

class Relation(yaml.YAMLObject):
    yaml_tag = u'!relation'
    def __init__(self, left_hand_side: Entity, type: str, right_hand_side: Entity):
        self.left_hand_side = left_hand_side
        self.type = type
        self.right_hand_side = right_hand_side

    @staticmethod
    def custom_constructor(loader, node):
        values = loader.construct_sequence(node)
        left, relation, right = values
        return Relation(left, relation, right)

class DependsOn(Relation):
    yaml_tag = u'!dependsOn'
    def __init__(self, left_hand_side: Entity, right_hand_side: Entity):
        super().__init__(left_hand_side, 'dependsOn', right_hand_side)

    @staticmethod
    def custom_constructor(loader, node):
        values = loader.construct_mapping(node, deep=True)
        return DependsOn(**values)

class Version(yaml.YAMLObject):
    yaml_tag = u'!version'
    def __init__(self, version_number: str, comment: str):
        self.version_number = version_number
        self.comment = comment

    @staticmethod
    def custom_constructor(loader, node):
        value = loader.construct_scalar(node)
        a, b = map(str, value.split(' - '))
        return Version(a, b)

class ToDo(yaml.YAMLObject):
    yaml_tag = u'!todo'
    def __init__(self, type: str, title: str):
        self.type = type
        self.title = title

    @staticmethod
    def custom_constructor(loader, node):
        value = loader.construct_scalar(node)
        a, b = map(str, value.split(' - '))
        return ToDo(a, b)

class ArtifactMetadata(yaml.YAMLObject):
    yaml_tag = u'!ameta'

class CodeMetadata(yaml.YAMLObject):
    yaml_tag = u'!cmeta'

class BuildMetadata(yaml.YAMLObject):
    yaml_tag = u'!bmeta'

class GlobalSpecification(yaml.YAMLObject):
    yaml_tag = u'!globals'

    # def __init__(self, name: str, type: str, artifact: ArtifactMetadata, code: CodeMetadata, build: BuildMetadata):
    #     self.name = name
    #     self.type = type
    #     self.description = description
        
    #     self.artifact = artifact
    #     self.code = code
    #     self.build = build