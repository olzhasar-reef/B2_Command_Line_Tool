######################################################################
#
# File: b2/transferer/range.py
#
# Copyright 2018 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################


class Range(object):
    """
    HTTP ranges use an *inclusive* index at the end.
    """

    def __init__(self, start, end):
        assert 0 <= start <= end
        self.start = start
        self.end = end

    def size(self):
        return self.end - self.start + 1

    def subrange(self, sub_start, sub_end):
        """
        Returns a range that is part of this range.
        :param sub_start: Index relative to the start of this range.
        :param sub_end: (Inclusive!) index relative to the start of this range.
        :return: A new Range
        """
        assert 0 <= sub_start <= sub_end < self.size()
        return Range(self.start + sub_start, self.start + sub_end)

    def as_tuple(self):
        return self.start, self.end

    def __repr__(self):
        return 'Range(%d, %d)' % (self.start, self.end)
