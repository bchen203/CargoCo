import sys
sys.path.append('../CargoCo')
import manifest
import calculate
import balance_operator


#Going to grab some of the test cases provided as an example. For now, writing test cases for the balance solution calculator, will copy over other tests after:

def test_case_1():
    print("Test Case 1: Ship is already Balanced")
    mani = manifest.Manifest("SampleManifests/BalanceTestPreBalanced.txt")
    manifest_info = mani.copyManifest()
    calculator = calculate.Calculate(manifest_info[0], manifest_info[1])
    balance_operator_object = balance_operator.BalanceOperator(calculator, mani)



    instructions = balance_operator_object.perform_balance_operation(calculator.ship_bay_array)
    if instructions == []:
        print("TEST PASSED")
    else:
        print("Test FAILED")


#Unbalanceable:
def test_case_2():
    print("Test Case 2: Ship is cannot be Balanced (no SIFT yet)")
    mani = manifest.Manifest("SampleManifests/BalanceTestUnbalanceable.txt")
    manifest_info = mani.copyManifest()
    calculator = calculate.Calculate(manifest_info[0], manifest_info[1])
    balance_operator_object = balance_operator.BalanceOperator(calculator, mani)


    instructions = balance_operator_object.perform_balance_operation(calculator.ship_bay_array)
    if instructions == None: #will add SIFT later
        print("TEST PASSED")
    else:
        print("Test FAILED")


#Test 3 - Balance Cases:
def test_case_3():
    print("Test Case 3: Small expected balancing case")
    mani = manifest.Manifest("SampleManifests/BalanceTest1Manifest.txt")
    manifest_info = mani.copyManifest()
    calculator = calculate.Calculate(manifest_info[0], manifest_info[1])
    balance_operator_object = balance_operator.BalanceOperator(calculator, mani)

    instructions = balance_operator_object.perform_balance_operation(calculator.ship_bay_array)

    for instruction in instructions:
        calculator.moveContainer(instruction.starting_location[0], instruction.starting_location[1], instruction.ending_location[0], instruction.ending_location[1])

    if balance_operator_object.is_ship_balanced(calculator.ship_bay_array):  
        print("TEST PASSED")
    else:
        print("Test FAILED")
    mani.exportManifest()


#Test 4:
def test_case_4():
    print("Test Case 4: Small expected balancing case")
    mani = manifest.Manifest("SampleManifests/BalanceTest2Manifest.txt")
    manifest_info = mani.copyManifest()
    calculator = calculate.Calculate(manifest_info[0], manifest_info[1])
    balance_operator_object = balance_operator.BalanceOperator(calculator, mani)

    instructions = balance_operator_object.perform_balance_operation(calculator.ship_bay_array)
    for instruction in instructions:
        calculator.moveContainer(instruction.starting_location[0], instruction.starting_location[1], instruction.ending_location[0], instruction.ending_location[1])

    if balance_operator_object.is_ship_balanced(calculator.ship_bay_array):  
        print("TEST PASSED")
    else:
        print("Test FAILED")
    mani.exportManifest()

#Test 5:
def test_case_5():
    print("Test Case 5: Small expected balancing case")
    mani = manifest.Manifest("SampleManifests/BalanceTest3Manifest.txt")
    manifest_info = mani.copyManifest()
    calculator = calculate.Calculate(manifest_info[0], manifest_info[1])
    balance_operator_object = balance_operator.BalanceOperator(calculator, mani)

    instructions = balance_operator_object.perform_balance_operation(calculator.ship_bay_array)
    for instruction in instructions:
        calculator.moveContainer(instruction.starting_location[0], instruction.starting_location[1], instruction.ending_location[0], instruction.ending_location[1])

    if balance_operator_object.is_ship_balanced(calculator.ship_bay_array):  
        print("TEST PASSED")
    else:
        print("Test FAILED")

    mani.exportManifest()


test_case_1()
test_case_2()
test_case_3()
test_case_4()
test_case_5()