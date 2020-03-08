""" Conversions """


def inches_to_m(inches):
    return inches*0.0254


def pounds_to_kg(pounds):
    return pounds*0.453592


def lbshr_to_kgsec(lbshr):
    return lbshr/7936.64


def lbsinch_to_kgm(lbsinch):
    return 0.0115212462*lbsinch


def kt_to_ms(kt):
    return 0.514444*kt


def cdeg_to_kdeg(cdeg):
    return cdeg + 273.15


def feet_to_m(feet):
    return 0.3048*feet