from enum import Enum, unique


@unique
class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    Others = "Others"
