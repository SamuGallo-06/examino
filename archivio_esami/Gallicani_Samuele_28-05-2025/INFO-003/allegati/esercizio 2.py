def cercaMaggiore(n1, n2):
    if(n1 > n2):
        print(f"Numero maggiore: {n1}")
    elif(n2>n1):
        print(f"Numero maggiore: {n2}")
    else:
        print("I due numeri sono uguali")
    
pippo = input("Inserisci un numero...")
paperino = input("Inserisci un'altro numero...")
cercaMaggiore(pippo, paperino)  