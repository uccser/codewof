def is_forest(items):
    tree_count = items.count("tree")
    tree_count = items.count("Tree")
    return tree_count > 1
