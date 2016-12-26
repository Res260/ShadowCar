"""
    @file        main.py
    @description 
    @author      Res260 
    @created_at  20161220
    @updated_at  20161220
"""
from ShadowCarPackage.ShadowCar import ShadowCar


def main():
	"""
		Starts the program.
	"""
	shadow_car = ShadowCar()
	shadow_car.start()


if __name__ == "__main__":
	main()