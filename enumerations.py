from enum import Enum


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


class PackageType(Enum):
    BAG = "Bag"
    BL = "Bale"
    BRL = "Barrel"
    BSK = "Basket"
    BX = "Box"
    BKT = "Bucket"
    BLKH = "Bulkhead"
    BDL = "Bundle"
    CRB = "Carboy"
    CTN = "Carton"
    CS = "Case"
    CHT = "Chest"
    CL = "Coil"
    CRT = "Crate"
    CYL = "Cylinder"
    DR = "Drum"
    FIR = "Firkin"
    HMP = "Hamper"
    HHD = "Hogshead"
    KEG = "Keg"
    PKG = "Package"
    PL = "Pail"
    PLT = "Pallet"
    PC = "Piece"
    RK = "Rack"
    REL = "Reel"
    RL = "Roll"
    SKD = "Skid"
    SLP = "Slip Sheet"
    TOTE = "Tote"
    TRK = "Trunk"
    TB = "Tube"


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

class TradeshowDeliveryTypes(Enum):
    ADVANCED_WAREHOUSE = "AW"
    DIRECT_TO_TRADE_SHOW = "DTS"