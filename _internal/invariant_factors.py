from collections.abc import Mapping, Sequence
import bisect


def prime_factors(number: int) -> dict[int, int]:
    divisor = 2
    factors = {}
    while divisor * divisor <= number:
        if number % divisor:
            divisor += 1
        else:
            power = 1
            while number % (divisor ** (power + 1)) == 0:
                power += 1
            factors[divisor] = power
            number /= divisor ** power
    if number > 1:
        factors[number] = 1
    return factors


def invariant_factors(numbers: Sequence[int]) -> list[int]:
    prime_powers = {}
    for number in numbers:
        prime_decomposition = prime_factors(number)
        for prime, power in prime_decomposition.items():
            sorted_powers = prime_powers.get(prime, [])
            bisect.insort(sorted_powers, power)
            prime_powers[prime] = sorted_powers

    for prime, powers_set in prime_powers.items():
        prime_powers[prime] = list(powers_set)

    max_prime_divisible_count = max(
        len(powers) for _, powers in prime_powers.items()
    )

    factors = []

    for index in range(max_prime_divisible_count, 0, -1):
        factor = 1
        for prime, powers in prime_powers.items():
            if index <= len(powers):
                factor *= prime ** powers[-index]
        factors.append(factor)

    return factors
