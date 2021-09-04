# Hope language
  Hope is a small programing lanuage developed by Ali Al Hadi
  
#Variable

## string or number varibles declaration

'''code
let var_name = some_value
'''
## list declaration
'''code
   let list_name = [list_elements] (use comma between elements)
'''
# Control-Flow

## If conditional
'''code
  if condition >> 
    do_something
    << 

'''

## Elif conditional
'''code
  if condition >> 
    do_something
  elif another_condition>>
    do_something_else (if and only if the first_conditon is not true and the 2nd is true)
    << 

'''
## Else conditional
'''code
  if condition >> 
    do_something
  else >>
    do_something_else
    << 

'''
## inline If conditional
'''code
  if condition >> do_something
  (it is possible to use elif and else control-flow in the same line like the flowing line)
  
  if conditon >> do_Something else do_something_else

'''
## Using control-flow inside a variable
'''code
  let var_name = if condition >> give_the_variable_this_value else give_it_another_value

'''

# Loops

## For loop
'''code
    for i=start_value -> end_value >>
    body
    <<
'''

## inline For loops
'''code
    for i=start_value -> end_value >> do_somthing
'''

## while loop
'''code

  while condition >>
    body
    <<

'''
## inline while loop
'''code

  while condition >> do_something

'''


#Functions

## typical function declaration 
'''code
    func function_name(paramters) >>
      Body
    <<
'''

##  function declaration  in variables
'''code
   let function_name =  func (paramters) >>
                              Body
                              return something
                            <<
'''

##  inline function declaration  
'''code
   func function_name(paramters) >> return_value(directly no need for return keyword)
                              
'''

Hope is inspired by python and javascript with a twist

