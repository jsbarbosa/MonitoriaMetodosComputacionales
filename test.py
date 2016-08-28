# genetica.py will be imported as G
from analyzer import *
from multiprocessing import Pool as ThreadPool 

def resolver(expresion_object):
#    print("Resolviendo...")
    try:
        initial = time.perf_counter()
        expresion_object.resuelve()
        return time.perf_counter() - initial
    except Exception as e:
#        print("Exception:", e)
        return e
        
def graficar(expresion_object, analitica = False):
#    print("Graficando...")
    try:
        initial = time.perf_counter()
        expresion_object.graficar(analitica)
        return time.perf_counter() - initial
    except Exception as e:
#        print("Exception:", e)
        return e

def poblacion(file):
#    print("Ejecutando poblacion.py...")
    try:
        initial = time.perf_counter()
        exec(open(file).read())
        return time.perf_counter() - initial
    except Exception as e:
#        print("Exception:", e)
        return e
        
files = getFiles("*.zip")
folders = unzip(files)
firstRow = ["Apellido", "Nombre", "Lineas", "resolver (s)", "graficar (s)", "poblacion (s)", "positivos"]
output = ["p_t.pdf", "r_t.pdf", "p_poblacion.dat", "r_poblacion.dat", "r_histograma.pdf", "p_histograma.pdf"]
saveResults("Resultados.csv", firstRow)

def test(file):
    try:
        # disables posible printing
        replace(file + "/genetica.py", "print ", "# print")
        replace(file + "/poblacion.py", "print ", "# print") 
        
        # replaces the output location
        for item in output:
            replace(file + "/genetica.py", item, file + "/" + item)
            replace(file + "/poblacion.py", item, file + "/" + item)
        
        G = moduleImport(file + "/genetica.py", "genetica")      # includes path to system
        
        first, last = nameSplitter(file)
    
        print(file)
        
        lines = countLines(file + "/genetica.py")     # counts lines in file      
       
        temp = G.Expresion()
        time_resolver = resolver(temp)
        
        analitica = False
            
        time_graficar = graficar(temp, analitica)
        time_poblacion = poblacion(file + "/poblacion.py")
    
        positives = file_checker(file, output) #changeLocation(file, output) 
    
        result = [last, first, lines, time_resolver, time_graficar, time_poblacion, positives]
        saveResults("Resultados.csv", result)
        
    except Exception as e:
        print(e)
        
initial_time = time.perf_counter()
pool = ThreadPool(4)
results = pool.map(test, folders)
    
pool.close() 
pool.join() 

print("===============================================")
print("Total time was %.3f seconds"%(time.perf_counter()-initial_time))
