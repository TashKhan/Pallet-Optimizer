import pallet
import pallet_optimization 
from pallet_optimization import optimal_linear_feet




if __name__ == "__main__":
    pallets = [
        pallet.Pallet(48, 48, 32, False),
        pallet.Pallet(48, 48, 32, False),
    ]

    answer = optimal_linear_feet(pallets)
    print("Final billed linear feet:", answer)