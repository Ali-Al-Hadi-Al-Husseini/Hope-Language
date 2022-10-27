from Hope import run,InvalidSyntaxErorr


x ,err = run("""for i= 1 -> 5 >>
                print(i) ;
                <<      """,'hola.hope')
print(x,err)