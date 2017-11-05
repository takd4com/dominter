# constants for pure css

CSS_URL = "https://cdnjs.cloudflare.com/ajax/libs/pure/1.0.0/pure-min.css"
CSS_LINK_TEXT = 'link rel="stylesheet" href="{}"'.format(CSS_URL)
#CSS_LINK_TEXT = 'link rel="stylesheet" href="https://unpkg.com/purecss@1.0.0/build/pure-min.css" integrity="sha384-nn4HPE8lTHyVtfCBi5yW9d20FjT8BJwUXyWZT9InLYax14RDjBj46LmSztkmNP9w" crossorigin="anonymous"'


def col(num, od=0):
    return 'pure-u-{}-24'.format(num * 2 + od)

GCONTAINER = ''
GCONTAINER_FLUID = ''
GROW = 'pure-g'
GCOL = ''
COL_R_BASE = '-u-'
COL_R_SM = '-u-sm-'
COL_R_MD = '-u-md-'
COL_R_LG = '-u-lg-'
COL_R_XL = '-u-xl-'

GCOL3 = (
    '',  # for GCOL3[0], use GCOL3[1]-GCOL3[3]
    col(4), col(8), col(12),
)

GCOL4 = (
    '',  # for GCOL4[0], use GCOL4[1]-GCOL4[4]
    col(3), col(6), col(9), col(12),
)

GCOL5 = (
    '',  # for GCOL5[0], use GCOL5[1]-GCOL5[5]
    col(2), col(5), col(7), col(10), col(12),
)

GCOL6 = (
    '',  # for GCOL6[0], use GCOL6[1]-GCOL5[6]
    col(2), col(4), col(6), col(8), col(10), col(12),
)

GCOL12 = (
    '',  # for GCOL12[0], use GCOL12[1]-GCOL12[12]
    col(1), col(2), col(3), col(4), col(5), col(6),
    col(7), col(8), col(9), col(10), col(11), col(12),
)

GCOL24 = (
    '',  # for GCOL12[0], use GCOL12[1]-GCOL12[12]
    col(1), col(1, 1), col(2), col(2, 1), col(3), col(3, 1),
    col(4), col(4, 1), col(5), col(5, 1), col(6), col(6, 1),
    col(7), col(7, 1), col(8), col(8, 1), col(9), col(9, 1),
    col(10), col(10, 1), col(11), col(11, 1), col(12), col(12, 1),
)

GSM3 = tuple(s.replace(COL_R_BASE, COL_R_SM) for s in GCOL3)
GMD3 = tuple(s.replace(COL_R_BASE, COL_R_MD) for s in GCOL3)
GLG3 = tuple(s.replace(COL_R_BASE, COL_R_LG) for s in GCOL3)
GXL3 = tuple(s.replace(COL_R_BASE, COL_R_XL) for s in GCOL3)
GSM4 = tuple(s.replace(COL_R_BASE, COL_R_SM) for s in GCOL4)
GMD4 = tuple(s.replace(COL_R_BASE, COL_R_MD) for s in GCOL4)
GLG4 = tuple(s.replace(COL_R_BASE, COL_R_LG) for s in GCOL4)
GXL4 = tuple(s.replace(COL_R_BASE, COL_R_XL) for s in GCOL4)
GSM5 = tuple(s.replace(COL_R_BASE, COL_R_SM) for s in GCOL5)
GMD5 = tuple(s.replace(COL_R_BASE, COL_R_MD) for s in GCOL5)
GLG5 = tuple(s.replace(COL_R_BASE, COL_R_LG) for s in GCOL5)
GXL5 = tuple(s.replace(COL_R_BASE, COL_R_XL) for s in GCOL5)
GSM6 = tuple(s.replace(COL_R_BASE, COL_R_SM) for s in GCOL6)
GMD6 = tuple(s.replace(COL_R_BASE, COL_R_MD) for s in GCOL6)
GLG6 = tuple(s.replace(COL_R_BASE, COL_R_LG) for s in GCOL6)
GXL6 = tuple(s.replace(COL_R_BASE, COL_R_XL) for s in GCOL6)
GSM12 = tuple(s.replace(COL_R_BASE, COL_R_SM) for s in GCOL12)
GMD12 = tuple(s.replace(COL_R_BASE, COL_R_MD) for s in GCOL12)
GLG12 = tuple(s.replace(COL_R_BASE, COL_R_LG) for s in GCOL12)
GXL12 = tuple(s.replace(COL_R_BASE, COL_R_XL) for s in GCOL12)
GSM24 = tuple(s.replace(COL_R_BASE, COL_R_SM) for s in GCOL24)
GMD24 = tuple(s.replace(COL_R_BASE, COL_R_MD) for s in GCOL24)
GLG24 = tuple(s.replace(COL_R_BASE, COL_R_LG) for s in GCOL24)
GXL24 = tuple(s.replace(COL_R_BASE, COL_R_XL) for s in GCOL24)
