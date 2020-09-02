/*
&G !globals
name: Users
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
    - &ref1 !az-dw-ext-table stg.Users
    - &ref2 !dataset
        name: hist.Users
        type: az-dw-table
    - &ref3 !az-dw-view core.Users
  outputs: 
    - &ref4 !az-dw-ext-table hist.Users_Daily_bkp
  externals:
    - &ref5 !az-dw-table core.SomeKeyTable
    - &report !pbi-report Road to 500k
  dependencies:
    - !relation [*ref3, dependsOn, *ref2]
    - !relation [*report, dependsOn, [*ref3, *ref1]]
    - !relation [*ref2, generatesKeysTo, $ref5]
  variables: {this: *G, ref1: *ref1, ref5: *ref5}
endglobals */

select * from dbo.[Users]

declare @var1 varchar(20) = 'stg.Users'
declare @var2 varchar(20) = 'stg.Users'

exec dbo.LogConsumer @inparam = 'core.SomeKeyTable'