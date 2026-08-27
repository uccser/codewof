def boxes_needed(envelopes):
    boxes = envelopes // 20
    if envelopes % 20 != 0:
        boxes += 1
    return boxes
