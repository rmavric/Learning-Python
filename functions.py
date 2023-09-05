def unlimited_arguments(args):
    for argument in args:
        print(argument)
#unlimited_arguments(1,2,3,4) => multiple arguments, prints nothing, because it expects only one argument, which are numbers
#unlimited_arguments([1,2,3,4]) => one argument, prints list of elements, because it receives only one argument, which is list





def unlimited_arguments(*args):
    print(args)     # => this gives us a TUPLE
    for argument in args:
        print(argument)
#unlimited_arguments(1,2,3,4) => multiple arguments, prints nothing, because it expects only one argument, which are numbers
#           => takes all arguments, separated with commas, and turns them into a list (TUPLE of arguments) because of * 
#unlimited_arguments([1,2,3,4]) => this doesn't fail but we only have only one argument 
#unlimited_arguments(*[1,2,3,4]) => this doesn't fail but we only have only one argument    
#           => because of this star in front of [] it once again returns tuple of elements





# * tells Python to accept an unlimited amount of unnamed arguments and pass them into the function as a tuple
# ** tells Python to accept and unlimited amount of named arguments and pass them into the function as a dictionary
def unlimited_arguments(*args, **keyword_args):
    print(keyword_args)
    # for argument in keyword_args:     => with that we are outputting only keys
    for k, argument in keyword_args.items():    # => like this we see key-value pairs
        print(k, argument)

#unlimited_arguments(1,2,3,4) => we don't get anything other than empty dictionary
#unlimited_arguments(1,2,3,4, name='Max', age=29) => any named argument will automatically be registered in keyword_args dictionary
        # => we get {'name': 'Max', 'age': 29}

