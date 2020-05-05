from statistics import mean
from glob import glob
from os.path import join, isfile

avg_diff = lambda lst1, lst2: mean(map(lambda tup: abs(tup[0]-tup[1]), zip(lst1, lst2)))

no_space = lambda lst: [item.lstrip() for item in lst]

remove_line_whitespace = lambda s: '\n'.join(map(lambda st: st.strip(), s.splitlines()))

has_dup = lambda l: len([item for item in l if l.count(item) > 1]) > 0

flatten = lambda l: [item for lst in l for item in lst]

grep = lambda folder, string: [path for path in glob(join(folder, '*')) if isfile(path) and string in open(path, 'r').read()]

def main():
	print(avg_diff([1, 1, 1, 1], [1, 2, 3, 4]))
	print(no_space(["   string", "string   ", " \t\t\tstring\t "]))
	print(remove_line_whitespace("""
	Line
		Another line\t
		\tMore lines
	\t\t  These lines won't end!\t
	
	"""))
	print(has_dup([1, 2, 3, 4]), has_dup(["a", "aa", "aa", "b"]))
	print(flatten([[25, 15, 21], [1, 18, 5], [3, 12, 5, 22, 5, 18]]))
	print(grep(r'C:\test', 'hello'))


if __name__ == '__main__':
	main()
