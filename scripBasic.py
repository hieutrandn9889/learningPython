# List
movies = ["test1", "test2", "test3", "test4"]
print(movies[1:4])  # ['test2', 'test3', 'test4']
print(movies[1:])  # ['test2', 'test3', 'test4']
print(movies[:2])  # ['test1', 'test2']
print(movies[-1])  # test4
print(len(movies))

# add test5
movies.append("test5")
print(movies)  # ['test1', 'test2', 'test3', 'test4', 'test5']

# skip test5
movies.pop()
print(movies)  # ['test1', 'test2', 'test3', 'test4']

# skip test1 and test5
movies.pop(0)
print(movies)  # ['test2', 'test3', 'test4']

# for loops
for x in movies:
    print(x)  # ['test2', 'test3, test4']

# while loops
i = 1
while i < 5:
    print(i)
    i += 1
