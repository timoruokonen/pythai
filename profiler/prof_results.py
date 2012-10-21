import pstats

p = pstats.Stats('prof')
p.strip_dirs().sort_stats('cumulative').print_stats()


