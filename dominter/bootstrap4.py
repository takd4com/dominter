# constants for bootstrap4 css

CSS_URL = 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css'
CSS_LINK_TEXT = 'link rel="stylesheet" href="{}"'.format(CSS_URL)
#CSS_LINK_TEXT = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">'


def col(num, od=0):
    return 'col-{}'.format(num)

GCONTAINER = 'container'
GCONTAINER_FLUID = 'container-fluid'
GROW = 'row'
GCOL = 'col'
COL_R_BASE = 'col-'
COL_R_SM = 'col-sm-'
COL_R_MD = 'col-md-'
COL_R_LG = 'col-lg-'
COL_R_XL = 'col-xl-'

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
