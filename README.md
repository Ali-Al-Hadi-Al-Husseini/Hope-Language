# Hope language
  Hope is a small programing lanuage developed by Ali Al Hadi
  it is inspired by python and javascript with a small twist
  
## Variable

### string or number varibles declaration

    let var_name = some_value
    
### list declaration
    
    let list_name = [list_elements] (use comma between elements)

## Control-Flow

### If conditional

    if condition >> 
        do_something
    << 
    


### Elif conditional

    if condition >> 
            do_something
    elif another_condition>>
        do_something_else 
        (if and only if the first_conditon is not true and the 2nd is true)
    << 


### Else conditional

    if condition >> 
        do_something
    else >>
        do_something_else
    << 

### inline If conditional

    if condition >> do_something
    (it is possible to use elif and else control-flow in the same line like the flowing line)
    if conditon >> do_Something else do_something_else


### Using control-flow inside a variable

    let var_name = if condition >> give_the_variable_this_value else give_another_value



## Loops

### For loop

    for i=start_value -> end_value >>
            body
    <<


### inline For loops
    
        for i=start_value -> end_value >> do_somthing


### while loop

    
      while condition >>
        body
        <<


### inline while loop

    while condition >> do_something

## Functions

### typical function declaration 

    func function_name(paramters) >>
            Body
        <<


###  function declaration  in variables

    let function_name =  func (paramters) >>
                              Body
                              return something
                            <<


###  inline function declaration  

    func function_name(paramters) >> return_value(directly no need to use  return keyword)
                              
                              
                              
       
## Runing Hope

### Runing from file (in terminal)

  python3 Hope.py file_name
 
 
### Runing  hope shell

  python3 Hope.py (shell will automaticaly start to stop shell use exit keyword)



