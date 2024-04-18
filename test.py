from pyswip import Prolog

prolog = Prolog()

prolog.consult("test_prolog.pl")

answer = list(prolog.query("faster(tiger, dog)"))

print(answer)