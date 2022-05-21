from src.utils.db_utils import get_all_plates
from src.utils.license_plates_comparator import LicensePlatesComparator


def get_info_about_plate(plate_nb: str):
    plates = get_all_plates()
    comparator = LicensePlatesComparator()

    for plate in plates:
        if comparator.compare_license_plates_strings(plate_nb, plate.plate_nb):
            return plate.comment
    return None


print(get_info_about_plate("LUB45Q5"))
