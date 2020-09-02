/*
&G !globals
name: SomeTable
type: sql
artifact: !ameta
  description: Does nothing at all
  versions:
    - !version 1.000 - Initial version
    - !version 1.100 - Second version
  todos:
    - !todo bug - Error code
    - !todo change - Not done yet
build: !bmeta
  version: 1
  infer:
    - coreview-dep
code: !cmeta
  definitions:
    - &ref1 !az-dw-ext-table stg.{{this.name}}
    - &ref2 !dataset
        name: hist.{{this.name}}
        type: az-dw-table
    - &ref3 !az-dw-view core.{{this.name}}
  outputs: 
    - &ref4 !az-dw-ext-table hist.{{this.name}}_Daily_bkp
  externals:
    - &ref5 !az-dw-table core.SomeKeyTable
    - &report !pbi-report Road to 500k
  dependencies:
    - !relation [*ref3, dependsOn, *ref2]
    - !relation [*report, dependsOn, [*ref3, *ref1]]
    - !relation [*ref2, generatesKeysTo, $ref5]
  variables: {this: *G, ref1: *ref1, ref5: *ref5}
endglobals */

select * from dbo.[{{this.name}}]

declare @var1 varchar(20) = '{{ref1.name}}'
declare @var2 varchar(20) = '{{ref1.schema}}.{{ref1.table}}'

exec dbo.LogConsumer @inparam = '{{ref5.name}}'