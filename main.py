import sys
import yaml
import models
from globals import Utils

print('-'*50)
print(sys.version)
print('-'*50)

g = Utils('./codefile.sql')
g.resolve_variables()

print(g.get_globals().artifact)