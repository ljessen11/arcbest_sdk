from enum import Enum


class PackageType(Enum):
    Bag = "BAG"
    Bale = "BL"
    Barrel = "BRL"
    Basket = "BSK"
    Box = "BX"
    Bucket = "BKT"
    Bulkhead = "BLKH"
    Bundle = "BDL"
    Carboy = "CRB"
    Carton = "CTN"
    Case = "CS"
    Chest = "CHT"
    Coil = "CL"
    Crate = "CRT"
    Cylinder = "CYL"
    Drum = "DR"
    Firkin = "FIR"
    Hamper = "HMP"
    Hogshead = "HHD"
    Keg = "KEG"
    Package = "PKG"
    Pail = "PL"
    Pallet = "PLT"
    Piece = "PC"
    Rack = "RK"
    Reel = "REL"
    Roll = "RL"
    Skid = "SKD"
    Slip_Sheet = "SLP"
    Tote = "TOTE"
    Trunk = "TRK"
    Tube = "TB"


class UnitsOfMeasurement(Enum):
    FT = "FT"
    IN = "IN"
    M = "M"


class LimitedAccessOptions(Enum):
    CHURCH = "C",
    MILITARY = "M",
    SCHOOL = "S",
    MINI_STORAGE = "U"
    OTHER = "O"


class ShipmentClasses(Enum):
    CLASS_50 = 50
    CLASS_55 = 55
    CLASS_60 = 60
    CLASS_65 = 65
    CLASS_70 = 70
    CLASS_77_5 = 77.5
    CLASS_85 = 85
    CLASS_92_5 = 92.5
    CLASS_100 = 100
    CLASS_110 = 110
    CLASS_125 = 125
    CLASS_150 = 150
    CLASS_175 = 175
    CLASS_200 = 200
    CLASS_250 = 250
    CLASS_300 = 300
    CLASS_400 = 400
    CLASS_500 = 500
