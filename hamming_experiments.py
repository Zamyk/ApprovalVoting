from generators import approval_ic_profile_generator
from rules import OrderedWeightedHamming

profile = approval_ic_profile_generator(["A", "B", "C"], 20)
print(profile)

election = OrderedWeightedHamming(profile=profile)
print(election)