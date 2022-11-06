from Hope import run,InvalidSyntaxErorr


x ,err = run("""let i=0; while i < 5 >> ; print(i) ; i = 1 + i ;<< ; print(i == 4)""",'hola.hope')
print(x,err)