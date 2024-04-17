from enum import Enum, unique


@unique
class Gender(Enum):
    Male = "Male"
    Female = "Female"
    Others = "Others"
