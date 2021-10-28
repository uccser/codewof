def clean_room(room_contents, dirty_items):
    result = []
    for item in room_contents:
        if item in dirty_items:
            result.append(item)
    return result
