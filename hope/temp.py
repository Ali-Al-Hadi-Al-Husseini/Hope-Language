from Hope import run,InvalidSyntaxErorr


x ,err = run("""let i = 0; while i < 10 >>; print(i); i = i + 1 ;<< ; print(i)""",'hola.hope')
print(x,err)