from enum import Enum


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
