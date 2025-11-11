from sympy.physics.units import Quantity, voltage, current, ohm, convert_to

def main():
    vs = Quantity('vs')
    vs.set_dimension(voltage)
    vs_i = Quantity('vs_i')
    vs_i.set_dimension(current)

    result = convert_to(vs/vs_i, ohm)
    expected_result = ohm
    if result != expected_result:
        raise AssertionError(f"Expected {expected_result} but got {result}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

exit(0)
