def package_loader():
    max_package_weight = 20
    min_item_weight = 1
    max_item_weight = 10

    #Prompt user for number of items

    while True:
        try:
            max_items = int(input("Enter the maximum number of items to be ship"))
            if max_items <= 0:
                print("Please enter a positive number greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    # Tracking variables
    current_package_weight = 0
    package_weights = [] # list of package weights
    item_count = 0

    while item_count < max_items:
        try:
            weight = int(input(f"Enter weight for item {max_items + 1} (1-10, or 0 to stop): "))
            if weight == 0:
                break
            if weight < min_item_weight or weight > max_item_weight:
                print(f"Invalid weight! Item weight must be between {min_item_weight} and {max_item_weight} (or 0 to stop).")
                continue

            if current_package_weight + weight > max_package_weight:
                # Send current package
                package_weights.append(current_package_weight)
                print(f"Package {len(package_weights)} sent with {current_package_weight} kg.")
                # start new package
                current_package_weight = weight
            else:
                current_package_weight += weight
            item_count += 1

        except ValueError:
            print("Invalid input.n Please enter a valid integer.")


    if current_package_weight > 0:
        package_weights.append(current_package_weight)
        print(f"Package {len(package_weights)} sent with {current_package_weight} kg.")


    if package_weights:
        num_packages = len(package_weights)
        total_weight = sum(package_weights)
        unused_capacity = num_packages * max_package_weight - total_weight


        unused_list = [max_package_weight - w for w in package_weights]
        max_unused = max(unused_list)
        package_with_max_unused = unused_list.index(max_unused) + 1

        print("\n--- Shipping Summary ---")
        print(f"Number of packages sent: {num_packages}")
        print(f"Total weight of packages sent: {total_weight} kg")
        print(f"Total unused capacity: {unused_capacity} kg")
        print(f"Package {package_with_max_unused} had the most unused capacity: {max_unused} kg")
    else:
        print("\nNo packages were sent.")


if __name__ == "__main__":
    package_loader()