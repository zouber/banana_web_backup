# -*- coding: utf-8 -*-
import string

a_string = '\^stack\.\*/overflo\\w\$arr=1'
escaped = a_string.translate(string.maketrans({"-":  r"\-",
                                            "]":  r"\]",
                                            "\\": r"\\",
                                            "^":  r"\^",
                                            "$":  r"\$",
                                            "*":  r"\*",
                                            ".":  r"\."}))

print escaped