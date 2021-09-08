def add_bookends(books):
    return ['Bookend'] + books + ['Bookend']


print(add_bookends(["Harry Potter", "Treasure Island", "Oliver Twist", "Alice In Wonderland", "The Secret Garden"]))
print(add_bookends(["Alice In Wonderland"]))
print(add_bookends([]))
